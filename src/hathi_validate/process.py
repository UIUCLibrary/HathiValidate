"""Process that validations."""

import abc
import datetime
import hashlib
import logging
import os
import itertools
import typing
import re
from typing import Tuple, Iterator, List, Dict, Any, Generator, Optional
import yaml
from lxml import etree

from importlib.resources import files

from hathi_validate import result
from hathi_validate import xsd as hathi_xsd
from . import validator

DIRECTORY_REGEX = \
    r"^\d+(p\d+(_\d+)?)?(v\d+(_\d+)?)?(i\d+(_\d+)?)?(m\d+(_\d+)?)?$"

DATE_REGEX = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T(\d{2})\:(\d{2})(\:\d{2})?-(\d{2}):(\d{2})$"
)


class ValidationError(Exception):
    """Validation failed."""


class InvalidChecksum(ValidationError):
    """Checksum is invalid."""


def find_missing_files(path: str) -> result.ResultSummary:
    """Check for expected files exist on the path.

    Args:
        path:

    Yields: Any files missing

    """
    expected_files = [
        "checksum.md5",
        "marc.xml",
        "meta.yml",
    ]

    summery_builder = result.SummaryDirector(source=path)

    for file in expected_files:
        if not os.path.exists(os.path.join(path, file)):
            summery_builder.add_error("Missing file: {}".format(file))
    return summery_builder.construct()


def find_extra_subdirectory(path: str) -> result.ResultSummary:
    """Check path for any subdirectories.

    Args:
        path:

    Yields: Any subdirectory

    """
    summary_builder = result.SummaryDirector(source=path)
    for item in os.scandir(path):
        if item.is_dir():

            summary_builder.add_error(
                "Extra subdirectory {}".format(item.name)
            )

    return summary_builder.construct()


def parse_checksum(line: str) -> Tuple[str, str]:
    """Parse a line for checksum data.

    Args:
        line:

    Returns:
        Returns a tuple, (hash value, file name)

    """
    chunks = line.strip().split(" ")
    md5_hash = chunks[0]
    raw_filename = chunks[-1]
    if len(md5_hash) != 32:
        raise InvalidChecksum("Invalid Checksum")
    # For file names listed with an asterisk before them in the checksum file
    if raw_filename[0] == "*":
        filename = raw_filename[1:]
    else:
        filename = raw_filename
    return md5_hash, filename


