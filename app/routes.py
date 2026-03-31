import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_bcrypt import Bcrypt
from app import db
from app.models import User, Item
from app.auth import token_required

main = Blueprint("main", __name__)
bcrypt = Bcrypt()

# /health
@main.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# /login
@main.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user:
        hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        user = User(username=data["username"], password=hashed)
        db.session.add(user)
        db.session.commit()

    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(
                seconds=current_app.config["JWT_EXPIRY_SECONDS"]
            )
        },
        current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"]
    )
    return jsonify({"token": token}), 200

# /items GET
@main.route("/items", methods=["GET"])
@token_required
def get_items():
    items = Item.query.filter_by(owner_id=request.user_id).all()
    return jsonify([
        {"id": i.id, "name": i.name, "description": i.description}
        for i in items
    ]), 200

# /items POST
@main.route("/items", methods=["POST"])
@token_required
def create_item():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "name required"}), 400
    item = Item(name=data["name"], description=data.get("description",""), owner_id=request.user_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name}), 201

# /items PUT
@main.route("/items/<int:item_id>", methods=["PUT"])
@token_required
def update_item(item_id):
    item = Item.query.filter_by(id=item_id, owner_id=request.user_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name}), 200

# /items DELETE
@main.route("/items/<int:item_id>", methods=["DELETE"])
@token_required
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id, owner_id=request.user_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200