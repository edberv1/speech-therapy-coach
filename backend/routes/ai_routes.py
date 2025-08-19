from flask import Blueprint, request, jsonify
from openai import OpenAI
from config import Config

api = Blueprint("api", __name__)
client = OpenAI(api_key=Config.OPENAI_API_KEY)

@api.route("/exercises", methods=["GET"])
def get_exercises():
    return jsonify({"message": "Your exercises retrieval logic goes here"})

@api.route("/generate", methods=["POST"])
def generate_exercise():
    data = request.get_json()
    prompt = data.get("prompt", "Give me a simple speech therapy exercise")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    exercise_text = response.choices[0].message.content
    return jsonify({"exercise": exercise_text})
