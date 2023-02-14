from jsonschema import Draft202012Validator, FormatChecker


def make_validator(serializer_class):
    return Draft202012Validator(
        serializer_class.json_schema, format_checker=FormatChecker()
    )


def get_valid_for_serializer(serializer_class):
    return serializer_class.valid + getattr(serializer_class, "invalid_by_schema", [])


def get_invalid_for_schema(serializer_class):
    return serializer_class.invalid + getattr(serializer_class, "invalid_by_schema", [])


def pytest_generate_tests(metafunc):
    serializer_classes = getattr(metafunc.module, "registered_serializer_classes", [])
    if "serializer_class" in metafunc.fixturenames:
        if "valid" in metafunc.fixturenames:
            parameters = [
                (serializer_class, data)
                for serializer_class in serializer_classes
                for data in get_valid_for_serializer(serializer_class)
            ]
            metafunc.parametrize("serializer_class,valid", parameters)

        elif "invalid" in metafunc.fixturenames:
            parameters = [
                (serializer_class, data)
                for serializer_class in serializer_classes
                for data in serializer_class.invalid
            ]
            metafunc.parametrize("serializer_class,invalid", parameters)
        elif "expected_json_schema" in metafunc.fixturenames:
            parameters = [
                (serializer_class, serializer_class.json_schema)
                for serializer_class in serializer_classes
            ]
            metafunc.parametrize("serializer_class,expected_json_schema", parameters)
    elif "validator" in metafunc.fixturenames:
        if "valid" in metafunc.fixturenames:
            parameters = [
                (make_validator(serializer_class), data)
                for serializer_class in serializer_classes
                for data in serializer_class.valid
            ]
            metafunc.parametrize("validator,valid", parameters)
        elif "invalid" in metafunc.fixturenames:
            parameters = [
                (make_validator(serializer_class), data)
                for serializer_class in serializer_classes
                for data in get_invalid_for_schema(serializer_class)
            ]
            metafunc.parametrize("validator,invalid", parameters)
