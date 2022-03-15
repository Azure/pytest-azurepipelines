=====================
pytest-azurepipelines
=====================

.. image:: https://dev.azure.com/AnthonyShaw/pytest-azurepipelines/_apis/build/status/tonybaloney.pytest-azurepipelines?branchName=master
   :target: https://dev.azure.com/AnthonyShaw/pytest-azurepipelines/_build/latest?definitionId=3?branchName=master
   :alt: Build status

.. image:: https://img.shields.io/pypi/v/pytest-azurepipelines.svg
    :target: https://pypi.org/project/pytest-azurepipelines
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-azurepipelines.svg
    :target: https://pypi.org/project/pytest-azurepipelines
    :alt: Python versions

.. image:: https://img.shields.io/pypi/dm/pytest-azurepipelines.svg
     :target: https://pypi.python.org/pypi/pytest-azurepipelines/
     :alt: PyPI download month

Making Pytest easier to use with Microsoft Azure Pipelines.

Just run pytest with this plugin and see your test results in the Azure Pipelines UI!

----

Features:

* Formats the PyTest output to show test docstrings and module names instead of just test case names in the Azure Pipelines UI.
* Uploads test results automatically, no need for a separate test results upload command
* Displays the number of failed tests if there were failures as an error message in the UI
* Automatically formats code coverage and uploads coverage data if pytest-cov is installed
* Supports running inside a Docker container and automatically uploads test results

Use this plugin with the [vs-pytest](https://marketplace.visualstudio.com/items?itemName=AnthonyShaw.vss-pytest&WT.mc_id=python-0000-anthonyshaw) extension installed to see granular pytest data inside the Azure UI:

.. image:: https://github.com/tonybaloney/pytest-azurepipelines/raw/master/screenshot.png
    :width: 600px
    :align: center

Installation
------------

You can install "pytest-azurepipelines" via `pip`_ from `PyPI`_::

    $ pip install pytest-azurepipelines

Usage
-----

This plugin requires no configuration.

Here is an example of installing the plugin and running the tests.

.. code-block:: yaml

  - script: |
      python -m pip install --upgrade pip
      pip install pytest pytest-azurepipelines
      pip install -e .
    displayName: 'Install dependencies'

  - script: |
      python -m pytest tests/
    displayName: 'pytest'

If you want to change the Azure Pipelines "Test Run Title", you can provide the `--test-run-title` flag with the run title.

.. code-block:: yaml

  - script: |
      pip install pytest pytest-azurepipelines
      pytest tests/ --test-run-title="Windows Test"

If you have long docstrings in your functions and want them to be shortened, you can use the `--napoleon-docstrings` flag:

.. code-block:: yaml
 
   - script: |
      pip install pytest pytest-azurepipelines
      pytest tests/ --test-run-title="Windows Test" --napoleon-docstrings

Fixtures
--------

The following fixtures are made available by this plugin.

``record_pipelines_property``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calling `record_pipelines_property(key: str, value: str)` will result in `Property` tags being added to the `test-case` for the related node. 

.. code-block:: python

    def test_basic(record_pipelines_property):
        record_pipelines_property("test", "value")
        assert 1 == 1

``add_pipelines_attachment``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add an attachment to a node test-case by calling the `add_pipelines_attachment(path: str, description: str)` function with the filepath and a description.

Attachments can be viewed in the Azure Pipelines UI under the 'Attachments' tab for a test case.

.. code-block:: python

    def test_attachment(add_pipelines_attachment):
        pth = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixture.gif')
        add_pipelines_attachment(path, "peanut butter jelly time")
        assert 1 == 1

Using the automatic code coverage upload
----------------------------------------

From version 0.6.0, pytest will upload successful coverage data into a format that Azure supports and package
the htmlcov directory into a ZIP file as an artifact for the build.

To use this feature, add the `--cov` flag with (optional, but required) path to your code files and also ensure you add `--cov-report html` as an option.

.. code-block:: yaml
 
   - script: |
      pip install pytest pytest-azurepipelines pytest-cov
      pytest tests/ --cov my_project --cov-report html

To disable coverage upload, use the `--no-coverage-upload` flag.

Running in Docker
-----------------

The plugin automatically detects when running inside a docker
container. It will apply
the mappings to the path to report them back to Azure Pipelines using the path
from the host that has been bind mounted to the docker container. 

No configuration is required if bind mounting is
used to the path the pytest output is written to. Also ensure the files are
written using an account the host has access to, this can be done by supplying
the user and group of the host account to the run command.

.. code-block:: bash

    docker run --user "$(id -u):$(id -g)" ...

To disable docker discovery, use the `--no-docker-discovery` flag.

Contributing
------------

Contributions are very welcome. 

License
-------

Distributed under the terms of the MIT license, "pytest-azurepipelines" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/tonybaloney/pytest-azurepipelines/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
