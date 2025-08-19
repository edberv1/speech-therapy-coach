
import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Speech Therapy Coach API is running"

@app.route("/generate", methods=["POST"])
def generate_exercise():
    try:
        data = request.json
        prompt = data.get("prompt", "Give me a simple speech therapy exercise")

        #Call AI Model
        response = client.chat.completions.create(
            model="gpt-40-mini", #small, fast model
            messages=[
                {"role": "system", "content": "You are a helpful speech therapy assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens = 200
        )  
        exercise = response.choices[0].message.content
        return jsonify({"exercise":exercise})
    except Exception as e:
        return jsonify({"error": str(e)}) , 500
    
exercises = []

@app.route("/add_exercise", methods=["POST"])
def add_exercise():
    data = request.json
    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return jsonify({"error" : "Title and description are required"}) , 400
    
    exercise = {"title": title, "description": description}
    exercises.append(exercise)
    return jsonify({"message": "Exercise added!","exercise":exercise})

@app.route("/exercises", methods=["GET"])
def get_exercises():
    return jsonify({"exercises": exercises})


if __name__ == "__main__":
    app.run(debug=True)






