from app.extensions import db, bcrypt
from datetime import datetime
from flask_login import UserMixin

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
            'is_admin': self.is_admin
        }

    def __repr__(self):
        return f"<User {self.name}>"