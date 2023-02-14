import pytest
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError
from rest_framework import serializers

from drf_jsonschema import JSONSchemaField, SerializerJSONField, to_jsonschema
from testapp.models import Album, Track

registered_serializer_classes = []


def register(serializer):
    registered_serializer_classes.append(serializer)
    return serializer


@register
class BooleanFieldBasic(serializers.Serializer):
    foo = serializers.BooleanField()

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "boolean", "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": True}, {"foo": False}]
    invalid = [{}, {"foo": "something"}, {"foo": None}]
    # the serializer actually accepts 0 and 1 and "true" and "false"
    # and even "0" and "1"
    invalid_by_schema = [
        {"foo": 0},
        {"foo": 1},
        {"foo": "true"},
        {"foo": "false"},
        {"foo": "0"},
        {"foo": "1"},
    ]


@register
class BooleanFieldNotRequired(serializers.Serializer):
    foo = serializers.BooleanField(required=False)

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "boolean", "title": "Foo"}},
    }

    valid = [{"foo": True}, {"foo": False}, {}]
    invalid = [{"foo": "something"}, {"foo": None}]
    invalid_by_schema = [{"foo": 0}, {"foo": 1}]


@register
class NullBooleanFieldBasic(serializers.Serializer):
    foo = serializers.BooleanField(allow_null=True)

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": ["boolean", "null"], "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": True}, {"foo": False}, {"foo": None}]
    invalid = [{}, {"foo": "something"}, {"foo": 10}]


@register
class CharFieldBasic(serializers.Serializer):
    foo = serializers.CharField()

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "string", "minLength": 1, "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": "something"}]
    invalid = [{}, {"foo": ""}, {"foo": None}, {"foo": False}]
    invalid_by_schema = [{"foo": 1}]


@register
class CharFieldMaxLength(serializers.Serializer):
    foo = serializers.CharField(max_length=10)

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string", "minLength": 1, "maxLength": 10, "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": "x" * 10}]
    invalid = [{}, {"foo": ""}, {"foo": "x" * 11}, {"foo": None}]


@register
class CharFieldAllowNull(serializers.Serializer):
    foo = serializers.CharField(allow_null=True)

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": ["string", "null"], "minLength": 1, "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": "something"}, {"foo": None}]
    invalid = [{}, {"foo": ""}]


@register
class CharFieldNotRequired(serializers.Serializer):
    foo = serializers.CharField(required=False)

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "string", "minLength": 1, "title": "Foo"}},
    }

    valid = [{"foo": "something"}, {}]
    invalid = [{"foo": None}, {"foo": ""}]


@register
class EmailFieldBasic(serializers.Serializer):
    foo = serializers.EmailField()

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string", "minLength": 1, "format": "email", "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": "someone@example.com"}]
    invalid = [{}, {"foo": ""}, {"foo": None}, {"foo": "someone"}]


@register
class RegexFieldBasic(serializers.Serializer):
    foo = serializers.RegexField(regex="^[0-9]+$")

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "string",
                "minLength": 1,
                "pattern": "^[0-9]+$",
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": "1"}, {"foo": "123"}]
    invalid = [{}, {"foo": ""}, {"foo": None}, {"foo": "someone"}, {"foo": "12foo"}]


@register
class SlugFieldBasic(serializers.Serializer):
    foo = serializers.SlugField()

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "string",
                "minLength": 1,
                "pattern": "^[-a-zA-Z0-9_]+$",
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": "1"}, {"foo": "123"}, {"foo": "foo12"}, {"foo": "12something"}]
    invalid = [{}, {"foo": ""}, {"foo": None}, {"foo": "$$$"}, {"foo": "!foo"}]


@register
class URLFieldBasic(serializers.Serializer):
    foo = serializers.URLField()

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string", "minLength": 1, "format": "uri", "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": "http://example.com"}]
    invalid = [{"foo": "something"}, {"foo": "/foo/bar"}, {"foo": ""}]


@register
class IntegerField(serializers.Serializer):
    foo = serializers.IntegerField()

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "integer", "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": 1}]
    invalid = [{}, {"foo": "something"}, {"foo": None}, {"foo": 1.5}, {"foo": "10.5"}]
    # the serializer actually accepts strings
    invalid_by_schema = [{"foo": "10"}]


