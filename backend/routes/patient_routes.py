from flask import Blueprint, request, jsonify
from models import db, Patient
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

patient_routes = Blueprint("patients", __name__)

@patient_routes.route("/", methods=["POST"])
@jwt_required()
def add_patient():
    therapist_id = int(get_jwt_identity())
    data = request.get_json()

    # Convert date_of_birth string to date object
    dob_str = data.get("date_of_birth")
    dob = None
    if dob_str:
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "date_of_birth must be in YYYY-MM-DD format"}), 400

    patient = Patient(
        therapist_id=therapist_id,
        name=data.get("name"),
        date_of_birth=dob,
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
    therapist_id = int(get_jwt_identity())
    patients = Patient.query.filter_by(therapist_id=therapist_id).all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "date_of_birth": str(p.date_of_birth),
        "phone": p.phone,
        "address": p.address,
        "medical_notes": p.medical_notes
    } for p in patients]), 200
