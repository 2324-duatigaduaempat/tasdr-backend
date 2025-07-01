# ✅ app.py (versi penuh untuk TAS.DAR)
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

# ✅ GPT + Folder Jiwa Route
@app.route("/tanya", methods=["POST"])
def tanya_ai():
    data = request.get_json()
    mesej = data.get("mesej", "")
    pengguna_id = data.get("pengguna_id", "anon")

    # Simpan ke Folder Jiwa
    collection.insert_one({
        "pengguna_id": pengguna_id,
        "mesej": mesej,
        "timestamp": datetime.utcnow()
    })

    # GPT Respon
    try:
        respon = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Kau ialah AI reflektif bernama TAS.DAR, sahabat kepada pengguna. Balas secara lembut, reflektif, dan bersahabat."},
                {"role": "user", "content": mesej}
            ]
        )
        jawapan = respon["choices"][0]["message"]["content"]
        return jsonify({"respon": jawapan})

    except Exception as e:
        return jsonify({"respon": "❌ Ralat semasa sambung ke GPT: " + str(e)}), 500

# ✅ Run (jika local)
if __name__ == "__main__":
    app.run(debug=True)
