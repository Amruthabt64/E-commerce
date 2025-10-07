# backend/orders/models.py
from extensions import db
from datetime import datetime

class Order(db.Model):
    __bind_key__ = 'orders'
    __tablename__='order_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
