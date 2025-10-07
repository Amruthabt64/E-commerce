# backend/orders/routes.py
from flask import Blueprint, jsonify, request
from extensions import db
from Orders.models import Order
from flask_jwt_extended import jwt_required, get_jwt_identity

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    result = [{"id": o.id, "total_amount": o.total_amount, "status": o.status, "created_at": o.created_at} for o in orders]
    return jsonify(result), 200

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_order = Order(
        user_id=user_id,
        total_amount=data['total_amount'],
        status=data.get('status', 'Pending')
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully"}), 201
