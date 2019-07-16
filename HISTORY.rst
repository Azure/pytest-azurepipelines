Release History
~~~~~~~~~~~~~~~


1.0.0a1 (16th July 2019)
------------------------

* FEATURE: Use pytest-nunit instead of Junit XML to have richer details and stack traces in the UI.

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
