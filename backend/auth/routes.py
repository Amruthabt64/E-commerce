from flask import Blueprint, request, jsonify
from extensions import db
from auth.models import User, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix='/api')

# ----------------------
# Register
# ----------------------
@auth_bp.route("/register", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "user already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "account created successfully"}), 201

# ----------------------
# Login
# ----------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "invalid username or password"}), 401
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({"message": "login successful", "token": access_token}), 200

# ----------------------
# Get or Update Profile (JWT Protected)
# ----------------------


# ----------------------
# Create Profile (POST) - JWT Protected
# ----------------------
@auth_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id) 

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.profile:
        return jsonify({"error": "Profile already exists, use PUT to update"}), 400

    data = request.get_json()
    profile = Profile(
        user_id=user.id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        age=data.get("age"),
        bio=data.get("bio"),
        phone_number=data.get("phone_number")
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "Profile created successfully", "profile": profile.to_dict()}), 201

# ----------------------
# Get or Update Profile (GET/PUT)
# ----------------------
@auth_bp.route("/profile", methods=["GET", "PUT"])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == "GET":
        if user.profile:
            return jsonify(user.profile.to_dict()), 200
        else:
            return jsonify({"message": "Profile not set"}), 200

    # PUT request
    data = request.get_json()
    if user.profile:
        profile = user.profile
    else:
        profile = Profile(user_id=user.id)
        db.session.add(profile)

    profile.first_name = data.get("first_name", profile.first_name)
    profile.last_name = data.get("last_name", profile.last_name)
    profile.age = data.get("age", profile.age)
    profile.bio = data.get("bio", profile.bio)
    profile.phone_number = data.get("phone_number", profile.phone_number)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully", "profile": profile.to_dict()}), 200

# ----------------------
# Delete Account (JWT Protected)
# ----------------------
@auth_bp.route("/delete-account", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Delete profile if exists
    if user.profile:
        db.session.delete(user.profile)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Account and profile deleted successfully"}), 200
