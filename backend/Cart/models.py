# backend/cart/models.py
from extensions import db

class CartItem(db.Model):
    __bind_key__ = 'cart'
    __tablename__='cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
