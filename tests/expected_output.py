import re

from pytest_litf import LITF_VERSION


class GreaterThan(object):
    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return other > self._value

    def __repr__(self):
        return "%d+" % self._value


class RegexMatch(object):
    def __init__(self, regex):
        self._regex = regex

    def __eq__(self, other):
        # Dictdiffer seems to call ourselves vs ourselved
        if hasattr(other, "_regex"):
            return self._regex == other._regex

        return re.match(self._regex, other)

    def __repr__(self):
        return repr(self._regex)


class EitherMatch(object):
    def __init__(self, values):
        self._values = values

    def __eq__(self, other):
        # Dictdiffer seems to call ourselves vs ourselved
        if hasattr(other, "_values"):
            return self._values == other._values

        for value in self._values:
            if other == value:
                return True

        return False

    def __repr__(self):
        return repr(self._values)


def get_expected_litf_output_collect_only():
    return [
        {"_type": "litf_start", "litf_version": LITF_VERSION},
        {"_type": "session_start", "test_number": 32},
        {
            "_type": "test_collection",
            "line": 11,
            "file": "test_class.py",
            "test_name": "TestClassPassing.test_passing",
            "id": "test_class.py::TestClassPassing::test_passing",
        },
        {
            "_type": "test_collection",
            "line": 22,
            "file": "test_class.py",
            "test_name": "TestClassFailing.test_failing",
            "id": "test_class.py::TestClassFailing::test_failing",
        },
        {
            "_type": "test_collection",
            "line": 33,
            "file": "test_class.py",
            "test_name": "TestClassError.test_error",
            "id": "test_class.py::TestClassError::test_error",
        },
        {
            "_type": "test_collection",
            "line": 44,
            "file": "test_class.py",
            "test_name": "TestClassFailingAndErrorTeardown.test_error",
            "id": "test_class.py::TestClassFailingAndErrorTeardown::test_error",
        },
        {
            "_type": "test_collection",
            "line": 55,
            "file": "test_class.py",
            "test_name": "TestClassErrorSetup.test_passing",
            "id": "test_class.py::TestClassErrorSetup::test_passing",
        },
        {
            "_type": "test_collection",
            "line": 66,
            "file": "test_class.py",
            "test_name": "TestClassErrorSetupAndTeardown.test_passing",
            "id": "test_class.py::TestClassErrorSetupAndTeardown::test_passing",
        },
        {
            "_type": "test_collection",
            "line": 77,
            "file": "test_class.py",
            "test_name": "TestClassErrorTeardown.test_passing",
            "id": "test_class.py::TestClassErrorTeardown::test_passing",
        },
        {
            "_type": "test_collection",
            "line": 6,
            "file": "test_func.py",
            "test_name": "test_success",
            "id": "test_func.py::test_success",
        },
        {
            "_type": "test_collection",
            "line": 10,
            "file": "test_func.py",
            "test_name": "test_fails",
            "id": "test_func.py::test_fails",
        },
        {
            "_type": "test_collection",
            "line": 14,
            "file": "test_func.py",
            "test_name": "test_fixtures[0]",
            "id": "test_func.py::test_fixtures[0]",
        },
        {
            "_type": "test_collection",
            "line": 14,
            "file": "test_func.py",
            "test_name": "test_fixtures[1]",
            "id": "test_func.py::test_fixtures[1]",
        },
        {
            "_type": "test_collection",
            "line": 14,
            "file": "test_func.py",
            "test_name": "test_fixtures[2]",
            "id": "test_func.py::test_fixtures[2]",
        },
        {
            "_type": "test_collection",
            "line": 19,
            "file": "test_func.py",
            "test_name": "test_error",
            "id": "test_func.py::test_error",
        },
        {
            "_type": "test_collection",
            "line": 12,
            "file": "test_module_setup_teardown.py",
            "test_name": "test_passing",
            "id": "test_module_setup_teardown.py::test_passing",
        },
        {
            "_type": "test_collection",
            "line": 16,
            "file": "test_module_setup_teardown.py",
            "test_name": "test_failing",
            "id": "test_module_setup_teardown.py::test_failing",
        },
        {
            "_type": "test_collection",
            "line": 27,
            "file": "test_module_setup_teardown.py",
            "test_name": "TestClassPassing.test_passing",
            "id": "test_module_setup_teardown.py::TestClassPassing::test_passing",
        },
        {
            "_type": "test_collection",
            "line": 38,
            "file": "test_module_setup_teardown.py",
            "test_name": "TestClassFailing.test_failing",
            "id": "test_module_setup_teardown.py::TestClassFailing::test_failing",
        },
        {
            "_type": "test_collection",
            "line": 6,
            "file": "test_skip.py",
            "test_name": "test_skip_function",
            "id": "test_skip.py::test_skip_function",
        },
        {
            "_type": "test_collection",
            "line": 12,
            "file": "test_skip.py",
            "test_name": "TestSkipCall.test_skip_method",
            "id": "test_skip.py::TestSkipCall::test_skip_method",
        },
        {
            "_type": "test_collection",
            "line": 19,
            "file": "test_skip.py",
            "test_name": "TestSkipClass.test_skipped_1",
            "id": "test_skip.py::TestSkipClass::test_skipped_1",
        },
        {
            "_type": "test_collection",
            "line": 22,
            "file": "test_skip.py",
            "test_name": "TestSkipClass.test_skipped_2",
            "id": "test_skip.py::TestSkipClass::test_skipped_2",
        },
        {
            "_type": "test_collection",
            "line": 6,
            "file": "test_slow.py",
            "test_name": "test_slow_passing",
            "id": "test_slow.py::test_slow_passing",
        },
        {
            "_type": "test_collection",
            "line": 6,
            "file": "test_std.py",
            "test_name": "test_stdout",
            "id": "test_std.py::test_stdout",
        },
        {
            "_type": "test_collection",
            "line": 10,
            "file": "test_std.py",
            "test_name": "test_stderr",
            "id": "test_std.py::test_stderr",
        },
        {
            "_type": "test_collection",
            "line": 21,
            "file": "test_std.py",
            "test_name": "TestClassStdout.test_stdout",
            "id": "test_std.py::TestClassStdout::test_stdout",
        },
        {
            "_type": "test_collection",
            "line": 32,
            "file": "test_std.py",
            "test_name": "TestClassStdoutSetup.test_stdout",
            "id": "test_std.py::TestClassStdoutSetup::test_stdout",
        },
        {
            "_type": "test_collection",
            "line": 43,
            "file": "test_std.py",
            "test_name": "TestClassStdoutAllPhases.test_stdout",
            "id": "test_std.py::TestClassStdoutAllPhases::test_stdout",
        },
        {
            "_type": "test_collection",
            "line": 54,
            "file": "test_std.py",
            "test_name": "TestClassFailing.test_stderr",
            "id": "test_std.py::TestClassFailing::test_stderr",
        },
        {
            "_type": "test_collection",
            "line": 10,
            "file": "test_unittest.py",
            "test_name": "TestStringMethods.test_isupper",
            "id": "test_unittest.py::TestStringMethods::test_isupper",
        },
        {
            "_type": "test_collection",
            "line": 7,
            "file": "test_unittest.py",
            "test_name": "TestStringMethods.test_upper",
            "id": "test_unittest.py::TestStringMethods::test_upper",
        },
        {
            "_type": "test_collection",
            "line": 4,
            "file": "directory/test_file_2.py",
            "test_name": "test_success",
            "id": "directory/test_file_2.py::test_success",
        },
        {
            "_type": "test_collection",
            "line": 4,
            "file": "directory/test_func.py",
            "test_name": "test_success",
            "id": "directory/test_func.py::test_success",
        },
        {
            "_type": "session_end",
            "total_duration": GreaterThan(0),
            "passed": 0,
            "failed": 0,
            "error": 0,
            "skipped": 0,
        },
    ]


