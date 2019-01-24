# -*- coding: utf-8 -*-
junitxml = None


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
    junitxml = config.getoption('--junitxml')
    print("Found JunitXml configuration {0}".format(junitxml))


def pytest_sessionfinish(session, exitstatus):
    junitxml = session.config.getoption('--junitxml')
    if junitxml:
        files = "**/{0}.xml".format(junitxml)
    else:
        files = "**/test*.xml"
    print("##vso[results.publish type=JUnit; mergeTestResults=false; testResultsFiles={0};]".format(files))


def pytest_warning_captured(warning_message, when, *args):
    print("##vso[task.issue type=warning;]{0}".format(str(warning_message)))
