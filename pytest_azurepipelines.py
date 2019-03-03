# -*- coding: utf-8 -*-
import os.path
import pytest

DEFAULT_PATH = "test-output.xml"


def pytest_addoption(parser):
    group = parser.getgroup('pytest_azurepipelines')
    group.addoption(
        '--test-run-title',
        action='store',
        dest='azure_run_title',
        default='Pytest results',
        help='Set the Azure test run title.'
    )
    group.addoption(
        '--napoleon-docstrings',
        action='store_true',
        dest='napoleon',
        default=False,
        help='If using Google, NumPy, or PEP 257 multi-line docstrings.'
    )


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        parent = item.parent.obj  # Test class/module
        node = item.obj  # Test case
        if config.getoption('napoleon'):
            suite_doc = parent.__doc__.split('\n\n')[0] if parent.__doc__ else parent.__name__
            case_doc = node.__doc__.split('\n\n')[0] if node.__doc__ else None
            item._nodeid = '[{0}] {1}/{2}'.format(case_doc, suite_doc, item.name)
        else:
            suite_doc = parent.__doc__.strip() if parent.__doc__ else None
            case_doc = node.__doc__.strip() if node.__doc__ else None
            if suite_doc and case_doc:
                item._nodeid = '{0} [{1}]'.format(suite_doc, case_doc)
            elif suite_doc and not case_doc:
                item._nodeid = '{0} [{1}]'.format(suite_doc, node.__name__)
            elif case_doc and not suite_doc and hasattr(parent, '__name__'):
                item._nodeid = '{0} [{1}]'.format(parent.__name__, case_doc)
            else:
                item._nodeid = node.__name__


def pytest_configure(config):
    xmlpath = config.getoption('--junitxml')
    if not xmlpath:
        config.option.xmlpath = DEFAULT_PATH

    # ensure coverage creates xml format
    if config.pluginmanager.has_plugin('pytest_cov'):
        if 'xml' not in config.option.cov_report:
            config.option.cov_report['xml'] = None


def pytest_sessionfinish(session, exitstatus):
    xmlpath = session.config.option.xmlpath

    # This mirrors https://github.com/pytest-dev/pytest/blob/38adb23bd245329d26b36fd85a43aa9b3dd0406c/src/_pytest/junitxml.py#L368-L369
    xmlabspath = os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(xmlpath))))

    # Set the run title in the UI to a configurable setting
    description = session.config.option.azure_run_title.replace("'", "")

    print("##vso[results.publish type=JUnit;runTitle='{1}';]{0}".format(xmlabspath, description))

    if exitstatus != 0 and session.testsfailed > 0 and not session.shouldfail:
        print("##vso[task.logissue type=error;]{0} test(s) failed, {1} test(s) collected.".format(session.testsfailed, session.testscollected))

    if session.config.pluginmanager.has_plugin('pytest_cov'):
        covpath = os.path.join(os.path.normpath(os.path.abspath(os.path.expanduser)), 'coverage.xml')
        print("##vso[codecoverage.publish codecoveragetool=Cobertura;summaryfile='{0}';]".format(covpath))

def pytest_warning_captured(warning_message, when, *args):
    print("##vso[task.logissue type=warning;]{0}".format(str(warning_message.message)))
