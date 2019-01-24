# -*- coding: utf-8 -*-
import os.path

DEFAULT_PATH = "test-output.xml"


def pytest_itemcollected(item):
    parent = item.parent.obj  # Test class/module
    node = item.obj  # Test case
    suite_doc = parent.__doc__.strip() if parent.__doc__ else None
    case_doc = node.__doc__.strip() if node.__doc__ else None
    if suite_doc and case_doc:
        item._nodeid = '{0} [{1}]'.format(suite_doc, case_doc)
    elif suite_doc and not case_doc:
        item._nodeid = '{0} [{1}]'.format(suite_doc, node.__name__)
    elif case_doc and not suite_doc:
        item._nodeid = '{0} [{1}]'.format(parent.__name__, case_doc)
    else:
        item._nodeid = node.__name__


def pytest_configure(config):
    xmlpath = config.getoption('--junitxml')
    if not xmlpath:
        config.option.xmlpath = DEFAULT_PATH


def pytest_sessionfinish(session, exitstatus):
    xmlpath = session.config.option.xmlpath
    if not xmlpath:
        xmlpath = session.config.getoption('--junitxml')
    # This mirrors https://github.com/pytest-dev/pytest/blob/38adb23bd245329d26b36fd85a43aa9b3dd0406c/src/_pytest/junitxml.py#L368-L369
    xmlabspath = os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(xmlpath))))
    print("##vso[results.publish type=JUnit; mergeTestResults=false;]{0}".format(xmlabspath))


def pytest_warning_captured(warning_message, when, *args):
    print("##vso[task.issue type=warning;]{0}".format(str(warning_message.message)))
