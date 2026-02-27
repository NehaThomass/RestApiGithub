from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

students_bp = Blueprint("students", __name__)

# In-memory storage (for testing/demo only)
students = []
current_id = 1


@students_bp.route("", methods=["POST"])
@jwt_required()
def create_student():
    global current_id

    data = request.get_json(silent=True) or {}

    student = {
        "id": current_id,
        "name": data.get("name", "").strip(),
        "email": data.get("email", "").strip(),
        "course": data.get("course", "").strip()
    }

    students.append(student)
    current_id += 1

    return jsonify({"student": student}), 201


@students_bp.route("", methods=["GET"])
@jwt_required()
def list_students():
    return jsonify({
        "count": len(students),
        "students": students
    }), 200


@students_bp.route("/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):
    student = next(
        (s for s in students if s["id"] == student_id),
        None
    )

    if student:
        return jsonify(student), 200

    return jsonify({"message": "Student not found"}), 404


@students_bp.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    data = request.get_json(silent=True) or {}

    for student in students:
        if student["id"] == student_id:
            student["name"] = data.get("name", student["name"]).strip()
            student["email"] = data.get("email", student["email"]).strip()
            student["course"] = data.get("course", student["course"]).strip()

            return jsonify({"student": student}), 200

    return jsonify({"message": "Student not found"}), 404


@students_bp.route("/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    global students

    if any(s["id"] == student_id for s in students):
        students = [s for s in students if s["id"] != student_id]

        return jsonify({"message": "Student deleted"}), 200

    return jsonify({"message": "Student not found"}), 404