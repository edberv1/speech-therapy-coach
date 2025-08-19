from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, bcrypt
from routes.auth_routes import auth_routes
from routes.patient_routes import patient_routes
from routes.ai_routes import api  # your OpenAI routes
from routes.therapy_routes import therapy_routes
from routes.therapist_routes import therapist_routes
import os

app = Flask(__name__)
CORS(app)

# Config
app.config.from_object("config.Config")

# Init extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(api, url_prefix="/api")  # AI exercises
app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(patient_routes, url_prefix="/patients")
app.register_blueprint(therapy_routes, url_prefix="/therapies")
app.register_blueprint(therapist_routes, url_prefix="/therapists")

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Speech Therapy App API is running"

if __name__ == "__main__":
    app.run(debug=True)
