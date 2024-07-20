from datetime import datetime
from app.extensions import db
from app.models.auth import User

# The cart model will be mapped to single user and will have cartItems which will contains all the products.
class Cart(db.Model):
    __tablename__ = "Cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('carts', lazy=True))

    def __init__(self, user_id):
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_on': self.created_on.isoformat(),
            'items': [item.serialize() for item in self.items]
        }

    def __repr__(self):
        return f"<Cart {self.id} for User {self.user_id}>"

# The cart-item model will carry the products and will be mapped to cart
class CartItem(db.Model):
    __tablename__ = "CartItems"
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    cart = db.relationship('Cart', backref=db.backref('items', lazy=True))
    product = db.relationship('Products')

    def __init__(self, cart_id, product_id, quantity=1):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

    def serialize(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.serialize()
        }

    def __repr__(self):
        return f"<CartItem {self.id} - Cart {self.cart_id}, Product {self.product_id}>"