from app.extensions import db, bcrypt
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.sqlite import JSON

class User(UserMixin, db.Model):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=True, default=None)
    mobileNumber = db.Column(db.Integer, unique=True, nullable=True, default=None)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, name, email, mobileNumber, public_id, password, is_admin=False):
        self.name = name
        self.email = email
        self.mobileNumber = mobileNumber
        self.public_id = public_id
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def serialize(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'name': self.name,
            'email': self.email,
            'mobileNumber': self.mobileNumber,
            'is_admin': self.is_admin,
            'carts': [cart.serialize() for cart in self.carts]
        }

    def __repr__(self):
        return f"<User {self.name}>"

class Address(db.Model):

    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    meta_details = db.Column(JSON, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, meta_details):
        self.user_id = user_id
        self.meta_details = meta_details

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meta_details': self.meta_details,
            'date_created': self.date_created.isoformat(),
            'date_modified': self.date_modified.isoformat(),
        }

    def __repr__(self):
        return f'<Address {self.meta_details}>'