# backend/products/models.py
from extensions import db

class Product(db.Model):
    __bind_key__ = 'products'
    __tablename__='items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))

    def to_dict(self):
        """Return a dictionary representation of the product"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image_url": self.image_url
        }