from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patients = db.relationship("Patient", backref="therapist", lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    medical_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    from datetime import datetime

class Therapy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey("therapist.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)

    therapist = db.relationship("Therapist", backref="therapies")
    patient = db.relationship("Patient", backref="therapies")

