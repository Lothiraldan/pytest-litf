# -*- coding: utf-8 -*-
"""
pytest_json
~~~~~~~~~~~

py.test is a plugin for py.test that changes the default look
and feel of py.test (e.g. progressbar, show tests that fail instantly).

:copyright: see LICENSE for details
:license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals
import json

import py
import pytest
from _pytest.terminal import TerminalReporter


__version__ = '0.0.1'


def pytest_addoption(parser):
    """ Called first to add additional CLI options
    """
    group = parser.getgroup("terminal reporting", "reporting", after="general")
    group._addoption(
        '--json', action="store_true",
        dest="json", default=False,
        help=(
            "Activate the json output"
        )
    )

@pytest.mark.trylast
def pytest_configure(config):
    """ Call in second to configure stuff
    """

    if config.getvalue('json'):
        # Get the standard terminal reporter plugin and replace it with our own
        standard_reporter = config.pluginmanager.getplugin('terminalreporter')
        json_reporter = JsonTerminalReporter(standard_reporter)
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(json_reporter, 'terminalreporter')


def pytest_collection_modifyitems(session, config, items):
    """ Called third with the collected items
    """
    data = {
        '_type': 'session_start',
        'test_number': len(items)
    }
    print(json.dumps(data))


def pytest_sessionstart(session):
    """ Called fourth to read config and setup global variables
    """

## XDIST, matrix style?
# try:
#     import xdist
# except ImportError:
#     pass
# else:
#     from distutils.version import LooseVersion
#     xdist_version = LooseVersion(xdist.__version__)
#     if xdist_version >= LooseVersion("1.14"):
#         def pytest_xdist_node_collection_finished(node, ids):
#             terminal_reporter = node.config.pluginmanager.getplugin(
#                 'terminalreporter'
#             )
#             if terminal_reporter:
#                 terminal_reporter.tests_count = len(ids)


def pytest_deselected(items):
    """ Update tests_count to not include deselected tests """
    print("pytest_deselected", items, len(items))
    # if len(items) > 0:
    #     pluginmanager = items[0].config.pluginmanager
    #     terminal_reporter = pluginmanager.getplugin('terminalreporter')
    #     if (hasattr(terminal_reporter, 'tests_count')
    #             and terminal_reporter.tests_count > 0):
    #         terminal_reporter.tests_count -= len(items)


class JsonTerminalReporter(TerminalReporter):
    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)
        self.writer = self._tw
        self.reports = []
        self.reportsbyid = {}

    def report_collect(self, final=False):
        pass

    def pytest_collectreport(self, report):
        """ Override to not display anything
        """
        if report.failed:
            self.stats.setdefault("error", []).append(report)
        elif report.skipped:
            self.stats.setdefault("skipped", []).append(report)
        items = [x for x in report.result if isinstance(x, pytest.Item)]
        self._numcollected += len(items)

    def pytest_sessionstart(self, session):
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

        if report.when == 'teardown':
            self.dump_json(self.reportsbyid[report.nodeid])

        # Save the stats
        self.stats.setdefault(report.outcome, []).append(report)

    def dump_json(self, reports):
        # Compute the final test outcome
        outcomes = [report.outcome for report in reports]
        if 'failed' in outcomes:
            outcome = 'failed'
        elif 'skipped' in outcomes:
            outcome = 'skipped'
        else:
            outcome = 'passed'

        # Errors
        errors = {}
        for report in reports:
            if report.longrepr:

                # Compute human repre
                tw = py.io.TerminalWriter(stringio=True)
                tw.hasmarkup = False
                report.longrepr.toterminal(tw)
                exc = tw.stringio.getvalue()
                humanrepr = exc.strip()

                errors[report.when] = {'humanrepr': humanrepr}

        # Durations
        total_duration = 0
        durations = {}
        for report in reports:
            durations[report.when] = report.duration
            total_duration += report.duration

        report = reports[-1]

        raw_json_report = {
            '_type': 'test_result',
            'file': report.fspath,
            'line': report.location[1],
            'test_name': report.location[2],
            'duration': total_duration,
            'durations': durations,
            'outcome': outcome,
            'id': report.nodeid,
            'stdout': report.capstdout,
            'stderr': report.capstderr,
            'errors': errors,
            'when': report.when
        }
        print(json.dumps(raw_json_report))

    def count(self, key, when=('call',)):
        if self.stats.get(key):
            return len([
                x for x in self.stats.get(key)
                if not hasattr(x, 'when') or x.when in when
            ])
        else:
            return 0

    def summary_stats(self):
        session_duration = py.std.time.time() - self._sessionstarttime

        final = {
            '_type': 'session_end',
            'total_duration': session_duration,
            'passed': self.count('passed'),
            'failed': self.count('failed', when=['call']),
            'error': self.count('failed', when=['setup', 'teardown']),
            'skipped': self.count('skipped', when=['call', 'setup', 'teardown'])
        }

        print(json.dumps(final))

    def summary_failures(self):
        # Prevent failure summary from being shown since we already
        # show the failure instantly after failure has occured.
        pass

    def summary_errors(self):
        # Prevent error summary from being shown since we already
        # show the error instantly after error has occured.
        pass
