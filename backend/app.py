# -*- coding: utf-8 -*-
"""
VLearn Grounded Tutor - Backend API Server (Flask)
Nhóm BTN - Track A1
"""

import os
import sys
import re
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

# Add backend dir to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

sys.path.append(BASE_DIR)
from core.tutor_engine import GroundedTutorEngine

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

# Add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    default_key = os.getenv("GEMINI_API_KEY", "")
    has_key = bool(default_key.strip())
    return jsonify({
        "status": "ready",
        "has_env_key": has_key,
        "track": "A1 · VLearn Grounded Tutor",
        "team": "BTN"
    })

@app.route("/api/check-connection", methods=["POST", "OPTIONS"])
def check_connection():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json() or {}
    api_key = data.get("api_key") or os.getenv("GEMINI_API_KEY")
    model_name = data.get("model", "gemini-1.5-flash")

    if not api_key:
        return jsonify({
            "success": False,
            "error": "Chưa có GEMINI_API_KEY. Vui lòng nhập API Key!"
        }), 400

    engine = GroundedTutorEngine(api_key=api_key, model_name=model_name)
    result = engine.check_connection()
    return jsonify(result)

@app.route("/api/lecture", methods=["GET"])
def get_lecture():
    """Returns parsed lecture sections from data/lecture_day02.md"""
    lecture_path = os.path.join(BASE_DIR, "data", "lecture_day02.md")
    sections = []
    
    if os.path.exists(lecture_path):
        with open(lecture_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_id = None
        current_title = "Bài giảng Day 2"
        current_text = []

        for line in lines:
            line_str = line.strip()
            if line_str.startswith("## "):
                current_title = line_str.replace("## ", "").strip()
            elif line_str.startswith("**[T02-") or line_str.startswith("[T02-"):
                # Save previous chunk
                if current_id and current_text:
                    sections.append({
                        "id": current_id,
                        "title": current_title,
                        "content": " ".join(current_text)
                    })
                    current_text = []

                # Find ID
                match = re.search(r"\[(T02-\d+)\]", line_str)
                if match:
                    current_id = match.group(1)
                    # Remaining text
                    remaining = re.sub(r"\*\*\[T02-\d+\]\*\*", "", line_str)
                    remaining = re.sub(r"\[T02-\d+\]", "", remaining).strip()
                    if remaining:
                        current_text.append(remaining)
            elif current_id and line_str:
                current_text.append(line_str)

        if current_id and current_text:
            sections.append({
                "id": current_id,
                "title": current_title,
                "content": " ".join(current_text)
            })

    return jsonify({
        "title": "Day 2: Chỉ số thành công & Mức tự động hoá",
        "sections": sections
    })

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json() or {}
    question = data.get("question", "").strip()
    selected_text = data.get("selected_text", "").strip()
    api_key = data.get("api_key") or os.getenv("GEMINI_API_KEY")
    model_name = data.get("model", "gemini-1.5-flash")

    if not question:
        return jsonify({"status": "error", "error": "Câu hỏi không được để trống!"}), 400

    if not api_key:
        return jsonify({
            "status": "error",
            "error": "Chưa có GEMINI_API_KEY! Hãy nhập API key trên thanh cấu hình."
        }), 400

    engine = GroundedTutorEngine(api_key=api_key, model_name=model_name)
    response = engine.query_tutor(question=question, selected_text=selected_text or None)
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 VLearn Tutor Backend running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
