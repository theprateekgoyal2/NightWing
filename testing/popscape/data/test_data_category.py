test_data_create_category = [
    # Case-1: Valid category creation
    {
        "payload": {"name": "Movie"},
        "expected_output": {"message": "Category created successfully"},
        "expected_status": 201,
    },
    {
        "payload": {"name": "Show"},
        "expected_output": {"message": "Category created successfully"},
        "expected_status": 201,
    },
    # Case-2: missing request body
    {
        "payload": {},
        "expected_output": {"message": "Request body is missing"},
        "expected_status": 400,
    },
    # Case-3: missing name field
    {
        "payload": {"another_field": "value"},
        "expected_output": {"message": "Name field missing."},
        "expected_status": 400,
    },
    # Case-4: empty name field
    {
        "payload": {"name": ""},
        "expected_output": {"message": "Name field can't be empty."},
        "expected_status": 400,
    },
    # Case-5: duplicate category
    {
        "payload": {"name": "Movie"},
        "expected_output": {"message": "Category already exists."},
        "expected_status": 400,
    },
]

test_data_update_category = [
    # Case-1: Valid category update
    {
        "payload": {"name": "Movies"},
        "category_id": 1,
        "expected_output": {"message": "Item edited successfully"},
        "expected_status": 202,
    },
    {
        "payload": {"name": "Shows"},
        "category_id": 2,
        "expected_output": {"message": "Item edited successfully"},
        "expected_status": 202,
    },
    # Case-2: Invalid Id
    {
        "payload": {"name": "New Category Updated"},
        "category_id": 3,
        "expected_output": {"message": "No item found"},
        "expected_status": 404,
    },
    # Case-3: Id missing
    {
        "payload": {"name": "New Category Updated"},
        "category_id": "id",
        "expected_output": {"message": "ID parameter is missing"},
        "expected_status": 400,
    },
    # Case-4: Missing request body
    {
        "payload": {},
        "category_id": 1,
        "expected_output": {"message": "Request body is missing"},
        "expected_status": 400,
    },
    # Case-5: Missing name field
    {
        "payload": {"another_field": "value"},
        "category_id": 1,
        "expected_output": {"message": "Name field missing."},
        "expected_status": 400,
    },
    # Case-6: Empty name field
    {
        "payload": {"name": ""},
        "category_id": 1,
        "expected_output": {"message": "Name field can't be empty."},
        "expected_status": 400,
    },
    # Case-7: Duplicate category
    {
        "payload": {"name": "Movies"},
        "category_id": 1,
        "expected_output": {"message": "Category already exists."},
        "expected_status": 400,
    },
]