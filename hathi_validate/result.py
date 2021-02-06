import abc
import typing
from typing import Optional, List
import collections.abc


class Result:
    def __init__(self, result_type: str) -> None:
        self.result_type: str = result_type
        self.source: Optional[str] = None
        self.message: str = ""

    def __str__(self) -> str:
        if self.source:
            message = '{}: "{}"'.format(self.source, self.message)
        else:
            message = '"{}"'.format(self.message)
        return "{}[{}]{}".format(Result.__name__, self.result_type, message)


class ResultSummary(collections.abc.Iterable):  # type: ignore
    def __init__(self) -> None:
        self.results: List[Result] = []
        self.source: Optional[str] = None

    def __iadd__(self, other: Result):
        self.results.append(other)
        return self

    def __iter__(self) -> typing.Iterator[Result]:
        return self.results.__iter__()

    def __len__(self) -> int:
        return len(self.results)

    def __contains__(self, x: Result) -> bool:
        return x in self.results


class AbsResultBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_new_summary(self) -> None:
        pass

    @abc.abstractmethod
    def add_result(self, result: Result) -> None:
        pass

    @abc.abstractmethod
    def get_summary(self) -> ResultSummary:
        pass

    @abc.abstractmethod
    def set_source(self, source: str) -> None:
        pass


class ResultSummaryBuilder(AbsResultBuilder):
    def __init__(self) -> None:
        self.summary: Optional[ResultSummary] = None
        self.source: Optional[str] = None

    def create_new_summary(self) -> None:
        self.summary = ResultSummary()

    def add_result(self, result: Result) -> None:
        if self.summary is None:
            raise RuntimeError("Summary has not been set")

        self.summary += result

    def get_summary(self) -> ResultSummary:
        if self.summary is None:
            raise RuntimeError("Summary has not been set")

        return self.summary

    def set_source(self, source: str) -> None:
        self.source = source


class SummaryDirector:
    def __init__(self, source: str) -> None:
        self.builder = ResultSummaryBuilder()
        self.builder.create_new_summary()
        self.builder.source = source

    def add_error(self, message: str) -> None:
        new_error = Result("error")
        new_error.message = message
        new_error.source = self.builder.source
        self.builder.add_result(new_error)

    def construct(self) -> ResultSummary:
        return self.builder.get_summary()
