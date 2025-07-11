"""Report generations tools."""

import abc
from typing import Iterator, IO, List, Generator
import itertools
import sys
import logging

from hathi_validate import result


def _split_text_line_by_words(
        text: str,
        max_len: int
) -> Generator[str, None, None]:

    words = text.split()
    line = ""
    while words:
        word = words.pop(0)
        #  If the word is longer than the width, split up the word
        if len(word) > max_len:
            args = [iter(word)] * max_len
            for chunk in itertools.zip_longest(*args, fillvalue=""):
                yield "".join(chunk)
            continue
        # otherwise split it up
        potential_line = "{} {}".format(line, word).strip()
        if len(potential_line) > max_len:
            words.insert(0, word)
            yield line
            line = ""
        else:
            line = potential_line

    yield line


def make_point(message: str, width: int) -> Iterator[str]:
    """Generate a bullet-point list.

    Args:
        message:
        width: Column width

    Yields:
        Yields a new bullet-pointed line containing the message

    """
    bullet = "* "
    for i, line in \
            enumerate(_split_text_line_by_words(message, width - len(bullet))):

        if i == 0:
            yield "{}{}".format(bullet, line)
        else:
            yield "{}{}".format(" " * len(bullet), line)


class ReportStringBuilder:
    """Builder for creating a string report."""

    def __init__(self, results: List[result.Result]) -> None:
        """Create a new String ReportStringBuilder object.

        Args:
            results: Results of a validation
        """
        self.results = results
        self.header = "Validation Results"

    def build_string(self, width: int = 0) -> str:
        """Create a new report as a string.

        Args:
            width: length of each line in the report

        Returns:
            Returns a multiline string based on the results given

        """
        report_width = width if width > 0 else 80

        sorted_results = sorted(
            self.results,
            key=lambda r: r.source if r.source is not None else ""
        )

        grouped_results = []
        for key, value in itertools.groupby(
                sorted_results, key=lambda r: r.source):

            grouped_results.append((key, list(value)))

        warnings_section = self.get_warnings_section(grouped_results,
                                                     report_width)

        main_spacer = "=" * report_width
        return f"{main_spacer}\n" \
               f"{self.header}\n" \
               f"{main_spacer}\n" \
               f"{warnings_section}" \
               f"{main_spacer}"

    def get_warnings_section(self, grouped_results, report_width: int) -> str:
        """Generate the section of the report containing the warnings.

        Args:
            grouped_results:
            report_width:
                Width of each line before a new line character is added.

        Returns:
            Returns the generated warnings section of the report as a string

        """
        group_spacer = "-" * report_width
        if len(grouped_results) == 0:
            return "No validation errors detected.\n"

        warning_groups = []
        for group_name, source_group in grouped_results:
            warning_message = \
                self.build_warning_message(
                    group_name,
                    source_group,
                    report_width
                )
            warning_groups.append(warning_message)

        return "\n{}\n".format(group_spacer).join(warning_groups)

    @staticmethod
    def build_warning_message(group_name: str,
                              source_group: List[result.Result],
                              report_width: int) -> str:
        """Build the warning message for each result provided.

        Args:
            group_name:
            source_group:
            report_width:
                Width of each line before a new line character is added.

        Returns:
            Returns a new warning message based on the results.

        """
        msg_list = []
        for msg in source_group:
            # if width > 0:
            for line in make_point(msg.message, report_width):
                msg_list.append(line)
        group_warnings = "\n".join(msg_list)
        return "{}\n\n{}\n".format(group_name, group_warnings)


def get_report_as_str(results: List[result.Result], width: int = 0) -> str:
    """Generate a new report string from the results given.

    Args:
        results: results to generate a report from
        width: Width of each line in the Report.

    Returns:
        Returns a new multiline report as a string

    """
    builder = ReportStringBuilder(results)
    return builder.build_string(width)


class AbsReporter(metaclass=abc.ABCMeta):
    """Base class for reporter."""

    @abc.abstractmethod
    def report(self, report: str) -> None:
        """Send report."""


class Reporter:
    """Reporter strategy context."""

    def __init__(self, reporter_strategy: AbsReporter) -> None:
        """Create a new strategy context object.

        Args:
            reporter_strategy: Strategy for reporting the data.
        """
        self._strategy = reporter_strategy

    def report(self, report: str) -> None:
        """Report the report.

        Args:
            report:

        """
        self._strategy.report(report)


class ConsoleReporter(AbsReporter):
    """Report to console."""

    def __init__(self, file: IO[str] = sys.stdout) -> None:
        """Create a new reporter object.

        Args:
            file: such as stderr or stdout

        """
        self.file = file

    def report(self, report: str) -> None:
        """Report the report.

        Args:
            report:

        """
        print("\n\n{}".format(report), file=self.file)


class FileOutputReporter(AbsReporter):
    """Report to file."""

    def __init__(self, filename: str) -> None:
        """Create a new reporter object.

        Args:
            filename: path to a file to save to

        """
        self.filename = filename

    def report(self, report: str) -> None:
        """Report the report.

        Args:
            report:

        """
        with open(self.filename, "w", encoding="utf8") as write_file:
            write_file.write("{}\n".format(report))


class LogReporter(AbsReporter):
    """Report to Python logger."""

    def __init__(self, logger: logging.Logger) -> None:
        """Create a new reporter object.

        Args:
            logger: Python logger

        """
        self.logger = logger

    def report(self, report: str) -> None:
        """Report the report.

        Args:
            report: message to report

        """
        self.logger.info("\n{}".format(report))
