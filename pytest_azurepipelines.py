# -*- coding: utf-8 -*-


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


def pytest_sessionfinish(session, exitstatus):
    # print("##vso[results.publish type=info;]This is a test 2")


def pytest_warning_captured(warning_message, when, *args):
    print("##vso[task.issue type=warning;]{0}".format(str(warning_message)))
