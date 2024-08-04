import os

domain = os.environ.get("LOCAL_HOST", "http://127.0.0.1:5000")

headers = {"Content-Type": "application/json"}

categories = "/api/categories"
sub_categories = "/api/categories/subcategories"
products = "/api/categories/subcategories/products"