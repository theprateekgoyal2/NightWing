from flask import Blueprint
from app.cart.apis import *

cart_bp = Blueprint('cart_bp', __name__, url_prefix='/api/cart')

cart_view = CartView.as_view('cart_view')
cartItem_view = CartItemView.as_view('cart_item_view')

cart_bp.add_url_rule('', view_func=cart_view, methods=['GET', 'POST'])
cart_bp.add_url_rule('/items', view_func=cartItem_view, methods=['GET', 'POST'])