@register
class IntegerFieldMinValue(serializers.Serializer):
    foo = serializers.IntegerField(min_value=10)

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "integer", "minimum": 10, "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": 10}, {"foo": 11}]
    invalid = [
        {},
        {"foo": "something"},
        {"foo": None},
        {"foo": 1},
        {"foo": 1.5},
        {"foo": 9},
        {"foo": 10.5},
    ]


@register
class IntegerFieldMaxValue(serializers.Serializer):
    foo = serializers.IntegerField(max_value=10)

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "integer", "maximum": 10, "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": 10}, {"foo": 1}]
    invalid = [
        {},
        {"foo": "something"},
        {"foo": None},
        {"foo": 11},
        {"foo": 1.5},
        {"foo": 10.5},
    ]


@register
class FloatField(serializers.Serializer):
    foo = serializers.FloatField()

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "number", "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": 10}, {"foo": 10.5}]
    invalid = [{}, {"foo": "something"}, {"foo": None}]
    # the serializer actually accepts strings
    invalid_by_schema = [{"foo": "1.5"}]


@register
class FloatFieldMinValue(serializers.Serializer):
    foo = serializers.FloatField(min_value=10)

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "number", "minimum": 10, "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": 10}, {"foo": 10.5}]
    invalid = [
        {},
        {"foo": "something"},
        {"foo": None},
        {"foo": 1},
        {"foo": 1.5},
        {"foo": 9.9},
    ]


@register
class FloatFieldMaxValue(serializers.Serializer):
    foo = serializers.FloatField(max_value=10)

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "number", "maximum": 10, "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": 9}, {"foo": 9.5}]
    invalid = [{}, {"foo": "something"}, {"foo": None}, {"foo": 10.5}, {"foo": 11}]


@register
class DecimalField(serializers.Serializer):
    # note that max_digits is explicitly not supported
    # and that we don't support min_value & max_value either due
    # to limitations in JSON-Schema
    foo = serializers.DecimalField(max_digits=None, decimal_places=2)

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "string",
                "pattern": "^\\-?[0-9]*(\\.[0-9]{1,2})?$",
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [
        {"foo": "10"},
        {"foo": "10.5"},
        {"foo": "-1.5"},
        {"foo": "9999999999.5"},
        {"foo": ".5"},
    ]
    invalid = [{}, {"foo": "something"}, {"foo": None}, {"foo": "1.123"}]
    # the serializer actually accepts numbers too
    # (but a string is used by the JSON if coerce_to_string is True,
    # the default)
    invalid_by_schema = [{"foo": 1}, {"foo": 1.5}]


@register
class DateTimeField(serializers.Serializer):
    foo = serializers.DateTimeField()

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string", "format": "date-time", "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": "2017-01-12T16:01:56Z"}]
    invalid = [{}, {"foo": "something"}, {"foo": "2017-14-1T16:01:56Z"}]
    # JSON schema is strict about date-time format, but the serializer
    # accepts shorter formats
    invalid_by_schema = [{"foo": "2017-01-12T16:01"}]


@register
class DateField(serializers.Serializer):
    foo = serializers.DateField()

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "string", "format": "date", "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": "2017-01-12"}]
    invalid = [
        {},
        {"foo": "something"},
        {"foo": "2017-01-12T16:01:00:Z"},
        {"foo": "2017-01"},
        {"foo": "2017-14-01"},
    ]


@register
class ChoiceFieldStrings(serializers.Serializer):
    foo = serializers.ChoiceField(["a", "b", "c"])

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string", "enum": ["a", "b", "c"], "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": "a"}, {"foo": "b"}, {"foo": "c"}]
    invalid = [{}, {"foo": None}, {"foo": ""}, {"foo": "d"}, {"foo": 1}]


@register
class ChoiceFieldStringsAllowBlank(serializers.Serializer):
    foo = serializers.ChoiceField(["a", "b", "c"], allow_blank=True)

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string", "enum": ["", "a", "b", "c"], "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": "a"}, {"foo": "b"}, {"foo": "c"}, {"foo": ""}]
    invalid = [{}, {"foo": None}, {"foo": "d"}, {"foo": 1}]


