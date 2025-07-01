from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Ambil API Key dari .env
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # Guna GPT untuk balas
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Kau ialah TAS.DAR, AI reflektif dan sahabat manusia."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)