import os
from flask import Flask, request, jsonify, Blueprint
from openai import OpenAI
from dotenv import load_dotenv
from database import Exercise, session
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a blueprint with '/api' prefix
api = Blueprint('api', __name__, url_prefix='/api')

# ---------------- Blueprint API Routes ---------------- #

# GET all exercises
@api.route("/exercises", methods=["GET"])
def get_exercises():
    all_exercises = session.query(Exercise).all()
    exercises_list = [{"title": ex.title, "description": ex.description} for ex in all_exercises]
    return jsonify({"exercises": exercises_list})

# POST add a new exercise
@api.route("/exercises", methods=["POST"])
def add_exercise():
    data = request.json
    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    exercise = Exercise(title=title, description=description)
    session.add(exercise)
    session.commit()
    return jsonify({"message": "Exercise added!", "exercise": {"title": title, "description": description}})

# POST generate AI exercise
@api.route("/generate", methods=["POST"])
def generate_exercise():
    try:
        data = request.json
        prompt = data.get("prompt", "Give me a simple speech therapy exercise")

        # Call AI model
        response = client.chat.completions.create(
            model="gpt-40-mini",  # fast small model
            messages=[
                {"role": "system", "content": "You are a helpful speech therapy assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        exercise_text = response.choices[0].message.content
        return jsonify({"exercise": exercise_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- End Blueprint Routes ---------------- #

# Register the blueprint with the app
app.register_blueprint(api)

# Optional root route
@app.route("/")
def home():
    return "Speech Therapy Coach API is running"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
