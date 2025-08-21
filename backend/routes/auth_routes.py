from flask import Blueprint, request, jsonify
from models import db, Therapist, bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    if Therapist.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    therapist = Therapist(name=name, email=email, password=hashed_password, phone=phone)
    db.session.add(therapist)
    db.session.commit()
    return jsonify({"message": "Therapist registered successfully"}), 201

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    therapist = Therapist.query.filter_by(email=email).first()
    if therapist and bcrypt.check_password_hash(therapist.password, password):
        access_token = create_access_token(identity=str(therapist.id), expires_delta=timedelta(days=1))
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401
