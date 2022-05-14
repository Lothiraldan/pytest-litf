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

import py
import pytest
from _pytest.terminal import TerminalReporter

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


def pytest_addoption(parser):
    """Called first to add additional CLI options"""
    group = parser.getgroup("terminal reporting", "reporting", after="general")
    group._addoption(
        "--litf",
        action="store_true",
        dest="litf",
        default=False,
        help=("Activate the litf output"),
    )


@pytest.mark.trylast
def pytest_configure(config):
    """Call in second to configure stuff"""
    if config.getvalue("litf"):
        # Get the standard terminal reporter plugin and replace it with our own
        standard_reporter = config.pluginmanager.getplugin("terminalreporter")
        litf_reporter = LitfTerminalReporter(standard_reporter)
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(litf_reporter, "terminalreporter")


def output(json_data):
    """A centralized function to print litf json-lines"""
    # In case of some test printing stuff on stdout without a newline, write a
    # newline
    sys.stdout.write("\n")
    json.dump(json_data, sys.stdout)
    sys.stdout.write("\n")
    # Flush the output to avoid buffering issues
    sys.stdout.flush()


def pytest_collection_modifyitems(session, config, items):
    """Called third with the collected items"""
    if config.getvalue("litf"):
        output({"_type": "litf_start", "litf_version": LITF_VERSION})
        data = {"_type": "session_start", "test_number": len(items)}
        output(data)


def pytest_sessionstart(session):
    """Called fourth to read config and setup global variables"""


def pytest_deselected(items):
    """Update tests_count to not include deselected tests"""
    pass


class LitfTerminalReporter(TerminalReporter):
    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)
        self.reports = []
        self.reportsbyid = {}

    def report_collect(self, final=False):
        pass

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

    def write_fspath_result(self, fspath, res):
        return

    def pytest_runtest_logstart(self, nodeid, location):
        # Prevent locationline from being printed since we already
        # show the module_name & in verbose mode the test name.
        pass

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
        output(raw_json_report)

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
                output(raw_json_report)

            # Todo handle
            if self.stats.get("failed"):
                self._tw.sep("!", "collection failures")
                for rep in self.stats.get("failed"):
                    rep.toterminal(self._tw)
                return 1

            return 0

        lines = self.config.hook.pytest_report_collectionfinish(
            config=self.config, startdir=self.startdir, items=session.items
        )
        self._write_report_lines_from_hooks(lines)

    def summary_stats(self):
        session_duration = py.std.time.time() - self._sessionstarttime

        final = {
            "_type": "session_end",
            "total_duration": session_duration,
            "passed": self.count("passed"),
            "failed": self.count("failed", when=["call"]),
            "error": self.count("failed", when=["setup", "teardown"]),
            "skipped": self.count("skipped", when=["call", "setup", "teardown"]),
        }

        output(final)

    def summary_errors(self):
        # Prevent error summary from being shown since we already
        # show the error instantly after error has occured.
        pass

    def summary_failures(self):
        # Prevent failure summary from being shown since we already
        # show the failure instantly after failure has occured.
        pass

    def summary_warnings(self):
        pass

    def summary_passes(self):
        pass

    def short_test_summary(self):
        # Prevent showing the short test summary
        pass
