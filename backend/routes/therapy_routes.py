from flask import Blueprint, request, jsonify
from models import db, Therapy, Therapist, Patient
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta

therapy_routes = Blueprint("therapies", __name__)

@therapy_routes.route("/", methods=["POST"])
@jwt_required()
def add_therapy():
    data = request.get_json()

    # Parse datetime from <input type="datetime-local"> => "YYYY-MM-DDTHH:MM"
    dt_str = data.get("date_time")
    if not dt_str:
        return jsonify({"error": "date_time is required"}), 400
    try:
        date_time = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
    except ValueError:
        return jsonify({"error": "date_time must be in format YYYY-MM-DDTHH:MM"}), 400

    # Validate foreign keys
    patient_id = data.get("patient_id")
    therapist_id = data.get("therapist_id")
    if not Patient.query.get(patient_id):
        return jsonify({"error": "Invalid patient_id"}), 400
    if not Therapist.query.get(therapist_id):
        return jsonify({"error": "Invalid therapist_id"}), 400

    duration = data.get("duration_minutes") or 60

    therapy = Therapy(
        patient_id=patient_id,
        therapist_id=therapist_id,
        date_time=date_time,              # <- proper Python datetime object
        duration_minutes=duration,
        notes=data.get("notes")
    )
    db.session.add(therapy)
    db.session.commit()
    return jsonify({"message": "Therapy added successfully"}), 201

@therapy_routes.route("/", methods=["GET"])
@jwt_required()
def get_therapies():
    therapies = Therapy.query.all()
    return jsonify([
        {
            "id": t.id,
            "patient_id": t.patient_id,
            "patient": t.patient.name if t.patient else None,
            "therapist_id": t.therapist_id,
            "therapist": t.therapist.name if t.therapist else None,
            "date_time": t.date_time.isoformat(),
            "duration_minutes": t.duration_minutes,
            "notes": t.notes
        }
        for t in therapies
    ]), 200
