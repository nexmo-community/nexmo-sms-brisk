========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |requires|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|



.. |requires| image:: https://requires.io/github/aaronbassett/nexmo-sms-brisk/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/aaronbassett/nexmo-sms-brisk/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/brisk.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/brisk

.. |commits-since| image:: https://img.shields.io/github/commits-since/aaronbassett/nexmo-sms-brisk/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/aaronbassett/nexmo-sms-brisk/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/brisk.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/brisk

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/brisk.svg
    :alt: Supported versions
    :target: https://pypi.org/project/brisk

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/brisk.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/brisk


.. end-badges

Rapid replies and new SMS messages from templates

* Free software: MIT license

Installation
============

::

    pip install brisk

Documentation
=============


To use the project:

.. code-block:: python

    import brisk
    brisk.longest()


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
