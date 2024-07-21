from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app.models.cart import Cart, CartItem
from app.models.auth import User
from app.models.popscape import Products
from app.decorators import login_required
from flask_jwt_extended import decode_token
from app.extensions import db
from app.utils import get_user_id
class CartView(MethodView):
    
    decorators = [login_required]

    # This view will retrieve all the carts for the particular user
    def get(self):
        
        # Decoding the payload to fetch the stored details
        token = request.headers['token']
        user_id = get_user_id(token)

        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify([cart.serialize() for cart in user.carts]), 200

        except SQLAlchemyError as e:
            # Log the error message
            # log.error(f"Database error: {str(e)}")
            return jsonify({"error": "Database error", "message": str(e)}), 500

    # This view will create a new cart for users.
    def post(self):

        # Decoding the payload to fetch the stored details
        token = request.headers['token']
        user_id = self.get_user_id(token)

        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            # Check for existing carts
            carts = user.carts
            
            # If the existing cart has no items added into it
            for cart in carts:
                if len(cart.items) == 0:
                    return jsonify({"message": "Your existing cart has nothing added, add items to make another cart"}), 200
            
            # If user already created 3 carts 
            if len(carts) == 3:
                    return jsonify({"message":"You already have 3 existing carts, checkout to make more"}), 200    
            
            new_cart = Cart(user_id=user.id)
            db.session.add(new_cart)
            db.session.commit()
            return jsonify(new_cart.serialize()), 201
        
        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"error": "Database error", "message": str(e)}), 500
        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Unexpected error", "message": str(e)}), 500

class CartItemView(MethodView):

    decorators = [login_required]
    
    def get(self):
        
        cart_id = request.args.get("cart_id")

        """Get all items in the cart."""
        cart = Cart.query.get(cart_id)
        if not cart:
            return jsonify({"error": "Cart not found"}), 404

        return jsonify([item.serialize() for item in cart.items]), 200

    def post(self):
        cart_id = request.args.get("cart_id")
        
        if not cart_id:
            return jsonify({"error": "Cart ID parameter is missing"}), 400

        try:
            """Add a new item to the cart."""
            cart = Cart.query.get(cart_id)
            if not cart:
                return jsonify({"error": "Cart not found"}), 404

            if not request.is_json:
                return jsonify({"error": "Invalid JSON"}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing"}), 400

            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)

            if not product_id:
                return jsonify({"error": "Product ID is missing"}), 400
            if not isinstance(quantity, int) or quantity <= 0:
                return jsonify({"error": "Quantity must be a positive integer"}), 400

            product = Products.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404
            
            # Check if the product is already in the cart
            existing_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
            if existing_item:
                existing_item.quantity += quantity
            else:
                cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=quantity)
                db.session.add(cart_item)

            db.session.commit()

            return jsonify(existing_item.serialize() if existing_item else cart_item.serialize()), 201

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")
            # Return a 500 error with the error message
            return jsonify({"error": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Unexpected error", "message": str(e)}), 500