from flask import Blueprint, request, jsonify
from models import db, Patient
from flask_jwt_extended import jwt_required
from datetime import datetime

patient_routes = Blueprint("patients", __name__)

@patient_routes.route("/", methods=["POST"])
@jwt_required()
def add_patient():
    data = request.get_json()

    dob_str = data.get("date_of_birth")
    dob = None
    if dob_str:
        # Accept "YYYY-MM-DD" from <input type="date">
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "date_of_birth must be YYYY-MM-DD"}), 400

    patient = Patient(
        name=data.get("name"),
        date_of_birth=dob,            # <- proper Python date object
        phone=data.get("phone"),
        address=data.get("address"),
        medical_notes=data.get("medical_notes")
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({"message": f"Patient {patient.name} added successfully"}), 201

@patient_routes.route("/", methods=["GET"])
@jwt_required()
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "date_of_birth": p.date_of_birth.isoformat() if p.date_of_birth else None,
            "phone": p.phone,
            "address": p.address,
            "medical_notes": p.medical_notes
        }
        for p in patients
    ]), 200
