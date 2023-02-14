.. drf-jsonschema documentation master file, created by
   sphinx-quickstart on Tue Feb 14 17:29:29 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django REST Framework JSON Schema
=================================

|build-status| |coverage| |linting| |black| |docs|

|python-versions| |django-versions| |pypi-version|

JSON Schema support for Django REST Framework

Overview
========

drf-jsonschema is a library built around Django REST Framework. It does the
following:

* Convert a DRF serializer into a JSON Schema.

* Provides ``JSONSchemaField`` that can validate JSON data according to
  a JSON schema.

* Provides a ``SerializerJSONField`` that can validate JSON data according to
  a serializer for a field.

This lets you use client-side form libraries such as react-jsonschema-form to
generate a web form from a serializer. This way you can use the same schema for
client-side form generation and validation as you use for REST service input
validation.

Credits and roadmap
===================

Many thanks to https://github.com/isprojects for the initial work on this library.
As of September 2021, Maykin Media has taken up maintenance of this package after
transferring it from isprojects. See the issues on Github for the roadmap.

See also CREDITS.txt for a full history of authorship.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   usage
   reference
   developers
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |build-status| image:: https://github.com/maykinmedia/drf-jsonschema/workflows/ci/badge.svg
    :target: https://github.com/maykinmedia/drf-jsonschema/actions/workflows/ci.yml
    :alt: Tests and PyPI publishing

.. |linting| image:: https://github.com/maykinmedia/drf-jsonschema/workflows/code-quality/badge.svg
    :target: https://github.com/maykinmedia/drf-jsonschema/actions/workflows/code-quality.yml
    :alt: Linting and code quality

.. |coverage| image:: https://codecov.io/gh/maykinmedia/drf-jsonschema/branch/main/graph/badge.svg
    :target: https://app.codecov.io/gh/maykinmedia/drf-jsonschema
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/drf-jsonschema.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/drf-jsonschema.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/drf-jsonschema.svg
    :target: https://pypi.org/project/drf-jsonschema/

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |docs| image:: https://readthedocs.org/projects/drf-jsonschema/badge/?version=latest
    :target: https://drf-jsonschema.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. _documentation: https://drf-jsonschema.readthedocs.io/
