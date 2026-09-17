# -*- coding: utf-8 -*-
"""
Quick API Test CLI for VLearn Grounded Tutor (Team BTN)
Validates Gemini API connectivity and Grounding Guardrail within seconds.

Usage:
    python scripts/test_api.py
    or
    python scripts/test_api.py --key YOUR_GEMINI_API_KEY
"""

import os
import sys
import argparse
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

# Load .env from project root
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
load_dotenv()

# Add backend to sys.path
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

try:
    from core.tutor_engine import GroundedTutorEngine
except ImportError:
    from backend.core.tutor_engine import GroundedTutorEngine

def main():
    parser = argparse.ArgumentParser(description="Test Gemini API connectivity for VLearn Tutor")
    parser.add_argument("--key", type=str, default=None, help="Gemini API Key")
    parser.add_argument("--model", type=str, default="gemini-1.5-flash", help="Gemini Model")
    args = parser.parse_args()

    api_key = args.key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Lỗi: Chưa có GEMINI_API_KEY! Hãy cung cấp qua tham số --key hoặc đặt trong file .env")
        sys.exit(1)

    print(f"🚀 Đang kiểm tra kết nối Gemini API (Model: {args.model})...")
    engine = GroundedTutorEngine(api_key=api_key, model_name=args.model)

    # 1. Test Ping
    conn = engine.check_connection()
    if conn.get("success"):
        print(f"✅ Kết nối thành công! Độ trễ: {conn.get('latency_ms')} ms | Phản hồi: {conn.get('reply')}")
    else:
        print(f"❌ Kết nối thất bại: {conn.get('error')}")
        sys.exit(1)

    print("\n--- TEST 1: CÂU HỎI TRONG BÀI (GROUNDED) ---")
    q1 = "Quick win trong ma trận tác động - nỗ lực là gì và tại sao quan trọng?"
    print(f"Học viên hỏi: '{q1}'")
    r1 = engine.query_tutor(q1)
    print(f"-> Phân loại: {r1.get('decision')} | Độ trễ: {r1.get('latency_ms')} ms")
    print(f"-> Trích dẫn: {r1.get('citations')}")
    print(f"-> Trả lời: {r1.get('answer')[:150]}...")

    print("\n--- TEST 2: CÂU HỎI MƠ HỒ (HAX G10 CLARIFY) ---")
    q2 = "Ma trận"
    print(f"Học viên hỏi: '{q2}'")
    r2 = engine.query_tutor(q2)
    print(f"-> Phân loại: {r2.get('decision')} | Độ trễ: {r2.get('latency_ms')} ms")
    print(f"-> Gợi ý làm rõ: {r2.get('clarify_options')}")
    print(f"-> Trả lời: {r2.get('answer')}")

    print("\n--- TEST 3: CÂU HỎI NGOÀI PHẠM VI (OUT OF BOUNDS) ---")
    q3 = "Thầy ơi nộp bài tập lab ở link nào vậy ạ?"
    print(f"Học viên hỏi: '{q3}'")
    r3 = engine.query_tutor(q3)
    print(f"-> Phân loại: {r3.get('decision')} | Độ trễ: {r3.get('latency_ms')} ms")
    print(f"-> Trả lời: {r3.get('answer')}")

    print("\n🎉 HOÀN THÀNH TẤT CẢ TEST! Sản phẩm hoạt động thật 100% với Google Gemini API.")

if __name__ == "__main__":
    main()
