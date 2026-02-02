"""Tiny Flask-based API for manual QA testing (placeholder)."""
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    question = data.get("question")
    return jsonify({"answer": f"[stub] received: {question}"})


if __name__ == "__main__":
    app.run(port=8080)
