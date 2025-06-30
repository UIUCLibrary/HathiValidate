"""Command line interface."""

import logging
import argparse

import abc
from importlib import metadata
import sys
import os
from typing import List, Optional

from hathi_validate import package, process, configure_logging, report, \
    validator, manifest, result


def get_parser() -> argparse.ArgumentParser:
    """Get argument parser."""
    parser = argparse.ArgumentParser()
    try:
        version = metadata.version("hathiValidate")
    except metadata.PackageNotFoundError:
        version = "dev"
    parser.add_argument(
        '--version',
        action='version',
        version=version
    )
    parser.add_argument("path", help="Path to the hathipackages")
    parser.add_argument("--check_ocr",
                        action="store_true",
                        help="Check for ocr xml files"
                        )

    parser.add_argument(
        "--save-report",
        type=str,
        dest="report_name",
        help="Save report to a file"
    )

    debug_group = parser.add_argument_group("Debug")

    debug_group.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")

    debug_group.add_argument(
        "--log-debug",
        dest="log_debug",
        help="Save debug information to a file"
    )

    return parser


def main(cli_args: Optional[List[str]] = None) -> None:
    """Start main entry point for command line interface."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    parser = get_parser()
    args = parser.parse_args(cli_args)

    configure_logging.configure_logger(debug_mode=args.debug,
                                       log_file=args.log_debug)

    report_generator = ReportGenerator(
        args=args,
        logger=logger
    )

    report_generator.generate_report()
    if report_generator.validation_report is not None and \
            report_generator.manifest_report is not None:
        console_reporter2 = report.Reporter(report.ConsoleReporter())
        console_reporter2.report(report_generator.manifest_report)
        console_reporter2.report(report_generator.validation_report)
        report_name = args.report_name
        if isinstance(report_name, str):
            file_reporter = report.Reporter(
                report.FileOutputReporter(report_name))
            file_reporter.report(report_generator.validation_report)


class AbsValidation(abc.ABC):
    """Base class for performing validations."""

    def __init__(self,
                 args: argparse.Namespace,
                 logger: logging.Logger) -> None:
        """Create a new validation object.

        Args:
            args:
            logger: Python logger.
        """
        super().__init__()
        self._args = args
        self.logger = logger

    @abc.abstractmethod
    def get_errors(self, pkg: str) -> List[result.Result]:
        """Get the results of the validations.

        Args:
            pkg: Path to the directory containing the files.

        Returns:
            Any errors found in the validation.

        """


class ValidateMissingComponents(AbsValidation):
    """Look for missing components."""

    def __init__(self,
                 args: argparse.Namespace,
                 logger: logging.Logger) -> None:
        """Create a new validation object.

        Args:
            args:
            logger: Python logger.
        """
        super().__init__(args, logger)
        self.extensions = [".txt", ".jp2"]
        if args.check_ocr:
            self.extensions.append(".xml")

    def get_errors(self, pkg: str) -> List[result.Result]:
        """Get the results of the validations.

        Args:
            pkg: Path to the directory containing the files.

        Returns:
            Any errors found in the validation.

        """
        self.logger.debug(
            "Looking for missing component files in {}".format(pkg))
        errors = process.run_validation(
            validator.ValidateComponents(pkg, r"^\d{8}$", *self.extensions))
        for error in errors:
            self.logger.info(error.message)
        if not errors:
            self.logger.info(
                "Found no missing component files in {}".format(pkg))
        return errors


class ValidateMissingFiles(AbsValidation):
    """Validate missing files."""

    def get_errors(self, pkg: str) -> List[result.Result]:
        """Get the results of the validations.

        Args:
            pkg: Path to the directory containing the files.

        Returns:
            Any errors found in the validation.

        """
        errors = []

        self.logger.debug("Looking for missing package files in %s", pkg)
        missing_files_errors = process.run_validation(
            validator.ValidateMissingFiles(path=pkg)
        )

        if not missing_files_errors:
            self.logger.info("Found no missing package files in %s", pkg)
        else:
            for error in missing_files_errors:
                self.logger.info(error.message)
                errors.append(error)
        return errors


class ValidateExtraSubdirectories(AbsValidation):
    """Validate extra subdirectories."""

    def get_errors(self, pkg: str) -> List[result.Result]:
        """Get the results of the validations.

        Args:
            pkg: Path to the directory containing the files.

        Returns:
            Any errors found in the validation.

        """
        errors = []
        self.logger.debug("Looking for extra subdirectories in {}".format(pkg))
        extra_subdirectories_errors = process.run_validation(
            validator.ValidateExtraSubdirectories(path=pkg))
        if extra_subdirectories_errors:
            for error in extra_subdirectories_errors:
                errors.append(error)
        return errors


class ValidateChecksums(AbsValidation):
    """Validate Checksums."""

    def get_errors(self, pkg: str) -> List[result.Result]:
        """Get the results of the validations.

        Args:
            pkg: Path to the directory containing the files.

        Returns:
            Any errors found in the validation.

        """
        errors = []
        checksum_report = os.path.join(pkg, "checksum.md5")
        checksum_report_errors = process.run_validation(
            validator.ValidateChecksumReport(pkg, checksum_report))
        if not checksum_report_errors:
            self.logger.info(
                "All checksums in {} successfully validated".format(
                    checksum_report))
        else:
            for error in checksum_report_errors:
                errors.append(error)
        return errors


class ValidateMarc(AbsValidation):
    """Validate Marc."""

    def get_errors(self, pkg: str) -> List[result.Result]:
        """Get the results of the validations.

        Args:
            pkg: Path to the directory containing the files.

        Returns:
            Any errors found in the validation.

        """
        errors = []
        marc_file = os.path.join(pkg, "marc.xml")
        marc_errors = process.run_validation(validator.ValidateMarc(marc_file))
        if not marc_errors:
            self.logger.info("{} successfully validated".format(marc_file))
        else:
            for error in marc_errors:
                errors.append(error)
        return errors


class ValidateYAML(AbsValidation):
    """Validate YML."""

    def get_errors(self, pkg: str) -> List[result.Result]:
        """Get the results of the validations.

        Args:
            pkg: Path to the directory containing the files.

        Returns:
            Any errors found in the validation.

        """
        errors = []
        yml_file = os.path.join(pkg, "meta.yml")
        meta_yml_errors = process.run_validation(
            validator.ValidateMetaYML(yaml_file=yml_file, path=pkg,
                                      required_page_data=True))
        if not meta_yml_errors:
            self.logger.info("{} successfully validated".format(yml_file))
        else:
            for error in meta_yml_errors:
                errors.append(error)
        return errors


class ValidateOcrFiles(AbsValidation):
    """Validate ocr files."""

    def get_errors(self, pkg: str) -> List[result.Result]:
        """Get the results of the validations.

        Args:
            pkg: Path to the directory containing the files.

        Returns:
            Any errors found in the validation.

        """
        errors = []
        if self._args.check_ocr:
            ocr_errors = process.run_validation(
                validator.ValidateOCRFiles(path=pkg))
            if not ocr_errors:
                self.logger.info("No validation errors found in %s", pkg)
            else:
                for error in ocr_errors:
                    errors.append(error)
        return errors


class ReportGenerator:
    """Create a report for cli."""

    def __init__(self,
                 args: argparse.Namespace,
                 logger: logging.Logger,
                 checks: Optional[List[AbsValidation]] = None) -> None:
        """Create a new report generator object.

        Args:
            args:
            logger:
            checks:
        """
        self._args = args
        self.logger = logger
        self.validation_report: Optional[str] = None
        self.manifest_report: Optional[str] = None
        self.checks: List[AbsValidation] = checks or [
            ValidateMissingFiles(args, logger),
            ValidateMissingComponents(args, logger),
            ValidateExtraSubdirectories(args, logger),
            ValidateChecksums(args, logger),
            ValidateMarc(args, logger),
            ValidateYAML(args, logger),
            ValidateOcrFiles(args, logger),
        ]

    def generate_report(self) -> None:
        """Output the report to stdout."""
        errors = []
        batch_manifest_builder = manifest.PackageManifestDirector()
        for pkg in package.get_dirs(self._args.path):
            self.logger.info("Creating a manifest for {}".format(pkg))
            package_builder = batch_manifest_builder.add_package(pkg)

            for _, __, files in os.walk(pkg):
                for file_name in files:
                    package_builder.add_file(file_name)

            self.logger.info("Checking {}".format(pkg))
            for validation in self.checks:
                errors += validation.get_errors(pkg)

        batch_manifest = batch_manifest_builder.build_manifest()

        self.manifest_report = manifest.get_report_as_str(
            batch_manifest, width=80
        )

        self.validation_report = report.get_report_as_str(errors)


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        import pytest  # type: ignore  # noqa

        sys.exit(pytest.main(sys.argv[2:]))
    else:
        main()
