import re
import os.path
import json
import subprocess

import dictdiffer
from pytest_litf import LITF_VERSION

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(PACKAGE_DIR, "..", "example_dir")


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


def _process_output(output_lines):
    json_lines = []
    invalid_lines = []

    for line in output_lines.splitlines():
        if not line:
            continue

        # Python 3.5 returns bytes for subprocess output and JSON loads only
        # accepts strings
        if hasattr(line, "decode"):
            line = line.decode("utf-8")

        try:
            json_lines.append(json.loads(line))
        except (ValueError, TypeError):
            invalid_lines.append(line.strip())

    return json_lines, invalid_lines


def test_pytest_litf_collect_only():
    args = {"collect-only": True}
    cmd = ["pytest-litf", json.dumps(args)]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=TEST_DIR
    )

    assert result.stderr == b""

    json_lines, invalid_lines = _process_output(result.stdout)

    assert invalid_lines == ["collecting ..."]

    expected = [
        {"_type": "litf_start", "litf_version": LITF_VERSION},
        {"_type": "session_start", "test_number": 32},
        {
            "_type": "test_collection",
            "file": "test_class.py",
            "id": "test_class.py::TestClassPassing::test_passing",
            "line": 8,
            "test_name": "TestClassPassing.test_passing",
        },
        {
            "_type": "test_collection",
            "file": "test_class.py",
            "id": "test_class.py::TestClassFailing::test_failing",
            "line": 19,
            "test_name": "TestClassFailing.test_failing",
        },
        {
            "_type": "test_collection",
            "file": "test_class.py",
            "id": "test_class.py::TestClassError::test_error",
            "line": 30,
            "test_name": "TestClassError.test_error",
        },
        {
            "_type": "test_collection",
            "file": "test_class.py",
            "id": "test_class.py::TestClassFailingAndErrorTeardown::test_error",
            "line": 41,
            "test_name": "TestClassFailingAndErrorTeardown.test_error",
        },
        {
            "_type": "test_collection",
            "file": "test_class.py",
            "id": "test_class.py::TestClassErrorSetup::test_passing",
            "line": 52,
            "test_name": "TestClassErrorSetup.test_passing",
        },
        {
            "_type": "test_collection",
            "file": "test_class.py",
            "id": "test_class.py::TestClassErrorSetupAndTeardown::test_passing",
            "line": 63,
            "test_name": "TestClassErrorSetupAndTeardown.test_passing",
        },
        {
            "_type": "test_collection",
            "file": "test_class.py",
            "id": "test_class.py::TestClassErrorTeardown::test_passing",
            "line": 74,
            "test_name": "TestClassErrorTeardown.test_passing",
        },
        {
            "_type": "test_collection",
            "file": "test_func.py",
            "id": "test_func.py::test_success",
            "line": 4,
            "test_name": "test_success",
        },
        {
            "_type": "test_collection",
            "file": "test_func.py",
            "id": "test_func.py::test_fails",
            "line": 8,
            "test_name": "test_fails",
        },
        {
            "_type": "test_collection",
            "file": "test_func.py",
            "id": "test_func.py::test_fixtures[0]",
            "line": 12,
            "test_name": "test_fixtures[0]",
        },
        {
            "_type": "test_collection",
            "file": "test_func.py",
            "id": "test_func.py::test_fixtures[1]",
            "line": 12,
            "test_name": "test_fixtures[1]",
        },
        {
            "_type": "test_collection",
            "file": "test_func.py",
            "id": "test_func.py::test_fixtures[2]",
            "line": 12,
            "test_name": "test_fixtures[2]",
        },
        {
            "_type": "test_collection",
            "file": "test_func.py",
            "id": "test_func.py::test_error",
            "line": 17,
            "test_name": "test_error",
        },
        {
            "_type": "test_collection",
            "file": "test_module_setup_teardown.py",
            "id": "test_module_setup_teardown.py::test_passing",
            "line": 9,
            "test_name": "test_passing",
        },
        {
            "_type": "test_collection",
            "file": "test_module_setup_teardown.py",
            "id": "test_module_setup_teardown.py::test_failing",
            "line": 13,
            "test_name": "test_failing",
        },
        {
            "_type": "test_collection",
            "file": "test_module_setup_teardown.py",
            "id": "test_module_setup_teardown.py::TestClassPassing::test_passing",
            "line": 24,
            "test_name": "TestClassPassing.test_passing",
        },
        {
            "_type": "test_collection",
            "file": "test_module_setup_teardown.py",
            "id": "test_module_setup_teardown.py::TestClassFailing::test_failing",
            "line": 35,
            "test_name": "TestClassFailing.test_failing",
        },
        {
            "_type": "test_collection",
            "file": "test_skip.py",
            "id": "test_skip.py::test_skip_function",
            "line": 4,
            "test_name": "test_skip_function",
        },
        {
            "_type": "test_collection",
            "file": "test_skip.py",
            "id": "test_skip.py::TestSkipCall::test_skip_method",
            "line": 10,
            "test_name": "TestSkipCall.test_skip_method",
        },
        {
            "_type": "test_collection",
            "file": "test_skip.py",
            "id": "test_skip.py::TestSkipClass::test_skipped_1",
            "line": 17,
            "test_name": "TestSkipClass.test_skipped_1",
        },
        {
            "_type": "test_collection",
            "file": "test_skip.py",
            "id": "test_skip.py::TestSkipClass::test_skipped_2",
            "line": 20,
            "test_name": "TestSkipClass.test_skipped_2",
        },
        {
            "_type": "test_collection",
            "file": "test_slow.py",
            "id": "test_slow.py::test_slow_passing",
            "line": 4,
            "test_name": "test_slow_passing",
        },
        {
            "_type": "test_collection",
            "file": "test_std.py",
            "id": "test_std.py::test_stdout",
            "line": 4,
            "test_name": "test_stdout",
        },
        {
            "_type": "test_collection",
            "file": "test_std.py",
            "id": "test_std.py::test_stderr",
            "line": 8,
            "test_name": "test_stderr",
        },
        {
            "_type": "test_collection",
            "file": "test_std.py",
            "id": "test_std.py::TestClassStdout::test_stdout",
            "line": 19,
            "test_name": "TestClassStdout.test_stdout",
        },
        {
            "_type": "test_collection",
            "file": "test_std.py",
            "id": "test_std.py::TestClassStdoutSetup::test_stdout",
            "line": 30,
            "test_name": "TestClassStdoutSetup.test_stdout",
        },
        {
            "_type": "test_collection",
            "file": "test_std.py",
            "id": "test_std.py::TestClassStdoutAllPhases::test_stdout",
            "line": 41,
            "test_name": "TestClassStdoutAllPhases.test_stdout",
        },
        {
            "_type": "test_collection",
            "file": "test_std.py",
            "id": "test_std.py::TestClassFailing::test_stderr",
            "line": 52,
            "test_name": "TestClassFailing.test_stderr",
        },
        {
            "_type": "test_collection",
            "file": "test_unittest.py",
            "id": "test_unittest.py::TestStringMethods::test_isupper",
            "line": 8,
            "test_name": "TestStringMethods.test_isupper",
        },
        {
            "_type": "test_collection",
            "file": "test_unittest.py",
            "id": "test_unittest.py::TestStringMethods::test_upper",
            "line": 5,
            "test_name": "TestStringMethods.test_upper",
        },
        {
            "_type": "test_collection",
            "file": "directory/test_file_2.py",
            "id": "directory/test_file_2.py::test_success",
            "line": 4,
            "test_name": "test_success",
        },
        {
            "_type": "test_collection",
            "file": "directory/test_func.py",
            "id": "directory/test_func.py::test_success",
            "line": 4,
            "test_name": "test_success",
        },
        {
            "_type": "session_end",
            "error": 0,
            "failed": 0,
            "passed": 0,
            "skipped": 0,
            "total_duration": GreaterThan(0),
        },
    ]

    assert json_lines == expected

    assert result.returncode == 0


