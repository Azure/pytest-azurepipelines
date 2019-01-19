=====================
pytest-azurepipelines
=====================

.. image:: https://img.shields.io/pypi/v/pytest-azurepipelines.svg
    :target: https://pypi.org/project/pytest-azurepipelines
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-azurepipelines.svg
    :target: https://pypi.org/project/pytest-azurepipelines
    :alt: Python versions

.. image:: https://travis-ci.org/tonybaloney/pytest-azurepipelines.svg?branch=master
    :target: https://travis-ci.org/tonybaloney/pytest-azurepipelines
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/tonybaloney/pytest-azurepipelines?branch=master
    :target: https://ci.appveyor.com/project/tonybaloney/pytest-azurepipelines/branch/master
    :alt: See Build Status on AppVeyor

Formatting PyTest output for Azure Pipelines UI

----

Formats the PyTest output to show test docstrings and module names instead of just test case names in the Azure Pipelines UI.

Requires the `--junit-xml` flag on execution as per normal Azure Pipelines usage.

Installation
------------

You can install "pytest-azurepipelines" via `pip`_ from `PyPI`_::

    $ pip install pytest-azurepipelines


Usage
-----

* TODO

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-azurepipelines" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/tonybaloney/pytest-azurepipelines/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
