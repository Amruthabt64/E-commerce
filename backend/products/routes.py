# backend/products/routes.py
from flask import Blueprint, jsonify, request
from extensions import db
from products.models import Product

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

# ----------------------
# GET all products
# ----------------------
@products_bp.route('/', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    result = [p.to_dict() for p in products]
    return jsonify(result), 200

# ----------------------
# GET single product by ID
# ----------------------
@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200

# ----------------------
# CREATE product
# ----------------------
@products_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data.get('name') or not data.get('price'):
        return jsonify({"error": "Name and price are required"}), 400

    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        stock=data.get('stock', 0),
        image_url=data.get('image_url')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully", "product": new_product.to_dict()}), 201

# ----------------------
# UPDATE product
# ----------------------
@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.image_url = data.get('image_url', product.image_url)

    db.session.commit()
    return jsonify({"message": "Product updated successfully", "product": product.to_dict()}), 200

# ----------------------
# DELETE product
# ----------------------
@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200
