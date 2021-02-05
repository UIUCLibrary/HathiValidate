import argparse
import logging
import sys
from unittest.mock import Mock

from hathi_validate import cli


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
    # assert output_log.exists()

    print(report_generator.validation_report)
    print(report_generator.manifest_report)

    sample_dir.remove()