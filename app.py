from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 🟢 Root endpoint - untuk uji jika server hidup
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "alive",
        "message": "TAS.DAR backend is running on Railway!",
        "owner": "Saif Sudrah"
    })

# 🧪 Endpoint ujian POST (boleh buang jika tak perlu)
@app.route("/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({
        "received": data
    })

# 🔁 Endpoint ringkas untuk status
@app.route("/status", methods=["GET"])
def status():
    return "✅ TAS.DAR Backend OK"

# 🚀 Run server - penting untuk Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)