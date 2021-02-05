import abc
import logging
import typing

import os

import re

from . import result
from . import process


class absValidator(metaclass=abc.ABCMeta):

    def __init__(self) -> None:
        self.results: typing.List[result.ResultSummary] = []

    @abc.abstractmethod
    def validate(self):
        pass


class ValidateMissingFiles(absValidator):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def validate(self):
        logger = logging.getLogger(__name__)
        logger.debug("Looking for missing files in {}".format(self.path))
        for missing_file in process.find_missing_files(self.path):
            self.results.append(missing_file)
        # super().validate(path, *args, **kwargs)


class ValidateComponents(absValidator):

    def __init__(self, path, component_regex, *extensions) -> None:
        """

        Args:
            path: Directory to find the files
            component_regex: A regular expression to identify the component
                names.
                Note: this regex should ignore the extension
            *extensions: All the extensions to check for a given component
        """
        super().__init__()
        self.path = path
        self.component_regex = component_regex
        self.extensions = extensions
        self._component_mask = re.compile(component_regex)

    def validate(self):
        components = set()
        found_files = False

        logger = logging.getLogger(__name__)
        report_builder = result.SummaryDirector(source=self.path)

        for component_file in filter(self._component_filter, os.scandir(self.path)):
            found_files = True
            components.add(os.path.splitext(component_file.name)[0])

        if not found_files:
            raise FileNotFoundError("No files found with regex {}".format(self.component_regex))

        for component in sorted(components):
            # print(component)
            for extension in self.extensions:
                component_file_name = f"{component}{extension}"
                component_file_path = os.path.join(self.path, component_file_name)
                if not os.path.exists(component_file_path):
                    report_builder.add_error("Missing {}".format(component_file_name))
                    logger.info("Missing {}".format(component_file_name))
        self.results = report_builder.construct()

    def _component_filter(self, entry: os.DirEntry):
        if not entry.is_file():
            return False

        base, ext = os.path.splitext(entry.name)
        if not self._component_mask.fullmatch(base):
            return False

        return True


class ValidateExtraSubdirectories(absValidator):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def validate(self):
        for extra_subdirectory in process.find_extra_subdirectory(self.path):
            self.results.append(extra_subdirectory)


class ValidateChecksumReport(absValidator):
    def __init__(self, path, checksum_report):
        super().__init__()
        self.path = path
        self.checksum_report = checksum_report

    def validate(self):
        for failing_checksum in process.find_failing_checksums(self.path, self.checksum_report):
            self.results.append(failing_checksum)


class ValidateMetaYML(absValidator):
    def __init__(self, yaml_file, path, required_page_data: bool) -> None:
        super().__init__()
        self.yaml_file = yaml_file
        self.path = path
        self.require_page_data = required_page_data

    def validate(self):
        for error in process.find_errors_meta(self.yaml_file, self.path, self.require_page_data):
            self.results.append(error)


class ValidateMarc(absValidator):
    def __init__(self, marc_file):
        super().__init__()
        self.marc_file = marc_file

    def validate(self):
        logger = logging.getLogger(__name__)
        logger.info("Validating {}".format(self.marc_file))
        for error in process.find_errors_marc(filename=self.marc_file):
            self.results.append(error)


class ValidateOCRFiles(absValidator):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def validate(self):
        for error in process.find_errors_ocr(path=self.path):
            self.results.append(error)


class ValidateUTF8Files(absValidator):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def validate(self):
        for error in process.find_non_utf8_characters(self.file_path):
            self.results.append(error)
