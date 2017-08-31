Django REST Framework JSON Schema support
=========================================

What does this do?
------------------

drf_jsonschema is a library built around Django REST Framework. It does the
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

``JSONSchemaField`` allows you to express complex data structures with a JSON
Schema. Data that comes in via a POST or PUT request is validated against the
supplied schema.

Once validated, the JSON can be processed further or stored directly in a
database, for instance using the PostgreSQL JSONField. When you turn a DRF
serializer that contains ``JSONSchemaField`` fields into a JSON Schema, their
JSON schemas are embedded in the larger schema that represents the serializer.

What is the point of ``SerializerJSONField``? It's very similar to
``JSONSchemaField`` and is used to store JSON directly in the database. Instead
of passing in a JSON schema directly, you pass in a serializer class that is
used to validate and convert the incoming JSON. A serializer class is sometimes
more convenient as you can do additional validations on the server that a JSON
Schema cannot do.

``SerializerJSONField`` can be converted to a JSON Schema like any other
serializer field, so it integrates with client-side form generation code.


Basic usage of conversion
-------------------------

::

    from rest_framework import serializers
    from drf_jsonschema import to_jsonschema

    class MySerializer(serializers.Serializer):
        foo = serializers.CharField()

    json_schema = to_jsonschema(MySerializer())

Basic usage of JSONSchemaField
------------------------------

::

    from rest_framework import serializers
    from drf_jsonschema import JSONSchemaField

    my_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string" }
        },
        "required": ["foo"]
    }

    class MySerializer(serializers.Serializer)
         data = JSONSchemaField(my_schema)

This serializer can then be converted into a larger JSON schema that
embeds the given schema using ``to_jsonschema`` as above.

Basic usage of SerializerJSONField
----------------------------------

::

    from rest_framework import serializers
    from drf_jsonschema import SerializerJSONField

    class MySerializer(serializers.Serializer):
        foo = serializers.IntegerField()

    class MySerializer(serializers.Serializer):
        data = SerializerJSONField(MySerializer)

Conversion limitations
----------------------

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

How to install
--------------

::

  $ pip install drf_jsonschema

Hacking on it
-------------

First install in a working env::

$ pip install -r develop_requirements

You can run the tests::

  py.test

Not yet supported are
---------------------

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

* Python 2 support.

Contributions are welcome!
