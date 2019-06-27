Release History
~~~~~~~~~~~~~~~

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
