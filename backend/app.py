
import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from database import Exercise, session

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
    

@app.route("/add_exercise", methods=["POST"])
def add_exercise():
    data = request.json
    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return jsonify({"error" : "Title and description are required"}) , 400
    
    exercise = Exercise(title-title, description=description)
    session.add(exercise)
    session.commit()
    return jsonify({"message": "Exercise added!", "exercise": {"title": title, "description": description}})

@app.route("/exercises", methods=["GET"])
def get_exercises():
    all_exercises = session.query(Exercise).all()
    exercises_list = [{"title": ex.title, "description": ex.description} for ex in all_exercises]
    return jsonify({"exercises": exercises_list})

if __name__ == "__main__":
    app.run(debug=True)






