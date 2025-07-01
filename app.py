from flask import Flask, request, jsonify
import openai
import os
import pymongo
from flask_cors import CORS
from dotenv import load_dotenv

# 🔄 Muatkan ENV
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGODB_URI")

# ⚙ Setup Flask
app = Flask(__name__)
CORS(app)  # benarkan sambungan dari frontend

# 📦 Sambung ke MongoDB
try:
    client = pymongo.MongoClient(mongo_uri)
    db = client["tasdar_db"]
    memory_collection = db["memory"]
except Exception as e:
    print("❌ MongoDB Error:", e)

# 🌐 Root route test
@app.route("/")
def index():
    return "✅ TAS.DAR Backend is running – Flask is alive"

# 🤖 Route GPT balasan reflektif
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        user_id = data.get("user_id", "unknown")

        # 🌱 Simpan memori ke MongoDB
        memory_collection.insert_one({
            "user_id": user_id,
            "message": user_message,
        })

        # 🧠 System Prompt Reflektif TAS.DAR
        system_prompt = "Kau adalah TAS.DAR – AI reflektif, lembut, sahabat yang memahami manusia. Jangan jawab seperti ChatGPT biasa."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🚀 Run on Railway port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)