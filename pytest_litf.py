# -*- coding: utf-8 -*-
"""
pytest_litf
~~~~~~~~~~~

py.test litf is a plugin for py.test that output test results in Language
Independent Test Format.

:copyright: see LICENSE for details
:license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals

import json
import os
import sys
from pathlib import Path

import py
import pytest

try:
    """
    pytest > 5.4 uses own version of TerminalWriter based on py.io.TerminalWriter
    and assumes there is a specific method TerminalWriter._write_source
    so try load pytest version first or fallback to default one
    """
    from _pytest._io import TerminalWriter
except ImportError:
    from py.io import TerminalWriter

__version__ = "0.1.2"
LITF_VERSION = "0.0.1"
GLOBAL_REPORTER = None


def pytest_addoption(parser):
    """Called first to add additional CLI options"""
    group = parser.getgroup("terminal reporting", "reporting", after="general")
    group._addoption(
        "--litf",
        action="store_true",
        dest="litf",
        default=False,
        help="Activate the litf output",
    )
    group._addoption(
        "--litf-output-file",
        action="store",
        dest="litf_output_filepath",
        default=None,
        help="If --lift flag is set, write LITF output to the given file instead of stdout",
    )


@pytest.mark.trylast
def pytest_configure(config):
    """Call in second to configure stuff"""
    global GLOBAL_REPORTER

    if config.getvalue("litf"):

        standard_reporter = config.pluginmanager.getplugin("terminalreporter")

        litf_output_filepath = config.getvalue("litf_output_filepath")
        if litf_output_filepath is not None:
            # Add a file reporter to write LITF output to a given file
            litf_output_path = Path(litf_output_filepath)
            # Ensure the directory exists
            litf_output_path.parent.mkdir(parents=True, exist_ok=True)
            # And ensure we can write to that path
            litf_output_path.touch()
            GLOBAL_REPORTER = LitfFileReporter(standard_reporter, litf_output_path)
        else:
            # Unregister the standard terminal reporter plugin and add the LITF File Reporter
            # emiting to sys.stdout
            GLOBAL_REPORTER = LitfFileReporter(standard_reporter)
            config.pluginmanager.unregister(standard_reporter)

        config.pluginmanager.register(GLOBAL_REPORTER, "litfreporter")


def pytest_collection_modifyitems(session, config, items):
    """Called third with the collected items"""
    if GLOBAL_REPORTER is not None:
        GLOBAL_REPORTER.output({"_type": "litf_start", "litf_version": LITF_VERSION})
        data = {"_type": "session_start", "test_number": len(items)}
        GLOBAL_REPORTER.output(data)


class LitfFileReporter:
    def __init__(self, reporter, output_filepath=None):
        # TerminalReporter.__init__(self, reporter.config)
        self.config = reporter.config
        self.startdir = self.config.invocation_dir
        self._numcollected = 0
        self.stats = {}

        if output_filepath is not None:
            self.output_file = open(output_filepath, "w", encoding="utf-8")
        else:
            self.output_file = sys.stdout

        self.reports = []
        self.reportsbyid = {}

    def output(self, json_data):
        # In case of some test printing stuff on stdout without a newline, write a
        # newline
        self.output_file.write("\n")
        json.dump(json_data, self.output_file)
        self.output_file.write("\n")
        # Flush the output to avoid buffering issues
        self.output_file.flush()

    def pytest_collectreport(self, report):
        """Override to not display anything"""
        if report.failed:
            self.stats.setdefault("error", []).append(report)
        elif report.skipped:
            self.stats.setdefault("skipped", []).append(report)
        items = [x for x in report.result if isinstance(x, pytest.Item)]
        self._numcollected += len(items)

    def pytest_sessionstart(self, session):
        self._session = session
        self._sessionstarttime = py.std.time.time()

    def pytest_runtest_logreport(self, report):
        # Save reports for later
        self.reports.append(report)

        self.reportsbyid.setdefault(report.nodeid, []).append(report)

        if report.when == "teardown":
            self.dump_json(self.reportsbyid[report.nodeid])

        # Save the stats
        self.stats.setdefault(report.outcome, []).append(report)

    def dump_json(self, reports):
        # Compute the final test outcome
        outcomes = [report.outcome for report in reports]
        if "failed" in outcomes:
            outcome = "failed"
        elif "skipped" in outcomes:
            outcome = "skipped"
        else:
            outcome = "passed"

        # Errors
        error = ""
        errors = {}
        for report in reports:
            if report.outcome == "failed" and report.longrepr:
                if hasattr(report.longrepr, "toterminal"):
                    # Compute human repre
                    stringio = py.io.TextIO()
                    tw = TerminalWriter(stringio)
                    tw.hasmarkup = False
                    report.longrepr.toterminal(tw)
                    exc = stringio.getvalue()
                else:
                    exc = str(report.longrepr)
                humanrepr = exc.strip()

                errors[report.when] = {"humanrepr": humanrepr}

                # Take the first error
                if not error:
                    error = humanrepr

        # Skipped
        skipped_messages = {}
        for report in reports:
            if report.outcome == "skipped" and report.longrepr:
                skipped_messages[report.when] = report.longrepr[2]

        # Durations
        total_duration = 0
        durations = {}
        for report in reports:
            durations[report.when] = report.duration
            total_duration += report.duration

        report = reports[-1]

        # Get logs reports
        logs = ""

        for secname, content in report.sections:
            if secname == "Captured log call":
                logs = content

        raw_json_report = {
            "_type": "test_result",
            "file": report.fspath,
            "line": report.location[1] + 1,  # Pytest lineno are 0-based
            "test_name": report.location[2],
            "duration": total_duration,
            "durations": durations,
            "outcome": outcome,
            "id": report.nodeid,
            "stdout": report.capstdout,
            "stderr": report.capstderr,
            "error": {"humanrepr": error},
            "logs": logs,
            "skipped_messages": skipped_messages,
        }
        self.output(raw_json_report)

    def count(self, key, when=("call",)):
        if self.stats.get(key):
            return len(
                [
                    x
                    for x in self.stats.get(key)
                    if not hasattr(x, "when") or x.when in when
                ]
            )

        else:
            return 0

    def pytest_collection_finish(self, session):
        if self.config.option.collectonly:
            for item in session.items:

                raw_json_report = {
                    "_type": "test_collection",
                    "line": item.location[1] + 1,  # Pytest lineno are 0-based
                    "file": item.fspath.relto(os.getcwd()),
                    "test_name": item.location[2],
                    "id": item.nodeid,
                }
                self.output(raw_json_report)

            # Todo handle
            if self.stats.get("failed"):
                self._tw.sep("!", "collection failures")
                for rep in self.stats.get("failed"):
                    rep.toterminal(self._tw)
                return 1

            return 0

    def pytest_sessionfinish(self, session, exitstatus):
        session_duration = py.std.time.time() - self._sessionstarttime

        final = {
            "_type": "session_end",
            "total_duration": session_duration,
            "passed": self.count("passed"),
            "failed": self.count("failed", when=["call"]),
            "error": self.count("failed", when=["setup", "teardown"]),
            "skipped": self.count("skipped", when=["call", "setup", "teardown"]),
        }

        self.output(final)
