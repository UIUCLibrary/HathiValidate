import abc
import typing
from typing import Iterator
import itertools
import sys
import logging
import warnings

from . import result


def _split_text_line_by_words(text: str, max_len: int) -> Iterator[str]:
    words = text.split()
    line = ""
    while words:
        word = words.pop(0)
        #  If the word is longer than the width, split up the word
        if len(word) > max_len:
            args = [iter(word)] * max_len
            for ch in itertools.zip_longest(*args, fillvalue=""):
                yield "".join(ch)
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
    bullet = "* "
    for i, line in \
            enumerate(_split_text_line_by_words(message, width - len(bullet))):

        if i == 0:
            yield "{}{}".format(bullet, line)
        else:
            yield "{}{}".format(" " * len(bullet), line)


def get_report_as_str(results: typing.List[result.Result], width: int = 0) -> str:
    report_width = width if width > 0 else 80
    sorted_results = sorted(
        results, key=lambda r: r.source if r.source is not None else ""
    )
    grouped2 = []
    for k, v in itertools.groupby(sorted_results, key=lambda r: r.source):
        new_messages = []
        for new_message in v:
            new_messages.append(new_message)
        grouped2.append((k, new_messages))
    header = "Validation Results"
    main_spacer = "=" * report_width
    group_spacer = "-" * report_width
    warning_groups = []
    if len(grouped2) > 0:
        for source_group in grouped2:
            msg_list = []
            for msg in source_group[1]:
                # if width > 0:
                for line in make_point(msg.message, report_width):
                    msg_list.append(line)

            group_warnings = "\n".join(msg_list)

            warning_groups.append(
                "{}\n\n{}\n".format(source_group[0], group_warnings)
            )

        warnings = "\n{}\n".format(group_spacer).join(warning_groups)
    else:
        warnings = "No validation errors detected.\n"

    return f"{main_spacer}\n{header}\n{main_spacer}\n{warnings}{main_spacer}"


class AbsReport(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, results: typing.List[result.Result]) -> None:
        pass


class Report:
    def __init__(self, report_strategy: AbsReport) -> None:
        warnings.warn("Use reporter class instead", DeprecationWarning)
        self._strategy = report_strategy

    def generate(self, results: typing.List[result.Result]) -> None:
        self._strategy.generate(results)


class ConsoleReport(AbsReport):
    def __init__(self, file=sys.stdout) -> None:
        self.file = file

    def generate(self, results: typing.List[result.Result]) -> None:
        sorted_results = sorted(
            results, key=lambda r: r.source if r.source is not None else ""
        )
        grouped = itertools.groupby(sorted_results, key=lambda r: r.source)
        print("\nValidation Results:")
        print("===================")
        for source_group in grouped:
            print("\n{}".format(source_group[0]), file=self.file)
            for i, res in enumerate(source_group[1]):
                print("{}: {}".format(i + 1, res.message))
        print("===================")


class LogReport(AbsReport):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def generate(self, results: typing.List[result.Result]) -> None:
        sorted_results = sorted(
            results, key=lambda r: r.source if r.source is not None else ""
        )
        grouped = itertools.groupby(sorted_results, key=lambda r: r.source)
        top = "Validation Results"
        brace = "==================="

        group_errors_messages = []
        for source_group in grouped:
            group_errors = []
            for i, res in enumerate(source_group[1]):
                line = "{}: {}".format(i + 1, res.message)
                group_errors.append(line)
            group_errors_messages.append(
                ">{}\n{}".format(source_group[0], "\n".join(group_errors))
            )

        summery = \
            "{}\n{}\n{}".format(top, brace, "\n".join(group_errors_messages))

        # print("==============")
        self.logger.info(summery)


class TextReport(AbsReport):
    def __init__(self, file: str):
        self.file = file

    def generate(self, results: typing.List[result.Result]) -> None:
        sorted_results = sorted(
            results, key=lambda r: r.source if r.source is not None else ""
        )
        grouped = itertools.groupby(sorted_results, key=lambda r: r.source)
        with open(self.file, "w", encoding="utf8") as w:
            w.write("Validation Results\n\n")
            for source_group in grouped:
                w.write("\n{}\n".format(source_group[0]))
                for res in source_group[1]:
                    w.write("{}\n".format(res.message))


class AbsReporter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def report(self, report: str) -> None:
        pass


class Reporter:
    def __init__(self, reporter_strategy: AbsReporter) -> None:
        self._strategy = reporter_strategy

    def report(self, report: str) -> None:
        self._strategy.report(report)


class ConsoleReporter(AbsReporter):
    def __init__(self, file=sys.stdout) -> None:
        self.file = file

    def report(self, report: str) -> None:
        print("\n\n{}".format(report), file=self.file)


class FileOutputReporter(AbsReporter):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def report(self, report: str) -> None:
        with open(self.filename, "w", encoding="utf8") as w:
            w.write("{}\n".format(report))


class LogReporter(AbsReporter):
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def report(self, report: str) -> None:
        self.logger.info("\n{}".format(report))