def test_pytest_litf_full_run():
    args = {}
    cmd = ["pytest-litf", json.dumps(args)]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=TEST_DIR
    )

    assert result.stderr == b""

    json_lines, invalid_lines = _process_output(result.stdout)

    assert invalid_lines == ["collecting ..."]

    expected = [
        {"_type": "litf_start", "litf_version": LITF_VERSION},
        {"_type": "session_start", "test_number": 32},
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 8,
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
            "line": 19,
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
                    r"self = <test_class.TestClassFailing object at 0x.*>\n\n    def test_failing\(self\):\n>       assert False\nE       assert False\n\ntest_class.py:20: AssertionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 30,
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
                    r"self = <test_class.TestClassError object at .*>\n\n    def test_error\(self\):\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_class.py:31: ZeroDivisionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 41,
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
                    r"self = <test_class.TestClassFailingAndErrorTeardown object at .*>\n\n    def test_error\(self\):\n>       assert False\nE       assert False\n\ntest_class.py:42: AssertionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 52,
            "test_name": "TestClassErrorSetup.test_passing",
            "duration": GreaterThan(0),
            "durations": {"setup": GreaterThan(0), "teardown": GreaterThan(0),},
            "outcome": "failed",
            "id": "test_class.py::TestClassErrorSetup::test_passing",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_class.TestClassErrorSetup object at .*>\nmethod = <bound method TestClassErrorSetup.test_passing of <test_class.TestClassErrorSetup object at 0x.*>>\n\n    def setup_method\(self, method\):\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_class.py:47: ZeroDivisionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 63,
            "test_name": "TestClassErrorSetupAndTeardown.test_passing",
            "duration": GreaterThan(0),
            "durations": {"setup": GreaterThan(0), "teardown": GreaterThan(0),},
            "outcome": "failed",
            "id": "test_class.py::TestClassErrorSetupAndTeardown::test_passing",
            "stdout": "",
            "stderr": "",
            "error": {
                "humanrepr": RegexMatch(
                    r"self = <test_class.TestClassErrorSetupAndTeardown object at 0x.*>\nmethod = <bound method TestClassErrorSetupAndTeardown.test_passing of <test_class.TestClassErrorSetupAndTeardown object at 0x.*>>\n\n    def setup_method\(self, method\):\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_class.py:58: ZeroDivisionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_class.py",
            "line": 74,
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
                    r"self = <test_class.TestClassErrorTeardown object at 0x.*>\nmethod = <bound method TestClassErrorTeardown.test_passing of <test_class.TestClassErrorTeardown object at 0x.*>>\n\n    def teardown_method\(self, method\):\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_class.py:72: ZeroDivisionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 4,
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
            "line": 8,
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
                "humanrepr": "def test_fails():\n>       assert False\nE       assert False\n\ntest_func.py:9: AssertionError"
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 12,
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
            "line": 12,
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
                "humanrepr": 'number = 1\n\n    @pytest.mark.parametrize("number", list(range(3)))\n    def test_fixtures(number):\n>       assert number % 2 == 0\nE       assert 1 == 0\nE         +1\nE         -0\n\ntest_func.py:14: AssertionError'
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_func.py",
            "line": 12,
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
            "line": 17,
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
                "humanrepr": "def test_error():\n>       1 / 0\nE       ZeroDivisionError: division by zero\n\ntest_func.py:18: ZeroDivisionError"
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_module_setup_teardown.py",
            "line": 9,
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
            "line": 13,
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
                "humanrepr": "def test_failing():\n>       assert False\nE       assert False\n\ntest_module_setup_teardown.py:14: AssertionError"
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_module_setup_teardown.py",
            "line": 24,
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
            "line": 35,
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
                    r"self = <test_module_setup_teardown.TestClassFailing object at 0x.*>\n\n    def test_failing\(self\):\n>       assert False\nE       assert False\n\ntest_module_setup_teardown.py:36: AssertionError"
                )
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_skip.py",
            "line": 4,
            "test_name": "test_skip_function",
            "duration": GreaterThan(0),
            "durations": {"setup": GreaterThan(0), "teardown": GreaterThan(0),},
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
            "line": 10,
            "test_name": "TestSkipCall.test_skip_method",
            "duration": GreaterThan(0),
            "durations": {"setup": GreaterThan(0), "teardown": GreaterThan(0),},
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
            "line": 17,
            "test_name": "TestSkipClass.test_skipped_1",
            "duration": GreaterThan(0),
            "durations": {"setup": GreaterThan(0), "teardown": GreaterThan(0),},
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
            "line": 20,
            "test_name": "TestSkipClass.test_skipped_2",
            "duration": GreaterThan(0),
            "durations": {"setup": GreaterThan(0), "teardown": GreaterThan(0),},
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
            "line": 4,
            "test_name": "test_slow_passing",
            "duration": GreaterThan(0),
            "durations": {
                "setup": GreaterThan(0),
                "call": GreaterThan(0),
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
            "line": 4,
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
            "line": 8,
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
            "line": 19,
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
            "line": 30,
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
            "line": 41,
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
            "line": 52,
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
            "line": 8,
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
                "humanrepr": 'self = <test_unittest.TestStringMethods testMethod=test_isupper>\n\n    def test_isupper(self):\n        self.assertTrue("FOO".isupper())\n>       self.assertTrue("Foo".isupper())\nE       AssertionError: False is not true\n\ntest_unittest.py:10: AssertionError'
            },
            "logs": "",
            "skipped_messages": {},
        },
        {
            "_type": "test_result",
            "file": "test_unittest.py",
            "line": 5,
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
            "total_duration": GreaterThan(0),
            "passed": 17,
            "failed": 9,
            "error": 4,
            "skipped": 4,
        },
    ]

    print("Got", json_lines)

    diff = list(dictdiffer.diff(json_lines, expected))

    assert diff == []

    assert result.returncode == 1
