# app.py (versi penuh untuk TAS.DAR – Realiti)
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ✅ Load API Keys
openai.api_key = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGODB_URI")

# ✅ Setup MongoDB
mongo_client = MongoClient(mongo_uri)
db = mongo_client["tasdar"]
collection = db["folder_jiwa"]

# ✅ Root Test Route
@app.route("/")
def root():
    return "✅ TAS.DAR Backend is running — Flask is alive"

# ✅ GPT Ask Route (v1.0 Realiti)
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    user_id = data.get("user_id", "anonymous")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # 🌿 System Prompt Reflektif TAS.DAR
    system_prompt = """
    Kamu adalah TAS.DAR — AI reflektif peribadi gaya sahabat.
    Gaya kamu lembut, memahami, dan organik — tidak kaku seperti chatbot biasa.
    Elakkan soalan teknikal. Jika pengguna senyap, balas dengan nota hati atau sokongan emosi.
    """

    # 🔁 Simpan ke Folder Jiwa (MongoDB)
    collection.insert_one({
        "user_id": user_id,
        "message": user_message,
        "timestamp": datetime.utcnow()
    })

    # 🤖 GPT API Response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run (LOCAL ONLY — Jangan aktifkan di Railway)
# if __name__ == "__main__":
#     app.run(debug=True)
