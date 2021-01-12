import argparse
from unittest.mock import Mock

from hathi_validate import cli


def test_version_exits_after_being_called(monkeypatch):

    parser = cli.get_parser()
    version_exit_mock = Mock()

    with monkeypatch.context() as m:
        m.setattr(argparse.ArgumentParser, "exit", version_exit_mock)
        parser.parse_args(["--version"])

    version_exit_mock.assert_called()
