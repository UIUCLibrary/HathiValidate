import io
from unittest.mock import Mock

from hathi_validate import report, result


def test_report_as_str_is_a_string_message():
    error_result = result.Result("error")
    error_result.message = "This is an error message"
    results = [
        error_result
    ]
    final_report = report.get_report_as_str(results)
    assert \
        isinstance(final_report, str) and \
        error_result.message in final_report


class TestConsoleReporter:
    def test_report_to_stream(self):
        stream = io.StringIO()
        stream_reporter = report.ConsoleReporter(stream)
        stream_reporter.report("spam")
        assert "spam" in stream.getvalue()

class TestReporter:
    def test_report_calls_strategy(self):
        reporter_strategy = Mock(spec=report.AbsReporter)
        reporter = report.Reporter(reporter_strategy=reporter_strategy)
        reporter.report("spam")
        reporter_strategy.report.assert_called_once_with("spam")