"""
Health-check endpoint.
"""
from flask import Blueprint, jsonify

health_bp = Blueprint("health", _name_)


@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200