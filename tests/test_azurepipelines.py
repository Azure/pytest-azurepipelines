# -*- coding: utf-8 -*-

import pytest


def test_bar_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_sth():
            assert 1 == 1
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*test_sth PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_warning_output(testdir):
    # create a temporary pytest test module
    testdir.makepyfile("""
        import warnings
        def test_warnings():
            assert 1 == 1
            warnings.warn("Checking the warning feature inside a test")
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*test_warnings PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_apply_docker_mappings():
    """
    GIVEN a dummy /proc/1/mountinfo with a docker mapping and a path contained
    in the mapping WHEN calling apply_docker_mappings THEN the path
    substitution should occur and the host path returned.
    """
    # Setup
    from pytest_azurepipelines import apply_docker_mappings
    dummy_mountinfo = """\
673 654 8:1 /home/tgates/hostspace /workspace rw,relatime - ext4 /dev/sda1 rw,errors=remount-ro,data=ordered
"""
    dockerpath = '/workspace/test'
    hostpath = '/home/tgates/hostspace/test'
    # Exercise
    checkpath = apply_docker_mappings(dummy_mountinfo, dockerpath)
    # Verify
    assert hostpath == checkpath


@pytest.mark.testfail
def test_failure(testdir):
    """
    Purposefully raise a failing test.
    """
    raise RuntimeError("Check stack traces in UI")
