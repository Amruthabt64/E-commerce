from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Allow React frontend to call Flask backend

# Configure database (adjust user, password, and db name as per your setup)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:Amrutha%401@localhost:3306/e_commerce"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================== MODELS ==================

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.Text, nullable=False)  # store items as JSON string

# ================== ROUTES ==================

@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])

@app.route("/api/orders", methods=["POST"])
def place_order():
    data = request.json  # expecting { "items": [...] }
    order = Order(items=json.dumps(data["items"]))
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully", "order_id": order.id})

@app.route("/api/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "items": json.loads(o.items)  # convert back to list
        })
    return jsonify(result)

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == "user" and data["password"] == "pass":
        return jsonify({"success": True, "username": data["username"]})
    return jsonify({"success": False}), 401

# ================== MAIN ==================

if __name__ == "__main__":
    # Create tables if they don’t exist
    with app.app_context():
        db.create_all()
        # Insert sample data if table is empty
        if Product.query.count() == 0:
            sample_products = [
                Product(name="Laptop", price=500),
                Product(name="Phone", price=300),
                Product(name="Headphones", price=50)
            ]
            db.session.bulk_save_objects(sample_products)
            db.session.commit()
            print("✅ Sample products inserted")

    app.run(debug=True)
