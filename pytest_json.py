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

from collections import defaultdict


__version__ = '0.0.1'


def pytest_addoption(parser):
    """ Called first to add additional CLI options
    """
    pass


@pytest.mark.trylast
def pytest_configure(config):
    """ Call in second to configure stuff
    """
    # Get the standard terminal reporter plugin and replace it with our own
    standard_reporter = config.pluginmanager.getplugin('terminalreporter')
    json_reporter = JsonTerminalReporter(standard_reporter)
    config.pluginmanager.unregister(standard_reporter)
    config.pluginmanager.register(json_reporter, 'terminalreporter')


def pytest_collection_modifyitems(session, config, items):
    """ Called third with the collected items
    """
    pass


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
        self.outcomes = defaultdict(set)

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

        self.outcomes[report.nodeid].add(report.outcome)

        # Print the report as json
        if report.when == 'teardown':
            # Compute the final test outcome
            outcomes = self.outcomes[report.nodeid]
            if 'failed' in outcomes:
                outcome = 'failed'
            else:
                outcome = 'passed'

            raw_json_report = {
                'file': report.fspath,
                'line': report.location[1],
                'duration': report.duration,
                'outcome': outcome,
                'id': report.nodeid,
                'stdout': report.capstdout,
                'stderr': report.capstderr,
            }
            print(json.dumps(raw_json_report))

        # Save the stats
        self.stats.setdefault(report.outcome, []).append(report)

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
