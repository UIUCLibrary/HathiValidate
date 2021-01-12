import argparse
import logging
import os
import threading

from script_gui import SimpleGui, AbsScript # type: ignore
from script_gui.script_signals import SignalTypes # type: ignore
from hathi_validate import package, process, configure_logging, report
import hathi_validate
from PyQt5 import QtWidgets  # type: ignore


def Ω():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version=hathi_validate.__version__)
    parser.add_argument("path", nargs="?", help="Path to the hathipackages")
    parser.add_argument("--save-report", dest="report_name", help="Save report to a file")
    debug_group = parser.add_argument_group("Debug")
    debug_group.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")
    debug_group.add_argument("--log-debug", dest="log_debug", help="Save debug information to a file")
    parser.add_argument("--gui", action='store_true', help="Experimental gui")
    return parser


class SimpleGui2(SimpleGui):

    def accept_experimental(self):
        warning_message = """The graphical version is currently experimental. 
        
Are you sure you want to continue?
        """

        reply = QtWidgets.QMessageBox.question(self, "Warning: Experimental Feature", warning_message,
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            return True
        elif reply == QtWidgets.QMessageBox.No:
            return False
        else:
            raise Exception("Invalid response")

class HathiValidateScript(AbsScript):
    def _script(self):
        errors = []
        path = self.args["Path"].value
        for i, pkg in enumerate(package.get_dirs(path)):
            if self._abort_flag.is_set():
                self.logger.warning("Aborted")
                self.announce(SignalTypes.FAILED, "Script was aborted")
                break
            self.logger.info("{}) Checking {}".format(i + 1, pkg))
            errors += process.process_directory(pkg)
        else:
            self.logger.info("Checking Finished")

            # report_str = report.get_report_as_str(errors)
            self.announce(SignalTypes.SUCCESS, report.get_report_as_str(errors, 37))
            console_reporter = report.Reporter(report.LogReporter(self.logger))
            console_reporter.report(report.get_report_as_str(errors, width=80))

    def run(self):
        self._script()

    def __init__(self, cli_args, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = logger
        default_path = cli_args.path if cli_args.path else ""
        self.args.add_required(name="Path", default=default_path, help="Path to the Hathi Packages",
                               validate=lambda user_input: os.path.isdir(user_input))

    @property
    def title(self) -> str:
        return hathi_validate.FULL_TITLE

    def start(self):
        self.t = threading.Thread(target=self._script, daemon=True)
        self.t.start()


def main():
    parser = get_parser()
    args = parser.parse_args()

    logger = configure_logging.configure_logger(debug_mode=args.debug, log_file=args.log_debug)

    script = HathiValidateScript(args, logger=logger)
    app = SimpleGui2(script)
    if args.debug or app.accept_experimental():
        app.load_logger(debug=args.debug)
        app.display()
    else:
        print("Exit")


if __name__ == '__main__':
    main()
