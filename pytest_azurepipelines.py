# -*- coding: utf-8 -*-

import os.path
import io
import sys
import pytest

DEFAULT_PATH = "test-output.xml"
DEFAULT_COVERAGE_PATH = "coverage.xml"


def pytest_addoption(parser):
    group = parser.getgroup("pytest_azurepipelines")
    group.addoption(
        "--test-run-title",
        action="store",
        dest="azure_run_title",
        default="Pytest results",
        help="Set the Azure test run title.",
    )
    group.addoption(
        "--napoleon-docstrings",
        action="store_true",
        dest="napoleon",
        default=False,
        help="If using Google, NumPy, or PEP 257 multi-line docstrings.",
    )
    group.addoption(
        "--no-coverage-upload",
        action="store_true",
        dest="no_coverage_upload",
        default=False,
        help="Skip uploading coverage results to Azure Pipelines.",
    )
    group.addoption(
        "--no-docker-discovery",
        action="store_true",
        dest="no_docker_discovery",
        default=False,
        help="Skip detecting running inside a Docker container.",
    )


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        # Make sure that nodes have required attributes
        if not hasattr(item, "obj") or not hasattr(item.parent, "obj"):
            continue

        parent = item.parent.obj  # Test class/module
        node = item.obj  # Test case
        if node is None:
            pass
        elif config.getoption("napoleon"):
            suite_doc = (
                parent.__doc__.split("\n\n")[0] if parent.__doc__ else parent.__name__
            )
            case_doc = node.__doc__.split("\n\n")[0] if node.__doc__ else None
            item._nodeid = "[{0}] {1}/{2}".format(case_doc, suite_doc, item.name)


def pytest_configure(config):
    xmlpath = config.getoption("--junitxml")
    if not xmlpath:
        config.option.xmlpath = DEFAULT_PATH

    # ensure coverage creates xml format
    if config.pluginmanager.has_plugin("pytest_cov"):
        config.option.cov_report["xml"] = os.path.normpath(
            os.path.abspath(os.path.expanduser(os.path.expandvars(DEFAULT_COVERAGE_PATH)))
        )
        if "html" not in config.option.cov_report:
            config.option.cov_report["html"] = None


def pytest_sessionfinish(session, exitstatus):
    xmlpath = session.config.option.xmlpath

    # This mirrors https://github.com/pytest-dev/pytest/blob/38adb23bd245329d26b36fd85a43aa9b3dd0406c/src/_pytest/junitxml.py#L368-L369
    xmlabspath = os.path.normpath(
        os.path.abspath(os.path.expanduser(os.path.expandvars(xmlpath)))
    )
    mountinfo = None
    if not session.config.getoption("no_docker_discovery") and os.path.isfile('/.dockerenv'):
        with io.open(
                    '/proc/1/mountinfo', 'rb',
                ) as fobj:
            mountinfo = fobj.read()
        mountinfo = mountinfo.decode(sys.getfilesystemencoding())
    if mountinfo:
        xmlabspath = apply_docker_mappings(mountinfo, xmlabspath)

    # Set the run title in the UI to a configurable setting
    description = session.config.option.azure_run_title.replace("'", "")

    if not session.config.getoption("no_docker_discovery"):
        print(
            "##vso[results.publish type=JUnit;runTitle='{1}';]{0}".format(
                xmlabspath, description
            )
        )
    else:
        print("Skipping uploading of test results because --no-docker-discovery set.")

    if exitstatus != 0 and session.testsfailed > 0 and not session.shouldfail:
        print(
            "##vso[task.logissue type=error;]{0} test(s) failed, {1} test(s) collected.".format(
                session.testsfailed, session.testscollected
            )
        )

    if not session.config.getoption("no_coverage_upload") and not session.config.getoption("no_docker_discovery") and session.config.pluginmanager.has_plugin("pytest_cov"):
        covpath = os.path.normpath(
            os.path.abspath(os.path.expanduser(os.path.expandvars(DEFAULT_COVERAGE_PATH)))
        )
        reportdir = os.path.normpath(os.path.abspath("htmlcov"))
        if os.path.exists(covpath):
            if mountinfo:
                covpath = apply_docker_mappings(mountinfo, covpath)
                reportdir = apply_docker_mappings(mountinfo, reportdir)
            print(
                "##vso[codecoverage.publish codecoveragetool=Cobertura;summaryfile={0};reportdirectory={1};]".format(
                    covpath, reportdir
                )
            )
        else:
            print(
                "##vso[task.logissue type=warning;]{0}".format(
                    "Coverage XML was not created, skipping upload."
                )
            )
    else:
        print("Skipping uploading of coverage data.")


def apply_docker_mappings(mountinfo, dockerpath):
    """
    Parse the /proc/1/mountinfo file and apply the mappings so that docker
    paths are transformed into the host path equivalent so the Azure Pipelines
    finds the file assuming the path has been bind mounted from the host.
    """
    for line in mountinfo.splitlines():
        words = line.split(' ')
        if len(words) < 5:
            continue
        docker_mnt_path = words[4]
        host_mnt_path = words[3]
        if dockerpath.startswith(docker_mnt_path):
            dockerpath = ''.join([
                host_mnt_path,
                dockerpath[len(docker_mnt_path):],
            ])
    return dockerpath


def pytest_warning_captured(warning_message, when, *args):
    print("##vso[task.logissue type=warning;]{0}".format(str(warning_message.message)))
