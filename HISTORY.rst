Release History
~~~~~~~~~~~~~~~

1.0.3 (16th March 2022)
~~~~~~~~~~~~~~~~~~~~~~~

* Updated to latest pytest-nunit

1.0.2 (15th March 2022)
~~~~~~~~~~~~~~~~~~~~~~~

* Fixed missing XML files when not specified on command line

1.0.1 (15th March 2022)
~~~~~~~~~~~~~~~~~~~~~~~

* Added support for Pytest 7

1.0.0rc5 (21st July 2020)
~~~~~~~~~~~~~~~~~~~~~~~~~

* Reverted change in 1.0.0rc4
* Set hook loading sequence to avoid collision with other plugins

1.0.0rc4 (9th June 2020)
~~~~~~~~~~~~~~~~~~~~~~~~

* Moved deprecated pytest hook `pytest_warning_captured` to `pytest_warning_recorded`

1.0.0rc3 (9th June 2020)
~~~~~~~~~~~~~~~~~~~~~

- xUnit 2 support in newer PyTest APIs (Optional)
- Drop support for older PyTest releases (pre 5)
- Drop support for Python 2

1.0.0rc1 (30th August 2019)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- First public release candidate of 1.0 features

1.0.0a2 (30th August 2019)
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Upload test data
- Support for vs-pytest UI extension

1.0.0a1 (16th July 2019)
------------------------

* FEATURE: Use pytest-nunit instead of Junit XML to have richer details and stack traces in the UI.
* FEATURE: Added ``add_pipelines_attachment`` fixture for adding attachments to the output.
* FEATURE: Added ``record_pipelines_property`` fixture for capturing runtime test case properties.

0.8.0 (7th July 2019)
---------------------

* FEATURE: Plugin will detect when being run inside a docker container and upload the test results into the mounted file path automatically (@timgates42)
* FEATURE: Added Pytest 5.0.0 support
* BUGFIX: Fixed crash when used with doctest modules
* FEATURE: Added --no-coverage-upload flag to skip uploading coverage even when coverage data is discovered
* FEATURE: Added --no-docker-discovery flag to skip detecting docker mount points
* BUGFIX: Test coverage file will be called coverage.xml instead of test-cov.xml, to fix compatibility with codecov.io
* OTHER: Builds are now verified against two massive test-suites (jinja2 and yellowbrick)

0.7.0
-----

* IMPORTANT: Nodeid rewriting is now opt-in via the `--napoleon-docstrings` flag, the default setting will not change Nodeid
* BUGFIX: Fixed support with other 3rd party plugins (pytest-flake8, pytest-black)

0.6.0
-----

* Add support for pytest-cov uploading coverage results and the htmlcov as an artifact
* Known issue: requires `--cov-report html` to be added on the CLI for the report upload to work

0.5.0
-----

* Add `--napoleon-docstrings` flag for shortened docstrings
* Fixed bug where some nodes could not be renamed if using `conftest.py`

0.4.0
-----

* Fix custom title flag #10
