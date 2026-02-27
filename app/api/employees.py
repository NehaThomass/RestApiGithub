from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

# ✅ Correct blueprint name (matches app/__init__.py)
employees_bp = Blueprint("employees", __name__)

employees = []
current_id = 1


@employees_bp.route("", methods=["POST"])
@jwt_required()
def create_employee():
    global current_id

    data = request.get_json(silent=True) or {}

    employee = {
        "id": current_id,
        "name": data.get("name", "").strip(),
        "email": data.get("email", "").strip(),
        "department": data.get("department", "").strip()
    }

    employees.append(employee)
    current_id += 1

    return jsonify({"employee": employee}), 201


@employees_bp.route("", methods=["GET"])
@jwt_required()
def list_employees():
    return jsonify({
        "count": len(employees),
        "employees": employees
    }), 200


@employees_bp.route("/<int:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id):
    employee = next(
        (e for e in employees if e["id"] == employee_id),
        None
    )

    if employee:
        return jsonify(employee), 200

    return jsonify({"message": "Employee not found"}), 404


@employees_bp.route("/<int:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id):
    data = request.get_json(silent=True) or {}

    for employee in employees:
        if employee["id"] == employee_id:
            employee["name"] = data.get("name", employee["name"]).strip()
            employee["email"] = data.get("email", employee["email"]).strip()
            employee["department"] = data.get("department", employee["department"]).strip()

            return jsonify({"employee": employee}), 200

    return jsonify({"message": "Employee not found"}), 404


@employees_bp.route("/<int:employee_id>", methods=["DELETE"])
@jwt_required()
def delete_employee(employee_id):
    global employees

    if any(e["id"] == employee_id for e in employees):
        employees = [e for e in employees if e["id"] != employee_id]
        return jsonify({"message": "Employee deleted"}), 200

    return jsonify({"message": "Employee not found"}), 404