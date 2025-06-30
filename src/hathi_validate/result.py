"""Results of validations."""

import abc
import typing
from typing import Optional, List
import collections.abc


class Result:
    """Result of a validation."""

    def __init__(self, result_type: str) -> None:
        """Create a new result object.

        Result objects are not normally created directly.

        Args:
            result_type: Category of the result such as "error"

        """
        self.result_type: str = result_type
        self.source: Optional[str] = None
        self.message: str = ""

    def __str__(self) -> str:
        """Get validation string."""
        if self.source:
            message = '{}: "{}"'.format(self.source, self.message)
        else:
            message = '"{}"'.format(self.message)
        return "{}[{}]{}".format(Result.__name__, self.result_type, message)


class ResultSummary(collections.abc.Iterable):  # type: ignore
    """Result summary."""

    def __init__(self) -> None:
        """Create a new ResultSummary object."""
        self.results: List[Result] = []
        self.source: Optional[str] = None

    def __iadd__(self, other: Result) -> "ResultSummary":
        """Add a result to the summary."""
        self.results.append(other)
        return self

    def __iter__(self) -> typing.Iterator[Result]:
        """Iterate of the results."""
        return self.results.__iter__()

    def __len__(self) -> int:
        """Get the number of results included in the summary."""
        return len(self.results)

    def __contains__(self, item: Result) -> bool:
        """Check if existing Result is already included."""
        return item in self.results


class AbsResultBuilder(metaclass=abc.ABCMeta):
    """Abstract base class for result builder."""

    @abc.abstractmethod
    def create_new_summary(self) -> None:
        """Reset the contents of a summary."""

    @abc.abstractmethod
    def add_result(self, result: Result) -> None:
        """Add a result to be used in a summary.

        Args:
            result: Result object to be added

        """

    @abc.abstractmethod
    def get_summary(self) -> ResultSummary:
        """Generate and return a summary."""

    @abc.abstractmethod
    def set_source(self, source: str) -> None:
        """Set the source of the results.

        Args:
            source: Usually a file path.

        """


class ResultSummaryBuilder(AbsResultBuilder):
    """Builder class for creating summaries from Result objects."""

    def __init__(self) -> None:
        """Create a new ResultSummaryBuilder object."""
        self.summary: Optional[ResultSummary] = None
        self.source: Optional[str] = None

    def create_new_summary(self) -> None:
        """Generate and return a summary."""
        self.summary = ResultSummary()

    def add_result(self, result: Result) -> None:
        """Add a result to be used in a summary.

        Args:
            result: Result object to be added

        """
        if self.summary is None:
            raise RuntimeError("Summary has not been set")

        self.summary += result

    def get_summary(self) -> ResultSummary:
        """Generate and return a summary."""
        if self.summary is None:
            raise RuntimeError("Summary has not been set")

        return self.summary

    def set_source(self, source: str) -> None:
        """Set the source of the results.

        Args:
            source: Usually a file path.

        """
        self.source = source


class SummaryDirector:
    """Director class for building summaries."""

    def __init__(self, source: str) -> None:
        """Create a new summary director object.

        Args:
            source: Usually a file path.

        """
        self.builder = ResultSummaryBuilder()
        self.builder.create_new_summary()
        self.builder.source = source

    def add_error(self, message: str) -> None:
        """Add additional error message to the summary.

        Args:
            message: Contents of an error message.

        """
        new_error = Result("error")
        new_error.message = message
        new_error.source = self.builder.source
        self.builder.add_result(new_error)

    def construct(self) -> ResultSummary:
        """Construct and return a new ResultSummary."""
        return self.builder.get_summary()
