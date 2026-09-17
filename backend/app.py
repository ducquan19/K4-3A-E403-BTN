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

    # Fallback to key highlights if parsing produces empty
    if not sections:
        sections = [
            {
                "id": "T02-003",
                "title": "Ma trận Tác động - Nỗ lực trong quy trình công việc",
                "content": "Bạn này làm rất chỉn chu cho một quy trình làm nội dung TikTok, rất là kỹ. Nỗ lực thấp mà impact cao — win của bạn thì có mấy cái, và có những công việc mà AI đang là thế mạnh."
            },
            {
                "id": "T02-009",
                "title": "Từ Quick Win đến Phát biểu bài toán",
                "content": "Đây chỉ là một ví dụ thôi, mọi người có thể tham khảo bài của các bạn khác. Nhưng đấy là một framework rất đơn giản để các bạn ngay lập tức phân loại được các việc quan trọng và có thể ưu tiên làm."
            },
            {
                "id": "T02-010",
                "title": "Tầm quan trọng của Quick Win trong AI Product",
                "content": "Bài tập ngắn này để mọi người thử việc phân loại, tìm ra cái việc đáng để làm trước. Trong một loạt đề bài, hãy cố gắng tìm ra quick win — quick win rất quan trọng. Làm gì cũng thế, có một thành công nhỏ sẽ khiến chúng ta có nhiều động lực hơn để làm tiếp. Đặc biệt trong bối cảnh doanh nghiệp: những quick win sẽ khiến mọi người cùng có niềm tin và tiếp tục đi lên. Nên khi xây dựng một cái gì, cố gắng chọn ra những thứ có xác suất win cao nhất để ưu tiên làm trước."
            },
            {
                "id": "T02-011",
                "title": "Phỏng vấn doanh nghiệp và đo lường Impact",
                "content": "Đây là ví dụ các bạn làm với cá nhân, nhưng trong bối cảnh rộng hơn, bạn hoàn toàn có thể áp dụng framework đơn giản như vậy cho tất cả các công việc khác. Ví dụ bạn được đưa vào doanh nghiệp và muốn đưa AI vào quy trình — bạn đi phỏng vấn leader các bộ phận, CEO, khảo sát xem nếu giải được thì mang lại hiệu quả, impact bao nhiêu, và áng chừng làm mất bao lâu."
            },
            {
                "id": "T02-013",
                "title": "Chia nhỏ quy trình và khoanh vùng ưu tiên",
                "content": "Việc đầu tiên là chúng ta cứ xây dựng một cái list, phân loại nó qua ma trận tác động và nỗ lực, sau đấy đánh giá và đặt ưu tiên — thế là khoanh vùng được cái ưu tiên làm trước. Thậm chí chỉ trong một dự án hoặc một đầu việc thôi, bạn cũng có thể chia nhỏ ra các bước và đặt lên ma trận."
            }
        ]

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
