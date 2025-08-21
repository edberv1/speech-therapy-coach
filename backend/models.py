from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))

    therapies = db.relationship("Therapy", backref="therapist", lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)  # <- Date type
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))
    medical_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    therapies = db.relationship("Therapy", backref="patient", lazy=True)

class Therapy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey("therapist.id"), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)  # <- DateTime type
    duration_minutes = db.Column(db.Integer, default=60)
    notes = db.Column(db.Text)