def get_expected_litf_output_full_run():

    return [
        {"_type": "litf_start", "litf_version": "0.0.1"},
        {"_type": "session_start", "test_number": 32},
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 11,
            "test_name": "TestClassPassing.test_passing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_class.py::TestClassPassing::test_passing",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 22,
            "test_name": "TestClassFailing.test_failing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_class.py::TestClassFailing::test_failing",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_class.TestClassFailing object at 0x.*>\n\n    def test_failing\(self\):\n>       assert False\nE       assert False\n\ntest_class.py:23: AssertionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 33,
            "test_name": "TestClassError.test_error",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_class.py::TestClassError::test_error",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_class.TestClassError object at 0x.*>\n\n    def test_error\(self\):\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_class.py:34: ZeroDivisionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 44,
            "test_name": "TestClassFailingAndErrorTeardown.test_error",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_class.py::TestClassFailingAndErrorTeardown::test_error",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_class.TestClassFailingAndErrorTeardown object at 0x.*>\n\n    def test_error\(self\):\n>       assert False\nE       assert False\n\ntest_class.py:45: AssertionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 55,
            "test_name": "TestClassErrorSetup.test_passing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_class.py::TestClassErrorSetup::test_passing",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_class.TestClassErrorSetup object at 0x.*>\nmethod = <bound method TestClassErrorSetup.test_passing of <test_class.TestClassErrorSetup object at 0x.*>>\n\n    def setup_method\(self, method\):\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_class.py:50: ZeroDivisionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 66,
            "test_name": "TestClassErrorSetupAndTeardown.test_passing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_class.py::TestClassErrorSetupAndTeardown::test_passing",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_class.TestClassErrorSetupAndTeardown object at 0x.*>\nmethod = <bound method TestClassErrorSetupAndTeardown.test_passing of <test_class.TestClassErrorSetupAndTeardown object at 0x.*>>\n\n    def setup_method\(self, method\):\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_class.py:61: ZeroDivisionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 77,
            "test_name": "TestClassErrorTeardown.test_passing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_class.py::TestClassErrorTeardown::test_passing",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_class.TestClassErrorTeardown object at 0x.*>\nmethod = <bound method TestClassErrorTeardown.test_passing of <test_class.TestClassErrorTeardown object at 0x.*>>\n\n    def teardown_method\(self, method\):\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_class.py:75: ZeroDivisionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 6,
            "test_name": "test_success",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_func.py::test_success",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 10,
            "test_name": "test_fails",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_func.py::test_fails",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": "def test_fails():\n>       assert False\nE       assert False\n\ntest_func.py:11: AssertionError"
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 14,
            "test_name": "test_fixtures[0]",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_func.py::test_fixtures[0]",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 14,
            "test_name": "test_fixtures[1]",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_func.py::test_fixtures[1]",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": EitherMatch(
                    # Diff order seems to change with pytest 5.4.0
                    [
                        'number = 1\n\n    @pytest.mark.parametrize("number", list(range(3)))\n    def test_fixtures(number):\n>       assert number % 2 == 0\nE       assert 1 == 0\nE         +1\nE         -0\n\ntest_func.py:16: AssertionError',
                        'number = 1\n\n    @pytest.mark.parametrize("number", list(range(3)))\n    def test_fixtures(number):\n>       assert number % 2 == 0\nE       assert 1 == 0\nE         -1\nE         +0\n\ntest_func.py:16: AssertionError',
                        'number = 1\n\n    @pytest.mark.parametrize("number", list(range(3)))\n    def test_fixtures(number):\n>       assert number % 2 == 0\nE       assert (1 % 2) == 0\n\ntest_func.py:16: AssertionError',
                    ]
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 14,
            "test_name": "test_fixtures[2]",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_func.py::test_fixtures[2]",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 19,
            "test_name": "test_error",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_func.py::test_error",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": "def test_error():\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_func.py:20: ZeroDivisionError"
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_module_setup_teardown.py",
            "line": 12,
            "test_name": "test_passing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_module_setup_teardown.py::test_passing",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_module_setup_teardown.py",
            "line": 16,
            "test_name": "test_failing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_module_setup_teardown.py::test_failing",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": "def test_failing():\n>       assert False\nE       assert False\n\ntest_module_setup_teardown.py:17: AssertionError"
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_module_setup_teardown.py",
            "line": 27,
            "test_name": "TestClassPassing.test_passing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_module_setup_teardown.py::TestClassPassing::test_passing",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_module_setup_teardown.py",
            "line": 38,
            "test_name": "TestClassFailing.test_failing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_module_setup_teardown.py::TestClassFailing::test_failing",
            "stdout": "TD M\nTD MO\n",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_module_setup_teardown.TestClassFailing object at 0x.*>\n\n    def test_failing\(self\):\n>       assert False\nE       assert False\n\ntest_module_setup_teardown.py:39: AssertionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_skip.py",
            "line": 6,
            "test_name": "test_skip_function",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "skipped",
            "id": "test_skip.py::test_skip_function",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {"setup": "Skipped: Skip"},
        },
        {
            "_type": "test_result",
            "file": "test_skip.py",
            "line": 12,
            "test_name": "TestSkipCall.test_skip_method",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "skipped",
            "id": "test_skip.py::TestSkipCall::test_skip_method",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {"setup": "Skipped: Skip"},
        },
        {
            "_type": "test_result",
            "file": "test_skip.py",
            "line": 19,
            "test_name": "TestSkipClass.test_skipped_1",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "skipped",
            "id": "test_skip.py::TestSkipClass::test_skipped_1",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {"setup": "Skipped: Skip"},
        },
        {
            "_type": "test_result",
            "file": "test_skip.py",
            "line": 22,
            "test_name": "TestSkipClass.test_skipped_2",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "skipped",
            "id": "test_skip.py::TestSkipClass::test_skipped_2",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {"setup": "Skipped: Skip"},
        },
        {
            "_type": "test_result",
            "file": "test_slow.py",
            "line": 6,
            "test_name": "test_slow_passing",
            "duration": GreaterThan(2),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(2),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_slow.py::test_slow_passing",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_std.py",
            "line": 6,
            "test_name": "test_stdout",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_std.py::test_stdout",
            "stdout": "STDOUT\n",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_std.py",
            "line": 10,
            "test_name": "test_stderr",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_std.py::test_stderr",
            "stdout": "",
            "stderr": "STDERR\n",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_std.py",
            "line": 21,
            "test_name": "TestClassStdout.test_stdout",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_std.py::TestClassStdout::test_stdout",
            "stdout": "STDOUT\n",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_std.py",
            "line": 32,
            "test_name": "TestClassStdoutSetup.test_stdout",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_std.py::TestClassStdoutSetup::test_stdout",
            "stdout": "SETUP\n",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_std.py",
            "line": 43,
            "test_name": "TestClassStdoutAllPhases.test_stdout",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_std.py::TestClassStdoutAllPhases::test_stdout",
            "stdout": "SETUP\nTEST\nTEARDOWN\n",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_std.py",
            "line": 54,
            "test_name": "TestClassFailing.test_stderr",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_std.py::TestClassFailing::test_stderr",
            "stdout": "",
            "stderr": "STDERR\n",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_unittest.py",
            "line": 10,
            "test_name": "TestStringMethods.test_isupper",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "failed",
            "id": "test_unittest.py::TestStringMethods::test_isupper",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": 'self = <test_unittest.TestStringMethods testMethod=test_isupper>\n\n    def test_isupper(self):\n        self.assertTrue("FOO".isupper())\n>       self.assertTrue("Foo".isupper())\nE       AssertionError: False is not true\n\ntest_unittest.py:12: AssertionError'
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_unittest.py",
            "line": 7,
            "test_name": "TestStringMethods.test_upper",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "test_unittest.py::TestStringMethods::test_upper",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "directory/test_file_2.py",
            "line": 4,
            "test_name": "test_success",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "directory/test_file_2.py::test_success",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "directory/test_func.py",
            "line": 4,
            "test_name": "test_success",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
                "teardown": GreaterThan(0),
            },
            "outcome": "passed",
            "id": "directory/test_func.py::test_success",
            "stdout": "",
            "stderr": "",
            "error": {"humanrepr": ""},
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "session_end",
            "total_duration": GreaterThan(2),
            "passed": 17,
            "failed": 9,
            "error": 4,
            "skipped": 4,
        },
    ]
