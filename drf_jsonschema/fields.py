from rest_framework import serializers
from jsonschema import Draft4Validator, FormatChecker
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError
from .convert import to_jsonschema

_DEFAULT = object()


class JSONSchemaField(serializers.Field):
    """A field that validates incoming data against a JSON Schema.

    This field takes incoming data as Python data structures (objects,
    lists, strings, numbers, bool, None) that is the equivalent of JSON.
    After validation the same structure is returned.

    The data can then be stored in a native JSON field (for instance a
    PostgreSQL ``django.contrib.postgres.JSONField``).
    """

    def __init__(self, schema, types=(), resolver=None,
                 format_checker=_DEFAULT, *args, **kw):
        super(JSONSchemaField, self).__init__(*args, **kw)
        Draft4Validator.check_schema(schema)
        self.schema = schema
        if format_checker is _DEFAULT:
            format_checker = FormatChecker()
        self.validator = Draft4Validator(schema, types, resolver,
                                         format_checker)

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        try:
            self.validator.validate(data)
        except JSONSchemaValidationError as e:
            raise serializers.ValidationError(e.message)

        return data


class SerializerJSONField(serializers.Field):
    """A field that stores JSON but uses a serializer to validate.
    """
    def __init__(self, serializer_class, *args, **kw):
        super(SerializerJSONField, self).__init__(*args, **kw)
        self.serializer_class = serializer_class
        self.schema = to_jsonschema(serializer_class())

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            serializer.run_validation(data)
        return serializer.validated_data
