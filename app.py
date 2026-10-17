import os

from anthropic import Anthropic
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")
SYSTEM_PROMPT = (
    "Sen foydali sun'iy intellekt yordamchisan. "
    "Foydalanuvchi qaysi tilda yozsa, shu tilda qisqa va aniq javob ber."
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "Xabar bo'sh"}), 400

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        answer = "".join(
            block.text for block in response.content if block.type == "text"
        )
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Xatolik: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
