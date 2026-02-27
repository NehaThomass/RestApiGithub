"""
Auth blueprint – register & login endpoints.
"""
import os
from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app.repositories.json_repository import JsonRepository
from app.services.auth_service import AuthService

# ✅ Correct blueprint initialization
auth_bp = Blueprint("auth", __name__)


def _get_service() -> AuthService:
    """Create AuthService instance."""
    data_dir = current_app.config["DATA_DIR"]
    repo = JsonRepository[User](
        os.path.join(data_dir, "users.json"),
        User
    )
    return AuthService(repo)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    body = request.get_json(silent=True) or {}

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    role = body.get("role", "user").strip()

    # ✅ Validation
    if not username or not password:
        return jsonify({
            "error": "username and password are required"
        }), 400

    try:
        user = _get_service().register(username, password, role)

        return jsonify({
            "message": "User registered successfully",
            "user": user
        }), 201

    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 409


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT tokens."""
    body = request.get_json(silent=True) or {}

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()

    # ✅ Validation
    if not username or not password:
        return jsonify({
            "error": "username and password are required"
        }), 400

    result = _get_service().login(username, password)

    if result is None:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    return jsonify(result), 200