from flask import Blueprint, jsonify
from models import Therapist
from flask_jwt_extended import jwt_required

therapist_routes = Blueprint("therapists", __name__)

@therapist_routes.route("/", methods=["GET"])
@jwt_required()
def list_therapists():
    therapists = Therapist.query.all()
    return jsonify([{"id": t.id, "name": t.name} for t in therapists]), 200
