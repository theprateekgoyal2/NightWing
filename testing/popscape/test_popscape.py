import pytest
from testing.utils.requests_utils import hit_endpoint
from testing.utils.assertion_utils import assert_response
from .utils import check_id, check_sid, generate_category_params, generate_subcategory_params
from testing.urls.popscape_urls import categories_api, categories_schema, sub_categories_api, sub_categories_schema
from .data.test_data_popscape import test_data_create_category, test_data_update_category, test_data_retrieve_category, test_data_create_subcategory, test_data_update_subcategory, test_data_retrieve_subcategory

class TestCategoryAPI:
    # POST-API
    @pytest.mark.parametrize('test_case', test_data_create_category)
    def test_create_category_api(self, test_case):
        response = hit_endpoint(endpoint=categories_api, payload=test_case['payload'], method='post')
        assert_response(response=response, expected_output=test_case['expected_output'], expected_status=test_case['expected_status'])

    # GET-API
    @pytest.mark.parametrize('test_case', test_data_retrieve_category)
    def test_retrieve_category_api(self, test_case):
        response = hit_endpoint(endpoint=categories_api, method='get')
        assert_response(response=response, expected_output=test_case['expected_output'], expected_status=test_case['expected_status'], schema_data=categories_schema)

    # PUT-API
    @pytest.mark.parametrize('test_case', test_data_update_category)
    def test_update_category_api(self, test_case):
        id = check_id(test_case['category_id'])
        params = generate_category_params(id)
        response = hit_endpoint(endpoint=categories_api, payload=test_case['payload'], method='put', params=params)
        assert_response(response=response, expected_output=test_case['expected_output'], expected_status=test_case['expected_status'])


class TestSubCategoryAPI:
    # POST-API
    @pytest.mark.parametrize('test_case', test_data_create_subcategory)
    def test_create_subcategory_api(self, test_case):
        id = check_id(test_case['category_id'])
        params = generate_category_params(id)
        response = hit_endpoint(endpoint=sub_categories_api, payload=test_case['payload'], method='post', params=params)
        assert_response(response=response, expected_output=test_case['expected_output'], expected_status=test_case['expected_status'])

    # GET-API
    @pytest.mark.parametrize('test_case', test_data_retrieve_subcategory)
    def test_retrieve_subcategory_api(self, test_case):
        id = check_id(test_case['category_id'])
        params = generate_category_params(id)
        response = hit_endpoint(endpoint=sub_categories_api, method='get', params=params)
        assert_response(response=response, expected_output=test_case['expected_output'], expected_status=test_case['expected_status'], schema_data=sub_categories_schema)

    # PUT-API
    @pytest.mark.parametrize('test_case', test_data_update_subcategory)
    def test_update_subcategory_api(self, test_case):
        sid = check_sid(test_case['subcategory_id'])
        params = generate_subcategory_params(sid)
        response = hit_endpoint(endpoint=sub_categories_api, payload=test_case['payload'], method='put', params=params)
        assert_response(response=response, expected_output=test_case['expected_output'], expected_status=test_case['expected_status'])