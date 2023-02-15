=========================================
Django REST Framework JSON Schema support
=========================================

:Version: 1.0.0
:Source: https://github.com/maykinmedia/drf-jsonschema-serializer
:Keywords: django, rest, jsonschema

|build-status| |coverage| |linting| |black| |docs|

|python-versions| |django-versions| |pypi-version|

JSON Schema support for Django REST Framework

Overview
========

drf-jsonschema-serializer is a library built around Django REST Framework. It does the
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

See the documentation_ for getting started and usage examples.

Credits and roadmap
===================

Many thanks to https://github.com/isprojects for the initial work on this library.
As of September 2021, Maykin Media has taken up maintenance of this package after
transferring it from isprojects. See the issues on Github for the roadmap.

See also CREDITS.txt for a full history of authorship.

.. |build-status| image:: https://github.com/maykinmedia/drf-jsonschema-serializer/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/maykinmedia/drf-jsonschema-serializer/actions/workflows/ci.yml
    :alt: Tests and PyPI publishing

.. |linting| image:: https://github.com/maykinmedia/drf-jsonschema-serializer/actions/workflows/code-quality.yml/badge.svg
    :target: https://github.com/maykinmedia/drf-jsonschema-serializer/actions/workflows/code-quality.yml
    :alt: Linting and code quality

.. |coverage| image:: https://codecov.io/gh/maykinmedia/drf-jsonschema-serializer/branch/main/graph/badge.svg
    :target: https://app.codecov.io/gh/maykinmedia/drf-jsonschema-serializer
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/drf-jsonschema-serializer.svg

.. |django-versions| image:: https://img.shields.io/pypi/frameworkversions/django/drf-jsonschema-serializer.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/drf-jsonschema-serializer.svg
    :target: https://pypi.org/project/drf-jsonschema-serializer/

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |docs| image:: https://readthedocs.org/projects/drf-jsonschema-serializer/badge/?version=latest
    :target: https://drf-jsonschema-serializer.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. _documentation: https://drf-jsonschema.readthedocs.io/