@register
class ChoiceFieldStringsBlankChoice(serializers.Serializer):
    foo = serializers.ChoiceField(["", "a", "b", "c"])

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string", "enum": ["", "a", "b", "c"], "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": "a"}, {"foo": "b"}, {"foo": "c"}, {"foo": ""}]
    invalid = [{}, {"foo": None}, {"foo": "d"}, {"foo": 1}]


@register
class ChoiceFieldStringsAllowNull(serializers.Serializer):
    foo = serializers.ChoiceField(["a", "b", "c"], allow_null=True)

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": ["null", "string"],
                "enum": [None, "a", "b", "c"],
                "enumNames": ["", "a", "b", "c"],
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": "a"}, {"foo": "b"}, {"foo": "c"}, {"foo": None}]
    invalid = [{}, {"foo": ""}, {"foo": "d"}, {"foo": 1}]


@register
class ChoiceFieldStringsNullChoice(serializers.Serializer):
    foo = serializers.ChoiceField([(None, "Nothing"), "a", "b", "c"], allow_null=True)

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": ["null", "string"],
                "enum": [None, "a", "b", "c"],
                "enumNames": ["Nothing", "a", "b", "c"],
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": "a"}, {"foo": "b"}, {"foo": "c"}, {"foo": None}]
    invalid = [{}, {"foo": ""}, {"foo": "d"}, {"foo": 1}]


@register
class ChoiceFieldDisplayNames(serializers.Serializer):
    foo = serializers.ChoiceField([("a", "A"), ("b", "B"), ("c", "C")])

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "string",
                "enum": ["a", "b", "c"],
                "enumNames": ["A", "B", "C"],
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": "a"}, {"foo": "b"}, {"foo": "c"}]
    invalid = [{}, {"foo": None}, {"foo": ""}, {"foo": "d"}, {"foo": 1}]


@register
class ChoiceFieldInts(serializers.Serializer):
    foo = serializers.ChoiceField([1, 2, 3])

    json_schema = {
        "type": "object",
        "properties": {"foo": {"type": "integer", "enum": [1, 2, 3], "title": "Foo"}},
        "required": ["foo"],
    }

    valid = [{"foo": 1}, {"foo": 2}, {"foo": 3}]
    invalid = [{}, {"foo": None}, {"foo": ""}, {"foo": "d"}, {"foo": 4}]


@register
class ChoiceFieldIntsDisplaynames(serializers.Serializer):
    foo = serializers.ChoiceField([(1, "One"), (2, "Two"), (3, "Three")])

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "integer",
                "enum": [1, 2, 3],
                "enumNames": ["One", "Two", "Three"],
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": 1}, {"foo": 2}, {"foo": 3}]
    invalid = [{}, {"foo": None}, {"foo": ""}, {"foo": "d"}, {"foo": 4}]


@register
class ChoiceFieldFloats(serializers.Serializer):
    foo = serializers.ChoiceField([1.1, 2.1, 3.1])

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "number", "enum": [1.1, 2.1, 3.1], "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": 1.1}, {"foo": 2.1}, {"foo": 3.1}]
    invalid = [{}, {"foo": None}, {"foo": ""}, {"foo": "d"}, {"foo": 4}, {"foo": 1.2}]


@register
class ChoiceFieldMixed(serializers.Serializer):
    foo = serializers.ChoiceField(["a", 1])

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": ["integer", "string"], "enum": ["a", 1], "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": 1}, {"foo": "a"}]
    invalid = [{}, {"foo": None}, {"foo": "b"}, {"foo": 3}]


@register
class ChoiceFieldBool(serializers.Serializer):
    foo = serializers.ChoiceField([False, True])

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "boolean", "enum": [False, True], "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": False}, {"foo": True}]
    invalid = [{}, {"foo": None}, {"foo": ""}, {"foo": "d"}, {"foo": 1}]


class SubSerializer(serializers.Serializer):
    foo = serializers.IntegerField()
    bar = serializers.CharField()


