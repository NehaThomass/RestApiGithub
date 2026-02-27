from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

# Blueprint (prefix handled in app/__init__.py)
employees_bp = Blueprint("employees", __name__)

employees = []
current_id = 1


# =============================
# CREATE EMPLOYEE
# POST /api/v1/students
# =============================
@employees_bp.route("/students", methods=["POST"])
@jwt_required()
def create_employee():
    global current_id

    data = request.get_json(silent=True) or {}

    student = {
        "id": current_id,
        "name": data.get("name", "").strip(),
        "email": data.get("email", "").strip(),
        "course": data.get("course", "").strip()
    }

    employees.append(student)
    current_id += 1

    return jsonify({"student": student}), 201


# =============================
# LIST STUDENTS
# GET /api/v1/students
# =============================
@employees_bp.route("/students", methods=["GET"])
@jwt_required()
def list_students():
    return jsonify({
        "students": employees
    }), 200


# =============================
# GET STUDENT
# =============================
@employees_bp.route("/students/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):

    student = next(
        (s for s in employees if s["id"] == student_id),
        None
    )

    if student:
        return jsonify({"student": student}), 200

    return jsonify({"message": "Student not found"}), 404


# =============================
# UPDATE STUDENT
# =============================
@employees_bp.route("/students/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):

    data = request.get_json(silent=True) or {}

    for student in employees:
        if student["id"] == student_id:

            student["name"] = data.get("name", student["name"]).strip()
            student["email"] = data.get("email", student["email"]).strip()
            student["course"] = data.get("course", student["course"]).strip()

            return jsonify({"student": student}), 200

    return jsonify({"message": "Student not found"}), 404


# =============================
# DELETE STUDENT
# =============================
@employees_bp.route("/students/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):

    global employees

    if any(s["id"] == student_id for s in employees):

        employees = [s for s in employees if s["id"] != student_id]

        return jsonify({"message": "Student deleted"}), 200

    return jsonify({"message": "Student not found"}), 404