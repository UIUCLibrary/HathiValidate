# Original VB CODE:
#
# SetText(lblStatus, folderName)
#
# If Form1.stopping = True Then Exit Sub
#
# 'get base object name which is the folder name
# Dim baseName As String = Path.GetFileName(folderName)
# SetText(txtStatus, String.Format("Object ID: {0}", baseName))
#
# Dim m As Match = Regex.Match(baseName, ObjectIdRegex)
# If m.Success = False Then
#   SetText(txtStatus, String.Format("   ERROR: Base folder name '{0}' does not match naming conventions for ObjectIDs ", baseName))
# Else
#   SetText(txtStatus, String.Format("   OK: Base folder name '{0}' is a valid ObjectID ", baseName))
# End If
#
#
# SetText(txtStatus, New String("-", 20))
# SetText(txtStatus, "   Checking for expected root files and folders:")
# 'check whether expected files exist
# CheckFileExists(folderName, "checksum.md5")
# CheckFileExists(folderName, "marc.xml")
# CheckFileExists(folderName, "meta.yml")
#
# 'make sure folder does not contain any subfolders
# Dim subfolders() As String = Directory.GetDirectories(folderName)
# If subfolders.Count > 0 Then
#   SetText(txtStatus, String.Format("      ERROR: The base folder '{0}' contains subfolders. ", baseName))
# Else
#   SetText(txtStatus, String.Format("      OK: The base folder '{0}' has no subfolders", baseName))
# End If
#
#
# 'validate that the checksums in the *.fil file match
# SetText(txtStatus, New String("-", 20))
# SetText(txtStatus, "   Validating Checksum File 'checksum.md5'")
# CheckChecksums(folderName)
#
# 'validate that the MARC file is valid
# SetText(txtStatus, New String("-", 20))
# SetText(txtStatus, "   Validating MARC XML File 'marc.xml'")
#
# Dim xmlSet As New XmlReaderSettings()
# xmlSet.CheckCharacters = True
# xmlSet.ConformanceLevel = ConformanceLevel.Document
# xmlSet.Schemas.Add("http://www.loc.gov/MARC21/slim", "http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd")
# xmlSet.ValidationFlags = XmlSchemaValidationFlags.ProcessIdentityConstraints Or XmlSchemaValidationFlags.ProcessSchemaLocation Or XmlSchemaValidationFlags.ReportValidationWarnings
#
# xmlSet.ValidationType = ValidationType.Schema
#
# CheckXML(folderName, "marc.xml", xmlSet)
#
# 'validate other xml files, currently ALTO
# SetText(txtStatus, New String("-", 20))
# SetText(txtStatus, String.Format("   Validating all other XML files"))
#
# xmlSet.Schemas.Add("http://www.loc.gov/standards/alto/ns-v2#", "http://www.loc.gov/standards/alto/alto.xsd")
# xmlSet.Schemas.Add("http://www.w3.org/1999/xlink", "http://www.loc.gov/standards/xlink/xlink.xsd")
#
# Dim allXML() As String = Directory.GetFiles(folderName, "*.xml")
#
# For Each xfile In allXML
#   If Path.GetFileName(xfile).ToLower <> "marc.xml" Then
#     SetText(txtStatus, String.Format("   Validating XML file '{0}'", Path.GetFileName(xfile)))
#     CheckXML(xfile, xmlSet)
#   End If
#   Application.DoEvents()
# Next
#
# 'Validate that the meta.yml file is valid; could also validate that the values are correct by comparing with the images
# SetText(txtStatus, New String("-", 20))
# SetText(txtStatus, "   Validating 'meta.yml' file")
# CheckYaml(folderName)
#
# Application.DoEvents()

import datetime
import hashlib
import logging
import os

import itertools
import yaml
from lxml import etree

from hathi_validate import result
from hathi_validate import xml_schemes
import re