@register
class SubSerializerBasic(serializers.Serializer):
    sub = SubSerializer(label="Sub serializer!")
    another = serializers.CharField()

    json_schema = {
        "type": "object",
        "properties": {
            "sub": {
                "type": "object",
                "title": "Sub serializer!",
                "properties": {
                    "foo": {"type": "integer", "title": "Foo"},
                    "bar": {"type": "string", "minLength": 1, "title": "Bar"},
                },
                "required": ["foo", "bar"],
            },
            "another": {"type": "string", "minLength": 1, "title": "Another"},
        },
        "required": ["sub", "another"],
    }

    valid = [{"sub": {"foo": 3, "bar": "BAR"}, "another": "HALLO"}]
    invalid = [
        {},
        {"sub": "what", "another": "HALLO"},
        {"sub": {"foo": 3, "bar": ""}, "another": "HALLO"},
    ]


@register
class SubSerializerMany(serializers.Serializer):
    sub = SubSerializer(many=True)
    another = serializers.CharField()

    json_schema = {
        "type": "object",
        "properties": {
            "sub": {
                "type": "array",
                "title": "Sub",
                "items": {
                    "type": "object",
                    "properties": {
                        "foo": {"type": "integer", "title": "Foo"},
                        "bar": {"type": "string", "minLength": 1, "title": "Bar"},
                    },
                    "required": ["foo", "bar"],
                },
            },
            "another": {"type": "string", "minLength": 1, "title": "Another"},
        },
        "required": ["sub", "another"],
    }

    valid = [
        {"sub": [{"foo": 3, "bar": "BAR"}], "another": "HALLO"},
        {"sub": [], "another": "HALLO"},
    ]
    invalid = [
        {},
        {"sub": "what", "another": "HALLO"},
        {"sub": [{"foo": 3, "bar": ""}], "another": "HALLO"},
    ]


@register
class SubSerializerManyNotAllowEmpty(serializers.Serializer):
    sub = SubSerializer(many=True, allow_empty=False)
    another = serializers.CharField()

    json_schema = {
        "type": "object",
        "properties": {
            "sub": {
                "type": "array",
                "title": "Sub",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "foo": {"type": "integer", "title": "Foo"},
                        "bar": {"type": "string", "minLength": 1, "title": "Bar"},
                    },
                    "required": ["foo", "bar"],
                },
            },
            "another": {"type": "string", "minLength": 1, "title": "Another"},
        },
        "required": ["sub", "another"],
    }

    valid = [{"sub": [{"foo": 3, "bar": "BAR"}], "another": "HALLO"}]
    invalid = [
        {},
        {"sub": [], "another": "HALLO"},
        {"sub": "what", "another": "HALLO"},
        {"sub": [{"foo": 3, "bar": ""}], "another": "HALLO"},
    ]


@register
class ListFieldBasic(serializers.Serializer):
    foo = serializers.ListField(child=serializers.IntegerField())

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "array", "items": {"type": "integer"}, "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": [1, 2, 3]}, {"foo": []}]
    invalid = [{}, {"foo": None}, {"foo": 1}, {"foo": ""}]


class IntegerListField(serializers.ListField):
    child = serializers.IntegerField()


@register
class ListFieldDeclarative(serializers.Serializer):
    foo = IntegerListField()

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "array", "items": {"type": "integer"}, "title": "Foo"}
        },
        "required": ["foo"],
    }

    valid = [{"foo": [1, 2, 3]}, {"foo": []}]
    invalid = [{}, {"foo": None}, {"foo": 1}, {"foo": ""}]


@register
class ListFieldMinLength(serializers.Serializer):
    foo = serializers.ListField(child=serializers.IntegerField(), min_length=1)

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 1,
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": [1, 2, 3]}, {"foo": [1]}]
    invalid = [{}, {"foo": None}, {"foo": 1}, {"foo": ""}, {"foo": []}]


@register
class ListFieldMaxLength(serializers.Serializer):
    foo = serializers.ListField(child=serializers.IntegerField(), max_length=2)

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "array",
                "items": {"type": "integer"},
                "maxItems": 2,
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": [1, 2]}, {"foo": []}]
    invalid = [{}, {"foo": None}, {"foo": 1}, {"foo": ""}, {"foo": [1, 2, 3]}]