def calculate_md5(filename: str, chunk_size: int = 8192) -> str:
    """Calculate the md5 hash value of a file."""
    md5 = hashlib.md5()

    with open(filename, "rb") as file_handle:
        while True:
            data = file_handle.read(chunk_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()


def is_same_hash(*hashes: str) -> bool:
    """Compare hash values to see if they are the same."""
    return all(
        hash_value_a.lower() == hash_value_b.lower()
        for hash_value_a, hash_value_b, in itertools.combinations(hashes, 2)
    )


def find_failing_checksums(path: str, report: str) -> result.ResultSummary:
    """Validate that the checksums in the .fil file match.

    Args:
        path:
        report:

    Returns: Error report

    """
    logger = logging.getLogger(__name__)
    report_builder = result.SummaryDirector(source=path)
    try:
        for report_md5_hash, filename in extracts_checksums(report):
            logger.debug(
                "Calculating the md5 checksum hash for %s", filename
            )
            file_path = os.path.join(path, filename)
            try:
                file_md5_hash = calculate_md5(filename=file_path)
                if not is_same_hash(file_md5_hash, report_md5_hash):
                    logger.debug(
                        'Hash mismatch for "%s". (Actual (%s): expected (%s))',
                        file_path, file_md5_hash, report_md5_hash
                    )
                    report_builder.add_error(
                        f"Checksum listed in {os.path.basename(report)} "
                        f"doesn't match for \"{filename}\""
                    )
                else:
                    logger.info(
                        "%s successfully matches md5 hash in %s",
                        filename, os.path.basename(report)
                    )
            except FileNotFoundError:
                logger.info(
                    "Unable to run checksum for missing file, %s", filename
                )
                report_builder.add_error(
                    f"Unable to run checksum for missing file, {filename}"
                )

    except FileNotFoundError:
        report_builder.add_error("File missing")
    return report_builder.construct()


def extracts_checksums(report: str) -> Iterator[Tuple[str, str]]:
    """Iterate over checksum hash values from a checksum report."""
    with open(report, "r") as file_read:
        for line in file_read:
            md5, filename = parse_checksum(line)
            yield md5, filename


def find_errors_marc(filename: str) -> result.ResultSummary:
    """Validate the MARC file.

    Args:
        filename:

    Returns:
        Returns a ResultSummary

    """
    summary_builder = result.SummaryDirector(source=filename)
    scheme = etree.XMLSchema(
        etree.XML(
            files(hathi_xsd)
            .joinpath("MARC21slim.xsd")
            .read_bytes()
        )
    )

    try:
        with open(filename, "r", encoding="utf8") as file_handle:
            raw_data = file_handle.read()
        doc = etree.fromstring(raw_data)
        if not scheme.validate(doc):  # type: ignore
            summary_builder.add_error("Unable to validate")
    except FileNotFoundError:
        summary_builder.add_error("File missing")
    except etree.XMLSyntaxError as error:
        summary_builder.add_error("Syntax error: {}".format(error))
    return summary_builder.construct()


def parse_yaml(filename: str) -> Dict[str, Any]:
    """Parse a YAML file."""
    with open(filename, "r") as file_handle:
        return yaml.load(file_handle, Loader=yaml.SafeLoader)


class AbsErrorLocator(abc.ABC):
    """Abstract base class for error locators."""

    def __init__(self, metadata: Dict[str, Any]) -> None:
        """Create new AbsErrorLocator object.

        Args:
            metadata:
        """
        self.metadata = metadata

    @abc.abstractmethod
    def find_errors(self) -> Generator[str, None, None]:
        """Find errors as strings.

        Yields:
            Yields errors as strings if found any, else returns None.

        """


class PageDataErrors(AbsErrorLocator):
    """Find errors in pagedata field."""

    def __init__(self,
                 filename: str,
                 path: str,
                 metadata: Dict[str, Any]) -> None:
        """Create new PageDataErrors object.

        Args:
            filename:
            path:
            metadata:
        """
        super().__init__(metadata)
        self.filename = filename
        self.path = path

    def find_errors(self) -> Generator[str, None, None]:
        """Find errors as strings.

        Yields:
            Yields errors as strings if found any, else returns None.

        """
        pages = self.metadata["pagedata"]
        for image_name in pages.keys():
            error_result = self.find_pagedata_file(image_name)
            if error_result is not None:
                yield error_result

    def find_pagedata_file(self, image_name: str) -> Optional[str]:
        """Locate pagedata file and check if exists.

        Args:
            image_name:

        Returns:
            If found any errors, returns message as human readable string. If
                no errors found, returns None.

        """
        if not os.path.exists(os.path.join(self.path, image_name)):
            return f"The pagedata {self.filename} contains an " \
                   f"nonexistent file {image_name}"

        return None


class CaptureDateErrors(AbsErrorLocator):
    """Find errors in capture_date field."""

    def find_errors(self) -> Generator[str, None, None]:
        """Find errors as strings.

        Yields:
            Yields errors as strings if found any, else returns None.

        """
        capture_date = self.metadata["capture_date"]

        if not isinstance(capture_date, datetime.datetime):
            if isinstance(capture_date, str):
                # Just because the parser wasn't able to convert into a
                #   datetime object doesn't mean it's not valid per se.
                #   It can also be a matched to a regex.
                if DATE_REGEX.fullmatch(capture_date) is None:
                    yield "Invalid YAML capture_date {}".format(
                        capture_date)
            else:
                yield "Invalid YAML data type for in capture_date"


class CaptureAgentErrors(AbsErrorLocator):
    """Find errors in capture_agent field."""

    def find_errors(self) -> Generator[str, None, None]:
        """Locate any errors with the capture_agent field in the metadata.

        Yields:
            Yields human-readable string of any issues. Otherwise, returns
                None if no problems discovered.

        """
        capture_agent = self.metadata["capture_agent"]
        potential_error = self.check_capture_agent_format(capture_agent)
        if potential_error is not None:
            yield potential_error

    @staticmethod
    def check_capture_agent_format(capture_agent_field: Any) -> Optional[str]:
        """Check the given fields matches what is expected of capture agent.

        Args:
            capture_agent_field:

        Returns:
            Returns a human-readable string of any issues. Otherwise, returns
                None if no problems discovered.

        """
        if not isinstance(capture_agent_field, str):
            return "Invalid YAML capture_agent: {}".format(capture_agent_field)
        return None


class FindErrorsMetadata:
    """Find errors metadata."""

    def __init__(self,
                 filename: str,
                 path: str,
                 require_page_data: bool = True
                 ) -> None:
        """Create new FindErrorsMetadata object.

        Args:
            filename:
            path:
            require_page_data:
        """
        self.filename = filename
        self.path = path
        self.require_page_data = require_page_data

    def find_errors(self) -> result.ResultSummary:
        """Find all metadata errors."""
        summary_builder = result.SummaryDirector(source=self.filename)
        try:
            yml_metadata = parse_yaml(filename=self.filename)

            try:
                capture_date_error_finder = CaptureDateErrors(yml_metadata)
                for error in capture_date_error_finder.find_errors():
                    summary_builder.add_error(error)

                capture_agent_error_finder = CaptureAgentErrors(yml_metadata)
                for error in capture_agent_error_finder.find_errors():
                    summary_builder.add_error(error)

                if self.require_page_data:
                    page_data_error_finder = PageDataErrors(
                        self.filename, self.path, yml_metadata
                    )
                    for error in page_data_error_finder.find_errors():
                        summary_builder.add_error(error)
            except KeyError as error:
                summary_builder.add_error(
                    "{} is missing key, {}".format(self.filename, error)
                )

        except yaml.YAMLError as error:
            summary_builder.add_error(
                "Unable to read {}. Reason:{}".format(self.filename, error)
            )
        except FileNotFoundError as error:
            summary_builder.add_error("Missing {}".format(error))
        return summary_builder.construct()


def find_errors_meta(
        filename: str,
        path: str,
        require_page_data: bool = True) -> result.ResultSummary:
    """Validate meta.yml file.

    Could also validate that the values are correct by comparing with the
    images

    Args:
        filename:
        path:
        require_page_data:

    Yields: Error messages

    """
    finder = FindErrorsMetadata(filename, path, require_page_data)
    return finder.find_errors()


def find_errors_ocr(path: str) -> result.ResultSummary:
    """Validate all xml files located in the given path.

        Make sure they are valid to the alto scheme

    Args:
        path: Path to find the alto xml files

    Returns:
        returns a ResultSummary of all the errors found in the alto ocr file.

    """

    def ocr_filter(entry: 'os.DirEntry[str]') -> bool:
        if not entry.is_file():
            return False

        base, ext = os.path.splitext(entry.name)
        if ext.lower() != ".xml":
            return False
        if base.lower() == "marc":
            return False

        return True

    logger = logging.getLogger(__name__)
    alto_scheme = etree.XMLSchema(
        etree.XML(
            files(hathi_xsd).joinpath("alto.xsd").read_bytes()
        )
    )

    summary_builder = result.SummaryDirector(source=path)
    for xml_file in filter(ocr_filter, os.scandir(path)):
        try:
            with open(xml_file.path, "r") as file_handle:
                doc = etree.fromstring(file_handle.read().encode("utf-8"))

            if not alto_scheme.validate(doc):
                summary_builder.add_error(
                    "{} does not validate to ALTO scheme".format(xml_file.name)
                )
            else:
                logger.info(
                    "%s validates to the ALTO XML scheme", xml_file.name
                )

        except FileNotFoundError:
            summary_builder.add_error("File missing")
        except etree.XMLSyntaxError as error:
            summary_builder.add_error("Syntax error: {}".format(error))
    return summary_builder.construct()


def run_validations(validators: typing.List[validator.AbsValidator]) \
        -> List[result.Result]:
    """Run validations."""
    errors = []
    for tester in validators:
        tester.validate()
        for error in tester.results:
            errors.append(error)

    return errors


def run_validation(validation_test: validator.AbsValidator) \
        -> List[result.Result]:
    """Run validation."""
    validation_test.validate()
    return validation_test.results


def find_non_utf8_characters(file_path: str) -> result.ResultSummary:
    """Locate any non utf-8 characters in a file."""
    result_builder = result.SummaryDirector(source=file_path)
    with open(file_path, "rb") as file_handle:

        for line_num, line in enumerate(file_handle):
            try:
                line.decode("utf-8", errors="strict")
            except UnicodeDecodeError as error:
                result_builder.add_error(
                    f"Line {line_num + 1} contains illegal characters. "
                    f"Details: {error}"
                )

    return result_builder.construct()
