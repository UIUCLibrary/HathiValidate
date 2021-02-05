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