DIRECTORY_REGEX = "^\d+(p\d+(_\d+)?)?(v\d+(_\d+)?)?(i\d+(_\d+)?)?(m\d+(_\d+)?)?$"
DATE_REGEX = re.compile("^(\d{4})-(\d{2})-(\d{2})T(\d{2})\:(\d{2})(\:\d{2})?-(\d{2}):(\d{2})$")


class ValidationError(Exception):
    pass


class InvalidChecksum(ValidationError):
    pass


#
# def load_validation(filename="hathi_validate/MARC21slim.xsd"):
#     def read_file():
#         with open(filename) as f:
#             for line in f:
#                 yield line.strip()
#
#     return "".join(read_file())

# XSD = load_validation()


def find_missing_files(path: str) -> result.ResultSummary:
    """
        check for expected files exist on the path
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


def find_extra_subdirectory(path) -> result.ResultSummary:
    """
        Check path for any subdirectories
    Args:
        path:

    Yields: Any subdirectory

    """
    summary_builder = result.SummaryDirector(source=path)
    for item in os.scandir(path):
        if item.is_dir():
            summary_builder.add_error("Extra subdirectory {}".format(item.name))
    return summary_builder.construct()


def parse_checksum(line):
    chunks = line.strip().split(" ")
    md5_hash = chunks[0]
    raw_filename = chunks[-1]
    if len(md5_hash) != 32:
        raise InvalidChecksum("Invalid Checksum")
    if raw_filename[0] == "*":  # For file names listed with an asterisk before them in the checksum file
        filename = raw_filename[1:]
    else:
        filename = raw_filename
    return md5_hash, filename


def calculate_md5(filename, chunk_size=8192):
    md5 = hashlib.md5()

    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()


def is_same_hash(*hashes) -> bool:
    for hash_value_a, hash_value_b, in itertools.combinations(hashes, 2):
        if hash_value_a.lower() != hash_value_b.lower():
            return False
    return True


def find_failing_checksums(path, report) -> result.ResultSummary:
    """
        validate that the checksums in the *.fil file match

    Args:
        path:
        report:

    Returns:

    """

    logger = logging.getLogger(__name__)
    report_builder = result.SummaryDirector(source=path)
    try:
        for report_md5_hash, filename in extracts_checksums(report):
            logger.debug("Calculating the md5 checksum hash for {}".format(filename))
            file_path = os.path.join(path, filename)
            try:
                file_md5_hash = calculate_md5(filename=file_path)
                if not is_same_hash(file_md5_hash, report_md5_hash):
                    logger.debug('Hash mismatch for "{}". (Actual ({}): expected ({}))'.format(file_path, file_md5_hash,
                                                                                               report_md5_hash))
                    report_builder.add_error(
                        "Checksum listed in \"{}\" doesn't match for \"{}\"".format(os.path.basename(report), filename))
                else:
                    logger.info("{} successfully matches md5 hash in {}".format(filename, os.path.basename(report)))
            except FileNotFoundError as e:
                logger.info("Unable to run checksum for missing file, {}".format(filename))
                report_builder.add_error("Unable to run checksum for missing file, {}".format(filename))
    except FileNotFoundError as e:
        report_builder.add_error("File missing")
    return report_builder.construct()


def extracts_checksums(report):
    with open(report, "r") as f:
        for line in f:
            md5, filename = parse_checksum(line)
            yield md5, filename


def find_errors_marc(filename) -> result.ResultSummary:
    """
    Validate the MARC file

    Args:
        filename:

    Returns:

    """
    summary_builder = result.SummaryDirector(source=filename)

    xsd = etree.XML(xml_schemes.MARC_XSD)  # type: ignore
    scheme = etree.XMLSchema(xsd)
    try:
        with open(filename, "r", encoding="utf8") as f:
            raw_data = f.read()
        doc = etree.fromstring(raw_data)
        if not scheme.validate(doc):  # type: ignore
            summary_builder.add_error("Unable to validate")
    except FileNotFoundError:
        summary_builder.add_error("File missing")
    except etree.XMLSyntaxError as e:
        summary_builder.add_error("Syntax error: {}".format(e))
    return summary_builder.construct()


def parse_yaml(filename):
    with open(filename, "r") as f:
        data = yaml.load(f)
        return data


def find_errors_meta(filename, path):
    """
    Validate meta.yml file
    could also validate that the values are correct by comparing with the images

    Args:
        filename:

    Yields: Error messages

    """

    def find_pagedata_errors(metadata):
        pages = metadata["pagedata"]
        for image_name, attributes in pages.items():
            if not os.path.exists(os.path.join(path, image_name)):
                yield "The pagedata {} contains an nonexistent file {}".format(filename, image_name)
            if attributes:
                pass

    def find_capture_date_errors(metadata):
        capture_date = metadata["capture_date"]

        if not isinstance(capture_date, datetime.datetime):
            if isinstance(capture_date, str):
                # Just because the parser wasn't able to convert into a datetime object doesn't mean it's not valid per se.
                # It can also be a matched to a regex.
                if DATE_REGEX.fullmatch(capture_date) is None:
                    yield "Invalid YAML capture_date {}".format(capture_date)
            else:
                yield "Invalid YAML data type for in capture_date"

    def find_capture_agent_errors(metadata):
        capture_agent = metadata["capture_agent"]
        if not isinstance(capture_agent, str):
            yield "Invalid YAML capture_agent: {}".format(capture_agent)

    summary_builder = result.SummaryDirector(source=filename)
    try:
        yml_metadata = parse_yaml(filename=filename)

        try:
            for error in find_capture_date_errors(yml_metadata):
                summary_builder.add_error(error)
            for error in find_capture_agent_errors(yml_metadata):
                summary_builder.add_error(error)
            for error in find_pagedata_errors(yml_metadata):
                summary_builder.add_error(error)
        except KeyError as e:
            summary_builder.add_error("{} is missing key, {}".format(filename, e))
    except yaml.YAMLError as e:
        summary_builder.add_error("Unable to read {}. Reason:{}".format(filename, e))
    except FileNotFoundError as e:
        summary_builder.add_error("Missing {}".format(e))
    return summary_builder.construct()


def process_directory(path: str):
    # TODO validate directory name
    logger = logging.getLogger(__name__)

    # Validate missing files
    logger.debug("Looking for missing files in {}".format(path))
    missing_errors = []
    for missing_file in find_missing_files(path):
        print(missing_file)
        missing_errors.append(missing_file)
    else:
        logger.info("Found no missing files in {}".format(path))

    logger.debug("Looking for extra subdirectories in {}".format(path))

    extra_subdirectory_errors = []
    for extra_subdirectory in find_extra_subdirectory(path=path):
        print(extra_subdirectory.message)
        extra_subdirectory_errors.append(extra_subdirectory)
    else:
        logger.info("Found no extra subdirectories in {}".format(path))

    # Validate checksum
    checksum_report = os.path.join(path, "checksum.md5")
    logger.info("Validating checksums in {}".format(checksum_report))
    checksum_errors = []
    for failing_checksum in find_failing_checksums(path=path, report=checksum_report):
        print(failing_checksum.message)
        checksum_errors.append(failing_checksum)

    # Validate MARC
    marc_file = os.path.join(path, "marc.xml")
    logger.info("Validating {}".format(marc_file))
    marc_errors = []
    for error in find_errors_marc(filename=marc_file):
        marc_errors.append(error)
    else:
        logger.info("{} successfully validated".format(marc_file))

    # TODO: validate other xml files, currently ALTO
    yml_file = os.path.join(path, "meta.yml")
    logger.info("Validating {}".format(yml_file))
    yml_errors = []
    for error in find_errors_meta(filename=yml_file, path=path):
        print(error.message)
        yml_errors.append(error)
    else:
        logger.info("{} successfully validated".format(yml_file))

    return yml_errors + marc_errors + checksum_errors + extra_subdirectory_errors + missing_errors
