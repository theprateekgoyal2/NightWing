from jsonschema import validate, ValidationError
import pytest

def assert_response(response, expected_status, expected_output, schema_data=None):
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
    if expected_output == 'SchemaData':
        if schema_data:
            validate_schema(instance_data=response.json(), schema_value=schema_data)
            return
    else: 
        assert response.json() == expected_output, f"Expected output {expected_output}, got {response.json()}"


def validate_schema(instance_data, schema_value):
    try:
        validate(instance=instance_data, schema=schema_value)
        assert True
    except ValidationError as e:
        pytest.fail(f"JSON response does not match schema: {e}")