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

test_data_retrieve_category = [
    # Case-1: Empty Database
    # {
    #     "expected_output": {"message": "No categories found"},
    #     "expected_status": 404
    # },
    # Case-2: Happy Flow
    {
        "expected_output": "SchemaData",
        "expected_status": 200
    },
]

test_data_create_subcategory = [
    # Case-1: Category Exists - Adding Sub-Category Happy Flow
    {
        "category_id": 1,
        "payload": {"name": "The Wolf Of Wall Street", "releaseYear": 2013},
        "expected_output": {"message": "Sub-Category added successfully"},
        "expected_status": 201,
    },
    {
        "category_id": 1,
        "payload": {"name": "Her", "releaseYear": 2013},
        "expected_output": {"message": "Sub-Category added successfully"},
        "expected_status": 201,
    },
    # Case-2: Category Exists - missing request body
    {
        "category_id": 1,
        "payload": {},
        "expected_output": {"message": "Request body is missing"},
        "expected_status": 400,
    },
    # Case-3: Category Exists - missing name field
    {
        "category_id": 1,
        "payload": {"another_field": "The Wolf Of Wall Street", "releaseYear": 2013},
        "expected_output": {"message": "Name field missing."},
        "expected_status": 400,
    },
    # Case-4: Category Exists - empty name field
    {
        "category_id": 1,
        "payload": {"name": "", "releaseYear": 2013},
        "expected_output": {"message": "Name field can't be empty."},
        "expected_status": 400,
    },
    # Case-5: Category Exists - missing year field
    {
        "category_id": 1,
        "payload": {"name": "The Wolf Of Wall Street", "another_field": 2013},
        "expected_output": {"message": "releaseYear field missing."},
        "expected_status": 400,
    },
    # Case-6: Category Exists - empty year field
    {
        "category_id": 1,
        "payload": {"name": "The Wolf Of Wall Street", "releaseYear": ""},
        "expected_output": {"message": "releaseYear field can't be empty."},
        "expected_status": 400,
    },
    # Case-7: Category doesn't exist
    {
        "category_id": 3,
        "payload": {"name": "Her", "releaseYear": 2013},
        "expected_output": {"message": "Category does not exist"},
        "expected_status": 404,
    },
    # Case-8: Sub-Category already exists
    {
        "category_id": 1,
        "payload": {"name": "The Wolf Of Wall Street", "releaseYear": 2013},
        "expected_output": {"message": "Sub-Category already exists"},
        "expected_status": 400,
    },
    # Case-9: ID parameter missing
    {
        "category_id": 'id',
        "payload": {"name": "The Wolf Of Wall Street", "releaseYear": 2013},
        "expected_output": {"message": "ID parameter is missing"},
        "expected_status": 400,
    },
]

test_data_update_subcategory = [
    # Case 1: Successful update
    {
        "subcategory_id": '1',
        "payload": {"name": "La La Land", "releaseYear": 2016},
        "expected_output": {"message": "Sub-Category edited successfully."},
        "expected_status": 202,
    },
    # Case 2: Missing S-ID parameter
    {
        "subcategory_id": 'sid',
        "payload": {"name": "New Name", "releaseYear": 2022},
        "expected_output": {"message": "S-ID parameter is missing."},
        "expected_status": 400,
    },
    # Case 3: Sub-Category not found
    {
        "subcategory_id": '999',
        "payload": {"name": "New Name", "releaseYear": 2022},
        "expected_output": {"message": "No Sub-Category found."},
        "expected_status": 404,
    },
    # Case 4: Missing request body
    {
        "subcategory_id": '1',
        "payload": {},
        "expected_output": {"message": "Request body is missing."},
        "expected_status": 400,
    },
    # Case 5: Empty name field
    {
        "subcategory_id": '1',
        "payload": {"name": "", "releaseYear": 2022},
        "expected_output": {"message": "Name field can't be empty."},
        "expected_status": 400,
    },
    # Case 6: Empty releaseYear field
    {
        "subcategory_id": '1',
        "payload": {"name": "New Name", "releaseYear": ""},
        "expected_output": {"message": "releaseYear field can't be empty."},
        "expected_status": 400,
    },
    # Case 7: Sub-Category already exists
    {
        "subcategory_id": '1',
        "payload": {"name": "Her", "releaseYear": 2013},
        "expected_output": {"message": "Sub-Category already exists."},
        "expected_status": 400,
    },
]

test_data_retrieve_subcategory = [
    # Case-1: Category exists and sub-category also exists
    {
        "category_id": 1,
        "expected_output": "SchemaData",
        "expected_status": 200,
    },
    # Case-2: Category exists but sub-category doesn't exist
    {
        "category_id": 2,
        "expected_output": {"message": "No Sub-Categories found"},
        "expected_status": 404,
    },
    # Case-3: Category doesn't exist
    {
        "category_id": 3,
        "expected_output": {"message": "Category does not exist"},
        "expected_status": 404,
    },
    # Case-4: ID parameter missing
    {
        "category_id": 'id',
        "expected_output": {"message": "ID parameter is missing"},
        "expected_status": 400,
    },
]