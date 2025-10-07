# backend/cart/routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from Cart.models import CartItem
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()
    result = [{"id": i.id, "product_id": i.product_id, "quantity": i.quantity} for i in items]
    return jsonify(result), 200

@cart_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    item = CartItem(user_id=user_id, product_id=data['product_id'], quantity=data.get('quantity', 1))
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Item added to cart"}), 201

@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_item(item_id):
    user_id = get_jwt_identity()
    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed"}), 200
