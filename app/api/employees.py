import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.student import Student
from app.repositories.json_repository import JsonRepository
from app.services.student_service import StudentService


# Blueprint (name must match usage in create_app)
employees_bp = Blueprint("employees", __name__)


# Service Loader
def _get_service() -> StudentService:
    data_dir = current_app.config["DATA_DIR"]
    repo = JsonRepository(
        os.path.join(data_dir, "employees.json"),
        Student
    )
    return StudentService(repo)


# ----------------------------
# GET ALL
# ----------------------------
@employees_bp.route("/", methods=["GET"])
@jwt_required()
def list_employees():
    employees = _get_service().list_students()
    return jsonify({
        "count": len(employees),
        "data": employees   # safer generic key
    }), 200


# ----------------------------
# GET SINGLE
# ----------------------------
@employees_bp.route("/<string:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id: str):
    employee = _get_service().get_student(employee_id)
    if employee is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(employee), 200


# ----------------------------
# CREATE
# ----------------------------
@employees_bp.route("/", methods=["POST"])
@jwt_required()
def create_employee():
    body = request.get_json(silent=True) or {}

    required_fields = ("first_name", "last_name", "email", "course")
    missing = [f for f in required_fields if not body.get(f)]

    if missing:
        return jsonify({
            "error": f"Missing fields: {', '.join(missing)}"
        }), 400

    try:
        employee = _get_service().create_student(body)
        return jsonify(employee), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409


# ----------------------------
# UPDATE
# ----------------------------
@employees_bp.route("/<string:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id: str):
    body = request.get_json(silent=True) or {}
    result = _get_service().update_student(employee_id, body)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(result), 200


# ----------------------------
# DELETE
# ----------------------------
@employees_bp.route("/<string:employee_id>", methods=["DELETE"])
@jwt_required()
def delete_employee(employee_id: str):
    if _get_service().delete_student(employee_id):
        return jsonify({"message": "Deleted successfully"}), 200

    return jsonify({"error": "Not found"}), 404