import pytest
import requests
import json
from jsonschema import validate, ValidationError
import os
from .data.test_data_category import test_data_create_category, test_data_update_category
from testing.utils.requests_utils import hit_endpoint
from testing.utils.assertion_utils import assert_response
from testing.utils.common_utils import check_id
from testing.urls.popscape_urls import *

# POST-API
@pytest.mark.parametrize('test_case', test_data_create_category)
def test_create_category_api(test_case):
    
    payload = test_case['payload']
    response = hit_endpoint(endpoint=categories, payload=payload, method='post')
    assert_response(response=response, expected_output=test_case['expected_output'], expected_status=test_case['expected_status'])

# GET-API
# def test_retrieve_category_api():
#     # Define the JSON schema to be compared
#     schema = {
#         "type": "array",
#         "items": {
#             "type": "object",
#             "properties": {
#                 "id": {"type": "integer"},
#                 "name": {"type": "string"},
#                 "totalItems": {"type": "integer"}
#             },
#             "required": ["id", "name", "totalItems"]
#         }
#     }
    
#     domain = os.environ['LOCAL_HOST']
#     url_to_hit = categories
#     req = requests.session()
#     retrieved_items = req.get(url_to_hit)

#     if retrieved_items.status_code == 200:
#         try:
#             validate(instance=retrieved_items.json(), schema=schema)
#             assert True
#         except ValidationError as e:
#             pytest.fail(f"JSON response does not match schema: {e}")
#         finally: 
#             assert isinstance(retrieved_items.json(), list), "Response is not a list"
#             for item in retrieved_items.json():
#                 assert isinstance(item['id'], int), "ID is not an integer"
#                 assert isinstance(item['name'], str), "Name is not a string"
#                 assert isinstance(item['totalItems'], int), "TotalItems is not an integer"

#     elif retrieved_items.status_code == 404:
#         error_response = retrieved_items.json()
#         assert "message" in error_response, "Error response does not contain 'message'"
#         assert error_response["message"] == "No categories found", "Error message does not match"
    
#     else:
#         pytest.fail(f"Unexpected status code: {retrieved_items.status_code}")

# PUT-API
@pytest.mark.parametrize('test_case', test_data_update_category)
def test_update_category_api(test_case):
    id = check_id(test_case['category_id'])
    payload = test_case['payload']
    params = {"id": id}
    response = hit_endpoint(endpoint=categories, payload=payload, method='put', params={params})
    assert_response(response=response, expected_output=test_case['expected_output'], expected_status=test_case['expected_status'])