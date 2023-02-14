=========
Changelog
=========

1.0.0 (2023-02-14)
==================

First stable version published to PyPI.

Many thanks to Martijn Faassen and ISPNext (https://www.ispnext.com/) for the actual
implementation and ground work.

**Breaking changes**

User upgrading from the Github version should look out for some potentially breaking
changes:

* Schema validation is now done against draft 2020-12 rather than Draft4 of jsonschema
* Validation of the format key may uninentionally be relaxed - typically you need some
  additional libraries for that. The easiest mitigation is installing with the extra:

  .. code-block:: bash

     pip install drf-jsonschema[all-format-validators]

* Support dropped for Django < 3.2 and djangorestframework < 3.13
* Support dropped for Python < 3.8

**Other changes**

* Set up documentation on readthedocs
* Added Github Actions CI pipeline
* Reorganized package structure
* Support Python 3.8-3.10, possibly 3.11 also works (untested)
* Support Django 3.2, 4.0 and 4.1. 4.2 will be added after it's released.
* Cleaned up package metadata
* The public API is now frozen
* Added type hints and mypy checking in CI
