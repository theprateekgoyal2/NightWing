from flask import Blueprint

popscape_bp = Blueprint('popscape', __name__, url_prefix='/api/categories')

from app.popscape.apis import *

# Registering views
category_view  = CategoryView.as_view('categories')
subCategory_view = SubCategoryView.as_view('subcategories')
product_view = ProductsView.as_view('products')

# Adding the urls to blueprint
popscape_bp.add_url_rule('', view_func=category_view, methods=['GET', 'POST', 'PUT', 'DELETE'])
popscape_bp.add_url_rule('/subcategories', view_func=subCategory_view, methods=['GET', 'POST', 'PUT', 'DELETE'])
popscape_bp.add_url_rule('/subcategories/products', view_func=product_view, methods=['GET', 'POST', 'PUT', 'DELETE'])
