.. _usage:

=====
Usage
=====

What does this do?
==================

:class:`drf_jsonschema.JSONSchemaField` allows you to express complex data structures
with a JSON Schema. Data that comes in via a POST or PUT request is validated against
the supplied schema.

Once validated, the JSON can be processed further or stored directly in a
database, for instance using :class:`models.JSONField`. When you turn a DRF serializer
that contains :class:`drf_jsonschema.JSONSchemaField` fields into a JSON Schema, their
JSON schemas are embedded in the larger schema that represents the serializer.

What is the point of :class:`drf_jsonschema.SerializerJSONField`? It's very similar to
:class:`drf_jsonschema.JSONSchemaField` and is used to store JSON directly in the
database. Instead of passing in a JSON schema directly, you pass in a serializer class
that is used to validate and convert the incoming JSON. A serializer class is sometimes
more convenient as you can do additional validations on the server that a JSON Schema
cannot do.

:class:`drf_jsonschema.SerializerJSONField` can be converted to a JSON Schema like any
other serializer field, so it integrates with client-side form generation code.

Basic usage of conversion
=========================

.. code-block:: python

    from drf_jsonschema import to_jsonschema
    from rest_framework import serializers


    class MySerializer(serializers.Serializer):
        foo = serializers.CharField()

    json_schema = to_jsonschema(MySerializer())

Basic usage of JSONSchemaField
==============================

.. code-block:: python

    from drf_jsonschema import JSONSchemaField
    from rest_framework import serializers

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
==================================

.. code-block:: python

    from drf_jsonschema import SerializerJSONField
    from rest_framework import serializers


    class MySerializer(serializers.Serializer):
        foo = serializers.IntegerField()


    class MySerializer(serializers.Serializer):
        data = SerializerJSONField(MySerializer)
