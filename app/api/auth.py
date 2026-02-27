import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.repositories.json_repository import JsonRepository
from app.services.auth_service import AuthService

# Blueprint
auth_bp = Blueprint("auth", __name__)


def _get_service() -> AuthService:
    data_dir = current_app.config["DATA_DIR"]
    repo = JsonRepository(
        os.path.join(data_dir, "users.json"),
        User
    )
    return AuthService(repo)


# ----------------------------
# REGISTER
# ----------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    role = body.get("role", "user").strip()

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    try:
        user = _get_service().register(username, password, role)
        return jsonify(user), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409


# ----------------------------
# LOGIN
# ----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "").strip()
    password = body.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    result = _get_service().login(username, password)
    if result is None:
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)

    return jsonify({
        "access_token": access_token
    }), 200