@register
class ListFieldObject(serializers.Serializer):
    foo = serializers.ListField(child=SubSerializer())

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "array",
                "title": "Foo",
                "items": {
                    "type": "object",
                    "properties": {
                        "foo": {"type": "integer", "title": "Foo"},
                        "bar": {"type": "string", "minLength": 1, "title": "Bar"},
                    },
                    "required": ["foo", "bar"],
                },
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": [{"foo": 1, "bar": "BAR"}, {"foo": 2, "bar": "BAR2"}]}]
    invalid = [
        {},
        {"foo": None},
        {"foo": [{"foo": 1, "bar": False}]},
        {"foo": [{"foo": 1}]},
    ]


@register
class DictFieldBasic(serializers.Serializer):
    foo = serializers.DictField(child=serializers.IntegerField())

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "object",
                "additionalProperties": {"type": "integer"},
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": {"a": 1, "b": 2}}, {"foo": {}}]
    invalid = [
        {},
        {"foo": None},
        {"foo": 1},
        {"foo": {"a": "nointeger"}},
    ]


@register
class DictFieldObject(serializers.Serializer):
    foo = serializers.DictField(child=SubSerializer())

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "foo": {"type": "integer", "title": "Foo"},
                        "bar": {"type": "string", "minLength": 1, "title": "Bar"},
                    },
                    "required": ["foo", "bar"],
                },
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": {"a": {"foo": 1, "bar": "BAR"}, "b": {"foo": 2, "bar": "BAR2"}}}]
    invalid = [
        {},
        {"foo": None},
        {"foo": 1},
        {"foo": {"a": {"foo": 1, "bar": False}}},
    ]


@register
class JSONSchemaFieldBasic(serializers.Serializer):
    foo = JSONSchemaField(
        schema={"type": "object", "properties": {"a": {"type": "integer"}}}
    )

    # FIXME: is it correct to add the title here?
    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "object",
                "properties": {"a": {"type": "integer"}},
                "title": "Foo",
            }
        },
        "required": ["foo"],
    }

    valid = [{"foo": {"a": 1}}, {"foo": {}}]
    invalid = [
        {},
        {"foo": None},
        {"foo": 1},
        {"foo": {"a": "nointeger"}},
    ]


@register
class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("album_name", "artist")

    json_schema = {
        "type": "object",
        "properties": {
            "album_name": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Album Name",  # note we take title from model field
            },
            "artist": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Artist",
            },
        },
        "required": ["album_name", "artist"],
    }

    valid = []
    invalid = []


@register
class ModelSerializerWithRelated(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("album_name", "artist", "tracks")

    json_schema = {
        "type": "object",
        "properties": {
            "album_name": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Album Name",
            },
            "artist": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Artist",
            },
            "tracks": {
                "type": "array",
                "title": "Tracks",
                "items": {"type": "integer"},
            },
        },
        "required": ["album_name", "artist", "tracks"],
    }

    valid = []
    invalid = []


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ("order", "title", "duration")


@register
class ModelSerializerWithRelatedSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ("album_name", "artist", "tracks")

    json_schema = {
        "type": "object",
        "properties": {
            "album_name": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Album Name",
            },
            "artist": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Artist",
            },
            "tracks": {
                "type": "array",
                "title": "Tracks",
                "items": {
                    "type": "object",
                    "properties": {
                        "order": {
                            "type": "integer",
                            "title": "Order",
                            "description": "The order of the track",
                        },
                        "title": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 100,
                            "title": "Title",
                        },
                        "duration": {"type": "integer", "title": "Duration"},
                    },
                    "required": ["order", "title", "duration"],
                },
            },
        },
        "required": ["album_name", "artist", "tracks"],
    }

    valid = []
    invalid = []


