from flask import Blueprint, jsonify, request, session
from functions.login import studentExists
from functions.students import changePassword

students = Blueprint('students', __name__, url_prefix='/students')


@students.route('/signin', methods=['POST'])
def signin():
    data = request.get_json(force=True)
    studentID = data.get("id")
    password = data.get("password")

    # Si un des champs est vide (en plus de la vérification client)
    if not (studentID and password):
        return jsonify({
            "status": 401,
            "reason": "ID or Password Invalid"
        }), 401
    else:
        student = studentExists(studentID, password)

        # Si l'étudiant existe en base de donnée
        if student:
            return jsonify({
                "success": True,
                "user": student
            }), 200
        else:
            return jsonify({
                "status": 401,
                "reason": "First Name, Surname or Password Invalid"
            }), 401


@students.route('/editPassword', methods=['POST'])
def editPassword():
    if 'user' in session:
        data = request.get_json(force=True)
        if changePassword(session["user"]["id"], data["password"]):
            return jsonify(success=True), 200
        else:
            return jsonify({
                "status": 400,
                "reason": "Modification de mot de passe : Invalid"
            }), 400

    else:
        return jsonify({
            "status": 400,
            "reason": "Session non disponible"
        }), 400
