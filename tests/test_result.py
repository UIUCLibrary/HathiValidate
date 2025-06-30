from hathi_validate import result
import pytest


@pytest.fixture(scope="module")
def simple_summary():
    summary_builder = result.SummaryDirector(source="spam_source")
    summary_builder.add_error("Not valid")
    summary = summary_builder.construct()
    return summary


def test_summary_builder(simple_summary):
    assert isinstance(simple_summary, result.ResultSummary)


def test_summary_size(simple_summary):
    assert len(simple_summary) == 1


def test_summary_iter(simple_summary):
    for report in simple_summary:
        assert isinstance(report, result.Result)


def test_summary_report(simple_summary):
    i = iter(simple_summary)
    report = next(i)
    assert report.message == "Not valid"
    assert report.source == "spam_source"


@pytest.fixture(scope="module")
def multiple_summary():
    summary_builder = result.SummaryDirector(source="eggs_source")
    summary_builder.add_error("Some Error")
    summary_builder.add_error("Another Error")
    return summary_builder.construct()

def test_multiple_summary_size(multiple_summary):
    assert len(multiple_summary) == 2

class TestResult:
    def test_str_with_no_source(self):
        my_result = result.Result("dummy")
        my_result.source = None
        assert str(my_result) =='Result[dummy]""'

    def test_str_with_source(self):
        my_result = result.Result("dummy")
        my_result.source = "spam"
        assert str(my_result) =='Result[dummy]spam: ""'