@register
class PrimaryKeyRelatedField(serializers.ModelSerializer):
    # album is a foreign key
    class Meta:
        model = Track
        fields = ("album", "order", "title", "duration")

    json_schema = {
        "type": "object",
        "properties": {
            "album": {"type": "integer", "title": "Album"},
            "order": {
                "type": "integer",
                "title": "Order",
                "description": "The order of the track",
            },
            "title": {
                "type": "string",
                "title": "Title",
                "maxLength": 100,
                "minLength": 1,
            },
            "duration": {"type": "integer", "title": "Duration"},
        },
        "required": ["album", "order", "title", "duration"],
    }

    valid = []
    invalid = []


@register
class StringRelatedField(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ("album_name", "artist", "tracks")

    json_schema = {
        "type": "object",
        "properties": {
            "album_name": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Album Name",
            },
            "artist": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Artist",
            },
            "tracks": {"type": "array", "title": "Tracks", "items": {"type": "string"}},
        },
        "required": ["album_name", "artist", "tracks"],
    }

    valid = []
    invalid = []


@register
class HyperlinkedRelatedField(serializers.ModelSerializer):
    tracks = serializers.HyperlinkedRelatedField(
        many=True, queryset=Track.objects, view_name="fake"
    )

    class Meta:
        model = Album
        fields = ("album_name", "artist", "tracks")

    json_schema = {
        "type": "object",
        "properties": {
            "album_name": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Album Name",
            },
            "artist": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Artist",
            },
            "tracks": {
                "type": "array",
                "title": "Tracks",
                "items": {"type": "string", "format": "uri"},
            },
        },
        "required": ["album_name", "artist", "tracks"],
    }

    valid = []
    invalid = []


@register
class SlugRelatedField(serializers.ModelSerializer):
    tracks = serializers.SlugRelatedField(
        many=True, queryset=Track.objects, slug_field="title"
    )

    class Meta:
        model = Album
        fields = ("album_name", "artist", "tracks")

    json_schema = {
        "type": "object",
        "properties": {
            "album_name": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Album Name",
            },
            "artist": {
                "type": "string",
                "maxLength": 100,
                "minLength": 1,
                "title": "Artist",
            },
            "tracks": {
                "type": "array",
                "title": "Tracks",
                "items": {"type": "string", "pattern": "^[-a-zA-Z0-9_]+$"},
            },
        },
        "required": ["album_name", "artist", "tracks"],
    }

    valid = []
    invalid = []


@register
class ReadOnlyIsNotConverted(serializers.Serializer):
    foo = serializers.CharField(read_only=True)

    json_schema = {"type": "object", "properties": {}}

    valid = [{"foo": "something"}, {}, {"foo": ""}, {"foo": None}, {"foo": False}]
    invalid = []


@register
class HelpTextIsDescription(serializers.Serializer):
    foo = serializers.CharField(help_text="This is really a foo")

    json_schema = {
        "type": "object",
        "properties": {
            "foo": {
                "type": "string",
                "minLength": 1,
                "title": "Foo",
                "description": "This is really a foo",
            }
        },
        "required": ["foo"],
    }

    valid = []
    invalid = []


class SJFSerializer(serializers.Serializer):
    foo = serializers.IntegerField()


@register
class SerializerJSON(serializers.Serializer):
    json = SerializerJSONField(SJFSerializer)

    json_schema = {
        "type": "object",
        "properties": {
            "json": {
                "type": "object",
                "title": "Json",
                "properties": {"foo": {"type": "integer", "title": "Foo"}},
                "required": ["foo"],
            }
        },
        "required": ["json"],
    }

    valid = [{"json": {"foo": 1}}]
    invalid = [{"json": {"foo": "Not a number"}}]
    invalid_by_schema = [{"json": {"foo": "1"}}]


def test_correct_generated_schema(serializer_class, expected_json_schema):
    generated_json_schema = to_jsonschema(serializer_class())
    assert generated_json_schema == expected_json_schema


def test_valid_by_serializer(serializer_class, valid):
    serializer_class(data=valid).run_validation(valid)


def test_invalid_by_serializer(serializer_class, invalid):
    with pytest.raises(serializers.ValidationError):
        serializer_class(data=invalid).run_validation(invalid)


def test_valid_by_jsonschema(validator, valid):
    validator.validate(valid)


def test_invalid_by_jsonschema(validator, invalid):
    with pytest.raises(JSONSchemaValidationError):
        validator.validate(invalid)
