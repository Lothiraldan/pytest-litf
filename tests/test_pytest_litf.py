import json
import os.path
import subprocess

import dictdiffer
from expected_output import (
    get_expected_litf_output_collect_only,
    get_expected_litf_output_full_run,
)

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(PACKAGE_DIR, "..", "example_dir")


def _process_output(output_lines):
    json_lines = []
    invalid_lines = []

    for line in output_lines.splitlines():
        if not line:
            continue

        try:
            json_lines.append(json.loads(line))
        except (ValueError, TypeError):
            invalid_lines.append(line.strip())

    return json_lines, invalid_lines


def test_pytest_litf_collect_only_stdout():
    args = {"collect-only": True}
    cmd = ["pytest-litf", json.dumps(args)]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=TEST_DIR
    )

    assert result.stderr == b""

    json_lines, invalid_lines = _process_output(result.stdout)

    # assert invalid_lines == [b"collecting ..."]

    expected = get_expected_litf_output_collect_only()

    assert json_lines == expected

    assert result.returncode == 0


def test_pytest_litf_collect_only_file_output(tmp_path):
    """Test that we can write the LITF output to a file while doing collection only"""
    output_filepath = tmp_path / "dir" / "out.litf"
    args = {"collect-only": True, "output-file": output_filepath.as_posix()}
    cmd = ["pytest-litf", json.dumps(args)]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=TEST_DIR
    )

    assert result.stderr == b""

    with open(output_filepath, "rb") as output_file:
        json_lines, invalid_lines = _process_output(output_file.read())

    # assert invalid_lines == [b"collecting ..."]

    expected = get_expected_litf_output_collect_only()

    assert json_lines == expected

    assert result.returncode == 0


def test_pytest_litf_full_run_stdout():
    args = {}
    cmd = ["pytest-litf", json.dumps(args)]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=TEST_DIR
    )

    assert result.stderr == b""

    json_lines, invalid_lines = _process_output(result.stdout)

    # assert invalid_lines == [b"collecting ..."]

    expected = get_expected_litf_output_full_run()

    print("Got", json_lines)

    diff = list(dictdiffer.diff(json_lines, expected))

    assert diff == []

    assert result.returncode == 1


def test_pytest_litf_full_run_file_ouput(tmp_path):
    output_filepath = tmp_path / "out.litf"
    args = {"output-file": output_filepath.as_posix()}
    cmd = ["pytest-litf", json.dumps(args)]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=TEST_DIR
    )

    assert result.stderr == b""

    with open(output_filepath, "rb") as output_file:
        json_lines, invalid_lines = _process_output(output_file.read())

    # assert invalid_lines == [b"collecting ..."]

    expected = get_expected_litf_output_full_run()

    print("Got", json_lines)

    diff = list(dictdiffer.diff(json_lines, expected))

    assert diff == []

    assert result.returncode == 1
