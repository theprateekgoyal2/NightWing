from app.extensions import db
import base64

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    totalItems = db.Column(db.Integer, default=0)

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'totalItems': self.totalItems 
        }

    def __repr__(self):
        return '<Category %r>' % self.name

class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    releaseYear = db.Column(db.Integer, nullable=False)
    totalProducts = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    abbreviation = db.Column(db.String(255), nullable=False)
    category = db.relationship('Category', backref=db.backref('category_lists', lazy=True))
    
    def __init__(self, name, releaseYear, category_id, abbreviation):
        self.name = name
        self.releaseYear = releaseYear
        self.category_id = category_id
        self.abbreviation = abbreviation

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'releaseYear': self.releaseYear,
            'category_id': self.category_id,
            'category': self.category.name,
            'code': self.abbreviation,
            'totalProducts': self.totalProducts
        }
    
    def __repr__(self):
        return '<SubCategory %r>' % self.name

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subProduct = db.Column(db.String(255), nullable=False)
    subCategory_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'))
    subCategory = db.relationship('SubCategory', backref=db.backref('products', lazy=True))
    price = db.Column(db.Float, nullable=False)

    def __init__ (self, name, subCategory_id, subProduct, price):
        self.name = name
        self.subCategory_id = subCategory_id
        self.subProduct = subProduct
        self.price = price

    def serialize(self):
        return {
            'id': self.id,
            'subCategory_ID': self.subCategory_id,
            'name': self.name,
            'subProduct': self.subProduct,
            'price': self.price
        }
    
    def __repr__(self):
        return '<Products %r>' % self.name