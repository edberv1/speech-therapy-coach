from flask import Blueprint, jsonify
from models import Therapist
from flask_jwt_extended import jwt_required

therapist_routes = Blueprint("therapists", __name__)

# GET all therapists
@therapist_routes.route("/", methods=["GET"])
@jwt_required()  # optional, only logged-in users can see therapists
def get_therapists():
    therapists = Therapist.query.all()
    return jsonify([{"id": t.id, "name": t.name} for t in therapists])
