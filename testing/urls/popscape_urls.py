import os

domain = os.environ.get("LOCAL_HOST", "http://127.0.0.1:5000")

headers = {"Content-Type": "application/json"}

categories_api = "/api/categories"
sub_categories_api = "/api/categories/subcategories"
products_api = "/api/categories/subcategories/products"

# Categories - GET API - SCHEMA
categories_schema = {
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

# Sub-Categories - GET API - SCHEMA
sub_categories_schema = {
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