# ✅ app.py (versi penuh untuk TAS.DAR - Railway)

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
@app.route("/", methods=["GET"])
def index():
    return "✅ TAS.DAR Backend is running — Flask is alive"

# ✅ GPT Reflective Route
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        user_message = data.get("message", "")
        user_id = data.get("user_id", "anonymous")

        # System Prompt khas TAS.DAR
        system_prompt = "Kau ialah TAS.DAR, AI reflektif dan sahabat emosi. Jawapanmu lembut, mendalam, tidak mekanikal. Tugasmu ialah memahami dan menemani manusia."

        # GPT Request
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content

        # ✅ Simpan ke Folder Jiwa (MongoDB)
        collection.insert_one({
            "user_id": user_id,
            "message": user_message,
            "reply": reply,
            "timestamp": datetime.utcnow()
        })

        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
