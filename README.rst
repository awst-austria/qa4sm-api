.. coding: utf-8

.. image:: https://img.shields.io/badge/CI-GitHub%20Actions-success?logo=github-actions
   :alt: GitHub Actions
   :target: https://github.com/awst-austria/qa4sm-api/actions
.. image:: https://img.shields.io/coveralls/github/awst-austria/qa4sm-api/main?logo=coveralls
   :alt: Coveralls
   :target: https://coveralls.io/github/awst-austria/qa4sm-api
.. image:: https://img.shields.io/pypi/v/qa4sm-api?logo=pypi
   :alt: PyPI
   :target: https://pypi.org/project/qa4sm-api/
.. image:: https://img.shields.io/github/v/release/awst-austria/qa4sm-api?display_name=tag
   :alt: GitHub release (latest SemVer)
   :target: https://github.com/awst-austria/qa4sm-api/releases

|

=========
qa4sm-api
=========

.. image:: https://qa4sm.eu/static/images/logo/qa4sm_logo_long.webp
   :height: 50px

Python client library for interacting with the **QA4SM** (Quality Assurance for Soil Moisture) validation service.
QA4SM is an online platform for validating (satellite) soil moisture datasets.

Features
--------

- **API Client**: Python API for QA4SM.eu web service
- **Command Line Interface**: Convenient CLI for common operations
- **Result Download**: Download NetCDF, graphics, and summary statistics
- **Search datasets in the service**, **download validation configurations**, ...
- **Programmatically trigger validation runs**

Coming soon:

- Programmatically upload your data for validation

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install qa4sm-api

Or from source:

.. code-block:: bash

   git clone https://github.com/awst-austria/qa4sm-api.git
   cd qa4sm-api
   pip install -e .

Documentation
-------------

Full documentation is available at https://awst-austria.github.io/qa4sm-api/

The documentation includes:

- Installation and setup
- Python API reference
- Command-line interface guide
- Usage examples and tutorials

Quick Start
-----------

**Command Line Interface:**

.. code-block:: bash

   # Test installation
   qa4sm --version

   # Check available commands
   qa4sm --help

**Python API:**

.. code-block:: python

   from qa4sm_api.client_api import Connection, ValidationConfiguration

   # Initialize connection
   conn = Connection()

   # now use the connection, e.g., discover datasets
   datasets = conn.datasets()

Authentication
--------------

Before using the API, you need to authenticate with QA4SM.

**Option 1: Automated setup (recommended)**

.. code-block:: bash

   qa4sm api setup

This prompts for your credentials and stores your API token in ``~/.qa4smapirc``.

**Option 2: Manual setup**

Create ``~/.qa4smapirc`` with your credentials:

.. code-block:: ini

   [qa4sm.eu]
   token: your_api_token_here
   username: your_username

API tokens are available from https://qa4sm.eu/ui/user-profile

CLI Commands
------------

- ``qa4sm api setup`` - Configure authentication
- ``qa4sm api check`` - Verify authentication
- ``qa4sm validate CONFIG.json`` - Submit a validation run
- ``qa4sm download config RUN_ID`` - Download configuration
- ``qa4sm download results RUN_ID`` - Download validation results

Use ``qa4sm --help`` for all commands.

Testing
-------

Run tests:

.. code-block:: bash

   pip install -e ".[testing]"
   pytest

Run with coverage:

.. code-block:: bash

   pytest --cov=qa4sm_api --cov-report=term-missing

Current coverage: ~68%

Project Status
-------------

| Resource | URL |
|----------|-----|
| Repository | https://github.com/awst-austria/qa4sm-api |
| Website | https://awst-austria.github.io/qa4sm-api |
| Documentation | https://awst-austria.github.io/qa4sm-api |
| Issue Tracker | https://github.com/awst-austria/qa4sm-api/issues |
| License | MIT |

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
---------------

This project was developed by TU Wien for the QA4SM validation service.

.. note::
   This project has been set up using PyScaffold 4.6. For details and usage information on PyScaffold see https://pyscaffold.org/.