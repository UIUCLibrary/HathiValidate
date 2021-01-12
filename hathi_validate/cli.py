import logging
import argparse

import sys

import os

from hathi_validate import package, process, configure_logging, report, validator, manifest

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore


def get_parser():
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
    parser.add_argument("--save-report", dest="report_name", help="Save report to a file")
    debug_group = parser.add_argument_group("Debug")
    debug_group.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")
    debug_group.add_argument("--log-debug", dest="log_debug", help="Save debug information to a file")
    return parser


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    parser = get_parser()
    args = parser.parse_args()

    configure_logging.configure_logger(debug_mode=args.debug, log_file=args.log_debug)
    errors = []
    batch_manifest_builder = manifest.PackageManifestDirector()
    for pkg in package.get_dirs(args.path):
        logger.info("Creating a manifest for {}".format(pkg))
        package_builder = batch_manifest_builder.add_package(pkg)

        for root, dirs, files in os.walk(pkg):
            for file_name in files:
                package_builder.add_file(file_name)

        logger.info("Checking {}".format(pkg))

        # Validate missing files
        logger.debug("Looking for missing package files in {}".format(pkg))
        missing_files_errors = process.run_validation(validator.ValidateMissingFiles(path=pkg))
        if not missing_files_errors:
            logger.info("Found no missing package files in {}".format(pkg))
        else:
            for error in missing_files_errors:
                logger.info(error.message)
                errors.append(error)

        # Look for missing components
        extensions = [".txt", ".jp2"]
        if args.check_ocr:
            extensions.append(".xml")
        logger.debug("Looking for missing component files in {}".format(pkg))
        missing_files_errors = process.run_validation(validator.ValidateComponents(pkg, "^\d{8}$", *extensions))
        if not missing_files_errors:
            logger.info("Found no missing component files in {}".format(pkg))
        else:
            for error in missing_files_errors:
                logger.info(error.message)
                errors.append(error)
        # exit()
        # Validate extra subdirectories
        logger.debug("Looking for extra subdirectories in {}".format(pkg))
        extra_subdirectories_errors = process.run_validation(validator.ValidateExtraSubdirectories(path=pkg))
        if not extra_subdirectories_errors:
            pass
        else:
            for error in extra_subdirectories_errors:
                errors.append(error)

        # Validate Checksums
        checksum_report = os.path.join(pkg, "checksum.md5")
        checksum_report_errors = process.run_validation(validator.ValidateChecksumReport(pkg, checksum_report))
        if not checksum_report_errors:
            logger.info("All checksums in {} successfully validated".format(checksum_report))
        else:
            for error in checksum_report_errors:
                errors.append(error)

        # Validate Marc
        marc_file=os.path.join(pkg, "marc.xml")
        marc_errors = process.run_validation(validator.ValidateMarc(marc_file))
        if not marc_errors:
            logger.info("{} successfully validated".format(marc_file))
        else:
            for error in marc_errors:
                errors.append(error)

        # Validate YML
        yml_file = os.path.join(pkg, "meta.yml")
        meta_yml_errors = process.run_validation(validator.ValidateMetaYML(yaml_file=yml_file, path=pkg, required_page_data=True))
        if not meta_yml_errors:
            logger.info("{} successfully validated".format(yml_file))
        else:
            for error in meta_yml_errors:
                errors.append(error)
        #

        # Validate ocr files
        if args.check_ocr:
            ocr_errors = process.run_validation(validator.ValidateOCRFiles(path=pkg))
            if not ocr_errors:
                logger.info("No validation errors found in ".format(pkg))
            else:
                for error in ocr_errors:
                    errors.append(error)

    batch_manifest = batch_manifest_builder.build_manifest()
    manifest_report = manifest.get_report_as_str(batch_manifest, width=80)
    console_reporter2 = report.Reporter(report.ConsoleReporter())
    validation_report = report.get_report_as_str(errors)
    console_reporter2.report(manifest_report)
    console_reporter2.report(validation_report)
    if args.report_name:
        file_reporter = report.Reporter(report.FileOutputReporter(args.report_name))
        file_reporter.report(validation_report)

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        import pytest  # type: ignore

        sys.exit(pytest.main(sys.argv[2:]))
    else:
        main()
