import argparse
import logging
import sys
from unittest.mock import Mock, MagicMock

import pytest

from hathi_validate import cli, process


def test_version_exits_after_being_called(monkeypatch):

    parser = cli.get_parser()
    version_exit_mock = Mock()

    with monkeypatch.context() as m:
        m.setattr(argparse.ArgumentParser, "exit", version_exit_mock)
        parser.parse_args(["--version"])

    version_exit_mock.assert_called()


def test_main_version_exists(monkeypatch):
    version_exit_mock = Mock()

    with monkeypatch.context() as m:
        m.setattr(sys, "exit", version_exit_mock)
        m.setattr(cli.ReportGenerator, "generate_report", Mock())
        cli.main(["--version"])

    version_exit_mock.assert_called()


def test_generate_report(tmpdir):
    temp_output = tmpdir / "output"
    temp_output.ensure_dir()

    output_log = temp_output / "log.txt"
    sample_dir = tmpdir / "mysample"
    sample_dir.ensure_dir()
    for sample_package_folder_name in [f"{str(x).zfill(8)}" for x in range(20)]:
        sample_package_folder = (sample_dir / sample_package_folder_name).ensure_dir()
        for f in range(4):
            test_file = sample_package_folder / f"{str(f).zfill(8)}.jp2"
            test_file.ensure()

    logger = logging.getLogger(__name__)
    args = argparse.Namespace(
        path=sample_dir.strpath,
        report_name=output_log.strpath,
        check_ocr=False
    )

    report_generator = cli.ReportGenerator(
        args=args,
        logger=logger
    )

    report_generator.generate_report()

    assert \
        isinstance(report_generator.validation_report, str) and \
        isinstance(report_generator.manifest_report, str)


def test_validate_missing_components_includes_xml_with_ocr_option():
    mylogger = Mock()
    args = argparse.Namespace(check_ocr=True)
    validator = cli.ValidateMissingComponents(
        args=args,
        logger=mylogger
    )
    assert ".xml" in validator.extensions


validations = [
    (cli.ValidateYAML, "successfully validated"),
    (cli.ValidateMissingComponents, "Found no missing component files"),
    (cli.ValidateMissingFiles, "Found no missing package files"),
    (cli.ValidateChecksums, "successfully validated"),
    (cli.ValidateMarc, "successfully validated"),
    (cli.ValidateOcrFiles, "No validation errors found in"),
]


@pytest.mark.parametrize("validator_type,included_message", validations)
def test_validate_success_message(validator_type,included_message, monkeypatch):
    mylogger = MagicMock()
    args = argparse.Namespace(check_ocr=True)
    validator = validator_type(
        args=args,
        logger=mylogger
    )

    def mock_errors(*args, **kwargs):
        return []

    monkeypatch.setattr(process, "run_validation", mock_errors)
    validator.get_errors("123")
    assert mylogger.info.called is True
    assert included_message in mylogger.info.call_args.args[0]
