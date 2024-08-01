import pytest
import requests
import json
from jsonschema import validate, ValidationError
import os

# POST-API
test_data_1 = [
                # Case: Valid category creation
                ({"name": "Movie"}, {"message": "Category created successfully"}, 201),
                ({"name": "Show"}, {"message": "Category created successfully"}, 201),
                # # Case: invalid JSON
                # ("Invalid Json", {"message": "Invalid JSON"}, 400),
                # Case: missing request body
                ({}, {"message": "Request body is missing"}, 400),
                # Case: missing name field
                ({"another_field": "value"}, {"message": "Name field missing."}, 400),
                # Case: empty name field
                ({"name": ""}, {"message": "Name field can't be empty."}, 400),
                # Case: duplicate category
                ({"name": "Movie"}, {"message": "Category already exists."}, 400)
            ]

@pytest.mark.parametrize('payload, expected_output, expected_status_code', test_data_1)
def test_create_category_api(payload, expected_output, expected_status_code):
    
    headers = {
        'Content-Type': 'application/json'
    }

    # Schema when data is added
    created_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        }
    }

    domain = os.environ.get('LOCAL_HOST', 'http://127.0.0.1:5000')

    url_to_hit = f"{domain}/api/categories"
    req = requests.session()

    if isinstance(payload, dict):
        payload = json.dumps(payload)
        response = req.post(url_to_hit, headers=headers, data=payload)
    
    assert response.status_code == expected_status_code
    assert response.json() == expected_output

# GET-API
def test_retrieve_category_api():
    # Define the JSON schema to be compared
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "totalItems": {"type": "integer"}
            },
            "required": ["id", "name", "totalItems"]
        }
    }
    
    domain = os.environ['LOCAL_HOST']
    url_to_hit = f"{domain}/api/categories"
    req = requests.session()
    retrieved_items = req.get(url_to_hit)

    if retrieved_items.status_code == 200:
        try:
            validate(instance=retrieved_items.json(), schema=schema)
            assert True
        except ValidationError as e:
            pytest.fail(f"JSON response does not match schema: {e}")
        finally: 
            assert isinstance(retrieved_items.json(), list), "Response is not a list"
            for item in retrieved_items.json():
                assert isinstance(item['id'], int), "ID is not an integer"
                assert isinstance(item['name'], str), "Name is not a string"
                assert isinstance(item['totalItems'], int), "TotalItems is not an integer"

    elif retrieved_items.status_code == 404:
        error_response = retrieved_items.json()
        assert "message" in error_response, "Error response does not contain 'message'"
        assert error_response["message"] == "No categories found", "Error message does not match"
    
    else:
        pytest.fail(f"Unexpected status code: {retrieved_items.status_code}")

# PUT-API
test_data_2 = [
                # Case: Valid category updation
                ({"name": "Movies"}, 1, {"message":"Item edited successfully"}, 202),
                ({"name": "Shows"}, 2, {"message":"Item edited successfully"}, 202),
                # # Case: invalid JSON
                # ("Invalid Json", {"message": "Invalid JSON"}, 400),
                
                # Case: Invalid Id
                ({"name": "New Category Updated"}, 3, {"message":"No item found"}, 404),
                
                # Case: Id missing
                ({"name": "New Category Updated"}, 'id', {"message":"ID parameter is missing"}, 400),
                
                # Case: missing request body
                ({}, 1, {"message": "Request body is missing"}, 400),
                
                # Case: missing name field
                ({"another_field": "value"}, 1, {"message": "Name field missing."}, 400),
                
                # Case: empty name field
                ({"name": ""}, 1, {"message": "Name field can't be empty."}, 400),
                
                # Case: duplicate category
                ({"name": "Movies"}, 1, {"message": "Category already exists."}, 400)
            ]

@pytest.mark.parametrize('payload, id, expected_output, expected_status_code', test_data_2)
def test_update_category_api(payload, id, expected_output, expected_status_code):
    
    headers = {
        'Content-Type': 'application/json'
    }

    # Schema when data is added
    created_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        }
    }

    domain = os.environ.get('LOCAL_HOST', 'http://127.0.0.1:5000')
    req = requests.session()

    if id == 'id':
        id = ''
    
    url_to_hit = f"{domain}/api/categories?id={id}"

    if isinstance(payload, dict):
        payload = json.dumps(payload)
        response = req.put(url_to_hit, headers=headers, data=payload)
    
    assert response.status_code == expected_status_code
    assert response.json() == expected_output