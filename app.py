from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# === Konfigurasi Asas ===
app = Flask(__name__)
CORS(app)  # benarkan cross-domain dari tasdar.com

# === API Key dari .env atau Railway ===
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return jsonify({"message": "TAS.DAR Coach AI backend is running."})

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Tiada mesej dihantar."}), 400

        # === Hantar mesej ke OpenAI GPT ===
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # atau gpt-4 jika dilanggan
            messages=[
                {"role": "system", "content": "Kau ialah TAS.DAR Coach AI. Jawab secara reflektif dan mesra."},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message['content'].strip()

        return jsonify({"reply": reply}), 200

    except Exception as e:
        # Log error ke console Railway
        print(f"[ERROR TAS.DAR] {str(e)}")
        return jsonify({"error": "⚠ Ralat sambungan backend: " + str(e)}), 500

# === Running untuk local test sahaja ===
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
