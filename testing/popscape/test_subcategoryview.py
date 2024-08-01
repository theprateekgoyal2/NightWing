import pytest
import requests
import json
from jsonschema import validate, ValidationError
import os

# def test_dummy():
#     assert 1 == 1
#     assert 1 == 2

# POST-API
test_data_1 = [
    # Case-1: Category Exists - Adding Sub-Category Happy Flow
    (1, {"name": "The Wolf Of Wall Street", "releaseYear": 2013}, {"message": "Sub-Category added successfully"}, 201),
    (1, {"name": "Her", "releaseYear": 2013}, {"message": "Sub-Category added successfully"}, 201),
    # Case-2: Category Exists - missing request body
    (1, {}, {"message": "Request body is missing"}, 400),
    # Case-3: Category Exists - missing name field
    (1, {"another_field": "The Wolf Of Wall Street", "releaseYear": 2013}, {"message": "Name field missing."}, 400),
    # Case-4: Category Exists - empty name field
    (1, {"name": "", "releaseYear": 2013}, {"message": "Name field can't be empty."}, 400),
    # Case-5: Category Exists - missing year field
    (1, {"name": "The Wolf Of Wall Street", "another_field": 2013}, {"message": "releaseYear field missing."}, 400),
    # Case-6: Category Exists - empty year field
    (1, {"name": "The Wolf Of Wall Street", "releaseYear": ""}, {"message": "releaseYear field can't be empty."}, 400),
    # Case-7: Category doesn't exists
    (3, {"name": "Her", "releaseYear": 2013}, {"message": "Category does not exist"}, 404),
    # Case-8: Sub-Category already exists
    (1, {"name": "The Wolf Of Wall Street", "releaseYear": 2013}, {"message": "Sub-Category already exists"}, 400),
    # Case-9: ID parameter missing
    ('id', {"name": "The Wolf Of Wall Street", "releaseYear": 2013}, {"message":"ID parameter is missing"}, 400),
]

@pytest.mark.parametrize('id, payload, expected_output, expected_status_code', test_data_1)
def test_create_subcategory_api(id, payload, expected_output, expected_status_code):
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

    domain = os.environ['LOCAL_HOST']
    req = requests.session()

    if id == 'id':
        id = ''
    
    url_to_hit = f"{domain}/api/categories/subcategories?id={id}"

    if isinstance(payload, dict):
        payload = json.dumps(payload)
        response = req.post(url_to_hit, headers=headers, data=payload)
    
    assert response.status_code == expected_status_code
    assert response.json() == expected_output

# GET-API
test_data_2 = [
    # Case-1: Category exists and sub-cateogry also exists
    (1, "schema", 200),
    # Case-2: Category exists but sub-category doesn't exists
    (2, {"message": "No Sub-Categories found"}, 404),
    # Case-3: Category doesn't exists
    (3, {"message": "Category does not exist"}, 404),
    # Case-4: ID parameter missing
    ('id', {"message": "ID parameter is missing"}, 400),
]

@pytest.mark.parametrize('id, expected_output, expected_status_code', test_data_2)
def test_retrieve_subcategory_api(id, expected_output, expected_status_code):

    # Define the JSON schema to be compared
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "category": { "type": "string" },
                "category_id": { "type": "integer" },
                "code": { "type": "string" },
                "id": { "type": "integer" },
                "name": { "type": "string" },
                "releaseYear": { "type": "integer" },
                "totalProducts": { "type": "integer" }
            },
            "required": ["category", "category_id", "code", "id", "name", "releaseYear", "totalProducts"]
        }
    }
    if id == 'id':
        id = ''

    domain = os.environ['LOCAL_HOST']
    url_to_hit = f"{domain}/api/categories/subcategories?id={id}"
    req = requests.session()
    response = req.get(url_to_hit)

    if response.status_code == 200:
        assert isinstance(response.json(), list), "Response is not a list"

        try:
            validate(instance=response.json(), schema=schema)
        except ValidationError as e:
            pytest.fail(f"JSON response does not match schema: {e}")

        for item in response.json():
            assert isinstance(item['id'], int), "ID is not an integer"
            assert isinstance(item['name'], str), "Name is not a string"
            assert isinstance(item['releaseYear'], int), "Release Year is not an integer"
            assert isinstance(item['category'], str), "Category is not a string"
            assert isinstance(item['category_id'], int), "Category ID is not an integer"
            assert isinstance(item['code'], str), "Code is not a string"
            assert isinstance(item['totalProducts'], int), "Total Products is not an integer"

    elif response.status_code == 404:
        assert response.json() == expected_output
    
    elif response.status_code == 400:
        assert response.json() == expected_output

    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")

# PUT-APIs
test_data_put = [
    # Case 1: Successful update
    ('1', {"name": "La La LAnd", "releaseYear": 2016}, {"message": "Sub-Category edited successfully."}, 202),
    # Case 2: Missing S-ID parameter
    ('sid', {"name": "New Name", "releaseYear": 2022}, {"message": "S-ID parameter is missing."}, 400),
    # Case 3: Sub-Category not found
    ('999', {"name": "New Name", "releaseYear": 2022}, {"message": "No Sub-Category found."}, 404),
    # Case 4: Missing request body
    ('1', {}, {"message": "Request body is missing."}, 400),
    # Case 5: Empty name field
    ('1', {"name": "", "releaseYear": 2022}, {"message": "Name field can't be empty."}, 400),
    # Case 6: Empty releaseYear field
    ('1', {"name": "New Name", "releaseYear": ""}, {"message": "releaseYear field can't be empty."}, 400),
    # Case 7: Sub-Category already exists
    ('1', {"name": "Her", "releaseYear": 2013}, {"message": "Sub-Category already exists."}, 400),
]

@pytest.mark.parametrize('sid, payload, expected_output, expected_status_code', test_data_put)
def test_update_subcategory_api(sid, payload, expected_output, expected_status_code):
    headers = {
        'Content-Type': 'application/json'
    }

    if sid is 'sid':
        sid = ''
    
    domain = os.environ['LOCAL_HOST']
    url_to_hit = f"{domain}/api/categories/subcategories?sid={sid}"
    req = requests.session()

    if isinstance(payload, dict):
        payload = json.dumps(payload)
        response = req.put(url_to_hit, headers=headers, data=payload)

    assert response.status_code == expected_status_code
    assert response.json() == expected_output