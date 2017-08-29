import pytest
from rest_framework import serializers
from drf_jsonschema import JSONSchemaField

schema = {
    'type': 'object',
    'properties': {
        'a': {
            'type': 'string'
        },
        'b': {
            'type': 'number'
        }
    }
}


format_schema = {
    'type': 'object',
    'properties': {
        'a': {
            'type': 'string',
            'format': 'email'
        }
    }
}


def test_valid_json_field():
    field = JSONSchemaField(schema=schema)
    assert field.to_internal_value({'a': 'foo', 'b': 3.1}) == {
        'a': 'foo', 'b': 3.1}


def test_invalid_json_field():
    field = JSONSchemaField(schema=schema)
    with pytest.raises(serializers.ValidationError) as e:
        field.run_validation({'a': 'foo', 'b': 'nonumber'})
    assert e.value.detail == ["'nonumber' is not of type 'number'"]


def test_json_field_valid_format_check():
    field = JSONSchemaField(schema=format_schema)
    assert field.to_internal_value({'a': 'foo@example.com'}) == {
        'a': 'foo@example.com'}


def test_json_field_invalid_format_check():
    field = JSONSchemaField(schema=format_schema)
    with pytest.raises(serializers.ValidationError) as e:
        field.run_validation({'a': 'noemail'})
    assert e.value.detail == ["'noemail' is not a 'email'"]


def test_json_field_invalid_format_check_but_format_checking_disabled():
    field = JSONSchemaField(schema=format_schema, format_checker=None)
    assert field.to_internal_value({'a': 'noemail'}) == {
        'a': 'noemail'}


def test_valid_json_field_in_serializer():
    class TestSerializer(serializers.Serializer):
        json = JSONSchemaField(schema=schema)
    serializer = TestSerializer(data={'json': {'a': 'foo', 'b': 3.1}})
    assert serializer.is_valid()
    assert serializer.validated_data == {
        'json': {'a': 'foo', 'b': 3.1}
    }


def test_serialize_json_field_in_serializer():
    class TestSerializer(serializers.Serializer):
        json = JSONSchemaField(schema=schema)
    serializer = TestSerializer(data={'json': {'a': 'foo', 'b': 3.1}})
    assert serializer.is_valid()
    assert serializer.data == {'json': {'a': 'foo', 'b': 3.1}}


def test_invalid_json_field_in_serializer():
    class TestSerializer(serializers.Serializer):
        json = JSONSchemaField(schema=schema)
    serializer = TestSerializer(data={'json': {'a': 'foo', 'b': 'nonumber'}})
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
