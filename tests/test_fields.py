import pytest
from rest_framework import serializers

from drf_jsonschema_serializer import JSONSchemaField, SerializerJSONField

schema = {
    "type": "object",
    "properties": {"a": {"type": "string"}, "b": {"type": "number"}},
}


format_schema = {
    "type": "object",
    "properties": {"a": {"type": "string", "format": "email"}},
}


def test_valid_json_field():
    field = JSONSchemaField(schema=schema)
    assert field.to_internal_value({"a": "foo", "b": 3.1}) == {"a": "foo", "b": 3.1}


def test_invalid_json_field():
    field = JSONSchemaField(schema=schema)
    with pytest.raises(serializers.ValidationError) as e:
        field.run_validation({"a": "foo", "b": "nonumber"})
    assert e.value.detail == ["'nonumber' is not of type 'number'"]


def test_json_field_valid_format_check():
    field = JSONSchemaField(schema=format_schema)
    assert field.to_internal_value({"a": "foo@example.com"}) == {"a": "foo@example.com"}


def test_json_field_invalid_format_check():
    field = JSONSchemaField(schema=format_schema)
    with pytest.raises(serializers.ValidationError) as e:
        field.run_validation({"a": "noemail"})
    assert e.value.detail == ["'noemail' is not a 'email'"]


def test_json_field_invalid_format_check_but_format_checking_disabled():
    field = JSONSchemaField(schema=format_schema, format_checker=None)
    assert field.to_internal_value({"a": "noemail"}) == {"a": "noemail"}


def test_valid_json_field_in_serializer():
    class TestSerializer(serializers.Serializer):
        json = JSONSchemaField(schema=schema)

    serializer = TestSerializer(data={"json": {"a": "foo", "b": 3.1}})
    assert serializer.is_valid()
    assert serializer.validated_data == {"json": {"a": "foo", "b": 3.1}}


def test_serialize_json_field_in_serializer():
    class TestSerializer(serializers.Serializer):
        json = JSONSchemaField(schema=schema)

    serializer = TestSerializer(data={"json": {"a": "foo", "b": 3.1}})
    assert serializer.is_valid()
    assert serializer.data == {"json": {"a": "foo", "b": 3.1}}


def test_invalid_json_field_in_serializer():
    class TestSerializer(serializers.Serializer):
        json = JSONSchemaField(schema=schema)

    serializer = TestSerializer(data={"json": {"a": "foo", "b": "nonumber"}})
    assert not serializer.is_valid()
    assert serializer.validated_data == {}


def test_serializer_json_field():
    class MySerializer(serializers.Serializer):
        foo = serializers.IntegerField()

    class TestSerializer(serializers.Serializer):
        json = SerializerJSONField(MySerializer)

    serializer = TestSerializer(data={"json": {"foo": 42}})
    assert serializer.is_valid()
    assert dict(serializer.validated_data) == {"json": {"foo": 42}}

    serializer = TestSerializer(data={"json": {"foo": "Not a number!"}})
    assert not serializer.is_valid()

    serializer = TestSerializer(data={"json": {"foo": "44"}})
    assert serializer.is_valid()
    assert dict(serializer.validated_data) == {"json": {"foo": 44}}


def test_serializer_json_field_error():
    class MySerializer(serializers.Serializer):
        foo = serializers.IntegerField()

    field = SerializerJSONField(MySerializer)
    with pytest.raises(serializers.ValidationError) as e:
        field.run_validation({"foo": "Not a number!"})
    # FIXME: is this really the right structure for errors in this
    # case?
    assert e.value.detail == {"foo": ["A valid integer is required."]}


def test_serializer_json_field_decimal():
    class MySerializer(serializers.Serializer):
        foo = serializers.DecimalField(None, 2)

    class TestSerializer(serializers.Serializer):
        json = SerializerJSONField(MySerializer)

    serializer = TestSerializer(data={"json": {"foo": "42.1"}})
    assert serializer.is_valid()
    assert dict(serializer.validated_data) == {"json": {"foo": "42.10"}}

    serializer = TestSerializer(data={"json": {"foo": "Not a number!"}})
    assert not serializer.is_valid()
