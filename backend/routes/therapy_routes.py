from flask import Blueprint, request, jsonify
from models import db, Therapy, Therapist, Patient
from flask_jwt_extended import jwt_required
from datetime import datetime
therapy_routes = Blueprint("therapies", __name__)

# Add a therapy
@therapy_routes.route("/", methods=["POST"])
@jwt_required()
def add_therapy():
    data = request.get_json()
    therapy = Therapy(
        therapist_id=data.get("therapist_id"),
        patient_id=data.get("patient_id"),
        date_time=datetime.strptime(data.get("date_time"), "%Y-%m-%dT%H:%M"),
        notes=data.get("notes")
    )
    db.session.add(therapy)
    db.session.commit()
    return jsonify({"message": "Therapy scheduled successfully"}), 201

# Get all therapies (global calendar view)
@therapy_routes.route("/", methods=["GET"])
@jwt_required()
def get_therapies():
    therapies = Therapy.query.all()
    return jsonify([
        {
            "id": t.id,
            "therapist": t.therapist.name,
            "patient": t.patient.name,
            "date_time": t.date_time.isoformat(),
            "notes": t.notes
        } for t in therapies
    ])
