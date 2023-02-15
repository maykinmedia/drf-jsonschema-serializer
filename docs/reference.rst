====================
Python API reference
====================

Conversion limitations
======================

We do our best to convert the DRF serializer into a JSON Schema, but not
all constructs of the DRF serializer can be fully converted. We try to
fail fast in such cases, but we don't detect everything yet. In addition
the JSON Schema is often more strict than what the DRF serializer accepts.

Here is an overview of the known differences:

* CharField: The serializer accepts numbers and converts them to strings,
  but the JSON schema only accepts strings.

* RegexField: The Python regex is literally exported to the JSON Schema,
  without taking into account any differences between Python regexes and
  the regexes supported by JSON Schema.

* BooleanField and NullBooleanField: the serializer accepts values such
  as 0, 1, "0", "1", "true", "false" in addition to the JSON ``true`` and
  ``false``. JSON Schema is strict and only accepts the real ``true``
  and ``false``.

* FloatField and IntegerField: these accept strings such as "10" that can
  be converted into a number. JSON Schema is strict and only accepts JSON
  numbers.

* DecimalField: these are converted to a "string" property with a regex pattern.
  ``max_digits`` is not supported. ``coerce_to_string`` must always be ``True``.
  Not converted are `min_value`` and ``max_value``.

* DateTimeField and DateField: only the default date/time formats are supported.

* ChoiceField: only basic datatypes (string, float, int, bool, None) are
  accepted.

Public API
==========

.. automodule:: drf_jsonschema_serializer
    :members:

Schema validation strictness
============================

:class:`drf_jsonschema_serializer.JSONSchemaField` performs schema validation to a varying degree
of strictness. Many format validations are implemented via additional, optional
libraries. For a reference of builtins, see ``jsonschema._formats`` and look for the
attempted imports.

For convenience sake, we define an extra package that installs all of them (at the time
of writing):

.. code-block::

    pip install drf-jsonschema[all-format-validators]

Alternatively, you can set these up for yourself and use this list as inspiration.

Without some of these packages, an invalid URI format would not raise a validation
error, for example.

Unsupported
===========

Contributions welcome to add support!

Fields
------

* UUIDField
* IPAddressField
* FileField
* FilePathField
* TimeField
* DurationField
* MultipleChoiceField
* ImageField
* JSONField (but see JSONSchemaField)
* ReadOnlyField
* HiddenField
* ModelField
* SerializerMethodField
* HyperlinkedIdentityField

Known todos
-----------

* PrimaryKeyRelatedField: support pk_field option
