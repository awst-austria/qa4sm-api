.. coding: utf-8

.. image:: https://img.shields.io/badge/CI-GitHub%20Actions-success?logo=github-actions
   :alt: GitHub Actions
   :target: https://github.com/awst-austria/qa4sm-api/actions
.. image:: https://img.shields.io/coveralls/github/awst-austria/qa4sm-api/main?logo=coveralls
   :alt: Coveralls
   :target: https://coveralls.io/github/awst-austria/qa4sm-api
.. image:: https://img.shields.io/pypi/v/qa4sm-api
   :alt: PyPI
   :target: https://pypi.org/project/qa4sm-api/
.. image:: https://img.shields.io/badge/Docs-Documentation-blue?logo=sphinx
   :alt: Documentation
   :target: https://awst-austria.github.io/qa4sm-api/readme.html


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
============

Install from PyPI:

.. code-block:: bash

   pip install qa4sm-api

Or from source:

.. code-block:: bash

   git clone https://github.com/awst-austria/qa4sm-api.git
   cd qa4sm-api
   pip install -e .

**Verify installation**

Run the following commands in your console to verify that the page
was installed.

.. code-block:: bash

   # Test installation
   qa4sm --version

   # Check available commands
   qa4sm --help


Authentication
--------------
In order to use the full API, you need to authenticate with QA4SM
via your user token.

1) Go to https://qa4sm.eu/ui/user-profile and request an API token
2) Choose one of the following 2 options to add the token to the
   local file ~/.qa4smapirc to use the API

**Option 1: Manual setup**

Create ``~/.qa4smapirc`` (Linux/MacOs) or ``%USERPROFILE%\.qa4smapirc`` (Windows)
with your credentials:

.. code-block:: ini

   [qa4sm.eu]
   token: your_api_token_here
   username: your_username


**Option 2: Automated setup**

.. code-block:: bash

   qa4sm api setup

This prompts for your username and password and stores your API token in ``~/.qa4smapirc``.

Documentation
-------------

Full documentation is available at https://awst-austria.github.io/qa4sm-api/

Quick Start
===========

Here are some example commands on using the API in a python application.
See the full documentation at https://awst-austria.github.io/qa4sm-api/
for more examples.

.. code-block:: python

   >> from qa4sm_api.client_api import Connection, ValidationConfiguration
   # Initialize connection
   >> conn = Connection()
   Hi, <username>! You're successfully logged in at https://qa4sm.eu/api/!


.. code-block:: python

   # Get a list of available datasets
   >> conn.datasets()[['short_name']]
    Out[10]:
                            short_name
    id
    1                     C3S_combined
    2                          SMAP_L3
    3                            ASCAT
    4                             ISMN
    5                            GLDAS
    6              ESA_CCI_SM_combined
    7                          SMOS_IC
    ...                         ...
   # Get a list of versions for a datasets


.. code-block:: python

   >> conn.versions("C3S_combined")
    Out[6]:
         short_name pretty_name  ... time_range_end geographical_range
    1   C3S_V201706     v201706  ...     2022-10-10               None
    10  C3S_V201812     v201812  ...     2018-12-31               None
    28  C3S_V201912     v201912  ...     2019-12-31               None
    31  C3S_V202012     v202012  ...     2020-12-31               None
    45  C3S_V202212     v202212  ...     2025-07-20               None
    58  C3S_V202312     v202312  ...     2025-07-20               None
    70  C3S_V202505     v202505  ...     2024-12-31               None


.. code-block:: python

   # Download the configuration for a validation run
   >> config = conn.download_configuration("9aeb663b-e24e-4541-8331-6ec3e0318d1f")
   >> print(config.data)
   {'name_tag': 'Test Case  QA4SM_VA_metrics - Test scaling_no_scaling_DEFAULT', 'interval_from': '1978-11-01', 'interval_to': '2024-12-31', 'temporal_matching': 12, 'anomalies_method': 'none', 'anomalies_from': None, 'anomalies_to': None, 'min_lat': 34.0, 'min_lon': -11.2, 'max_lat': 71.6, 'max_lon': 48.3, 'scaling_method': 'none', 'metrics': [{'id': 'tcol', 'value': False}, {'id': 'bootstrap_tcol_cis', 'value': False}, {'id': 'stability_metrics', 'value': False}], 'intra_annual_metrics': {'intra_annual_metrics': False, 'intra_annual_type': '', 'intra_annual_overlap': None}, 'dataset_configs': [{'dataset_id': 1, 'version_id': 70, 'variable_id': 1, 'is_spatial_reference': False, 'is_temporal_reference': True, 'is_scaling_reference': False, 'basic_filters': [1], 'parametrised_filters': []}, {'dataset_id': 4, 'version_id': 69, 'variable_id': 4, 'is_spatial_reference': True, 'is_temporal_reference': False, 'is_scaling_reference': False, 'basic_filters': [1, 2], 'parametrised_filters': [{'id': 18, 'parameters': 'AMMA-CATCH,DAHRA,TAHMO,SD_DEM,CHINA,CTP_SMTMN,HiWATER_EHWSN,HSC_SEOLMACHEON,IIT_KANPUR,KHOREZM,MAQU,MONGOLIA,MySMNet,RUSWET-AGRO,RUSWET-GRASS,RUSWET-VALDAI,SKKU,SW-WHU,KIHS_CMC,KIHS_SMC,VDS,NAQU,NGARI,SMN-SDR,SONTE-China,WIT-Network,AACES,OZNET,SASMAS,BIEBRZA_S-1,CALABRIA,CAMPANIA,FMI,FR_Aqui,GROW,GTK,HOBE,HYDROL-NET_PERUGIA,IMA_CAN1,METEROBS,MOL-RAO,ORACLE,REMEDHUS,RSMN,SMOSMANIA,SWEX_POLAND,TERENO,UDC_SMOS,UMBRIA,UMSUOL,VAS,WEGENERNET,WSMN,HOAL,IPE,COSMOS-UK,LABFLUX,NVE,Ru_CFR,STEMS,TWENTE,XMS-CAT,ARM,AWDN,BNZ-LTER,FLUXNET-AMERIFLUX,ICN,IOWA,PBO_H2O,RISMA,SCAN,SNOTEL,SOILSCAPE,USCRN,USDA-ARS,TxSON,LAB-net,PTSMN'}, {'id': 24, 'parameters': '0.00,0.10'}]}], 'settings_changes': {'filters': [], 'anomalies': False, 'scaling': False, 'variables': [], 'versions': []}}

.. code-block:: python

   # Start a new validation using the local validation configuration
   >> r = conn.start_validation(config)
   # The validation run is now triggered under your user account, check https://qa4sm.eu/ui/my-validations
   >> print(r.status)
   'SCHEDULED'

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
