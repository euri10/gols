========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/gols/badge/?style=flat
    :target: https://readthedocs.org/projects/gols
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/euri10/gols.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/euri10/gols

.. |requires| image:: https://requires.io/github/euri10/gols/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/euri10/gols/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/github/euri10/gols/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/euri10/gols?branch=master

.. |codecov| image:: https://codecov.io/github/euri10/gols/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/euri10/gols

.. |landscape| image:: https://landscape.io/github/euri10/gols/master/landscape.svg?style=flat
    :target: https://landscape.io/github/euri10/gols/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg
    :target: https://www.codacy.com/app/euri10/gols
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/euri10/gols/badges/gpa.svg
   :target: https://codeclimate.com/github/euri10/gols
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/gols.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/gols

.. |wheel| image:: https://img.shields.io/pypi/wheel/gols.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/gols

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/gols.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/gols

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/gols.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/gols

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/euri10/gols/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/euri10/gols/


.. end-badges

gols

* Free software: BSD license

Installation
============

::

    pip install gols

Documentation
=============

https://gols.readthedocs.io/

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
