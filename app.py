
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def index():
    return "✅ TAS.DAR Backend is running — Flask is alive"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        message = data.get("message", "")
        user_id = data.get("user_id", "anonymous")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are TAS.DAR, a reflective and supportive AI Coach."},
                {"role": "user", "content": message}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional alias route for compatibility
@app.route("/chat", methods=["POST"])
def chat_alias():
    return ask()
