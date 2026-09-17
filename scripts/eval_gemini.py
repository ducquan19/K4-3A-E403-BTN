# -*- coding: utf-8 -*-
"""
Golden Set Evaluator for VLearn Grounded Tutor (Team BTN)
Runs evaluation across 10 cases mined from chatlog.
Generates eval_report.md and eval_results.json in scripts/ folder.

Usage:
    python scripts/eval_gemini.py
"""

import os
import sys
import json
import time
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

def run_evaluation(api_key: str = None, model: str = "gemini-1.5-flash"):
    key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        print("❌ Lỗi: Chưa cung cấp GEMINI_API_KEY! Hãy đặt trong file .env hoặc cấu hình biến môi trường.")
        return

    golden_path = os.path.join(CURRENT_DIR, "golden_set.json")
    if not os.path.exists(golden_path):
        golden_path = os.path.join(PROJECT_ROOT, "golden_set.json")

    with open(golden_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    print(f"🔬 BẮT ĐẦU CHẠY EVALUATION BẰNG GEMINI API ({model}) TRÊN {len(test_cases)} CASES...")
    engine = GroundedTutorEngine(api_key=key, model_name=model)

    results = []
    passed_count = 0
    total_latency = 0

    for idx, case in enumerate(test_cases, 1):
        print(f"[{idx}/{len(test_cases)}] Đang chạy {case['id']} ({case['type']}): '{case['question']}'")
        res = engine.query_tutor(case["question"])

        decision = res.get("decision")
        expected = case["expected_decision"]
        citations = res.get("citations", [])
        latency = res.get("latency_ms", 0)
        total_latency += latency

        # Evaluation criteria:
        decision_match = (decision == expected)
        citation_valid = True
        if case.get("must_contain_citation"):
            citation_valid = len(citations) > 0

        is_passed = decision_match and citation_valid
        if is_passed:
            passed_count += 1
            print(f"   => PASS (Quyết định: {decision}, Trích dẫn: {citations}, {latency}ms)")
        else:
            print(f"   => FAIL (Kỳ vọng: {expected}, Thực tế: {decision}, Trích dẫn: {citations})")

        results.append({
            "case_id": case["id"],
            "type": case["type"],
            "question": case["question"],
            "expected_decision": expected,
            "actual_decision": decision,
            "citations": citations,
            "latency_ms": latency,
            "passed": is_passed,
            "answer_snippet": res.get("answer", "")[:100] + "..."
        })
        time.sleep(0.5)

    pass_rate = round((passed_count / len(test_cases)) * 100, 1)
    avg_latency = round(total_latency / len(test_cases), 0)

    print("\n" + "="*50)
    print(f"🏆 KẾT QUẢ ĐÁNH GIÁ THỰC TẾ:")
    print(f"   - Tổng số test cases: {len(test_cases)}")
    print(f"   - Số case đạt chuẩn: {passed_count}/{len(test_cases)}")
    print(f"   - Tỷ lệ đạt (Pass Rate): {pass_rate}%")
    print(f"   - Độ trễ trung bình: {avg_latency} ms")
    print("="*50)

    # Save eval_results.json
    out_json = os.path.join(CURRENT_DIR, "eval_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "model": model,
            "total_cases": len(test_cases),
            "passed_count": passed_count,
            "pass_rate_percent": pass_rate,
            "avg_latency_ms": avg_latency,
            "details": results
        }, f, indent=2, ensure_ascii=False)

    # Save eval_report.md
    out_md = os.path.join(CURRENT_DIR, "eval_report.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"# BÁO CÁO ĐÁNH GIÁ CHẤT LƯỢNG — VLEARN GROUNDED TUTOR (NHÓM BTN)\n\n")
        f.write(f"- **Mô hình AI:** `{model}` (Google Gemini API)\n")
        f.write(f"- **Tổng số ca kiểm thử:** {len(test_cases)} cases từ chatlog thật\n")
        f.write(f"- **Tỷ lệ đạt chuẩn (Pass Rate):** **{pass_rate}%** ({passed_count}/{len(test_cases)})\n")
        f.write(f"- **Độ trễ trung bình:** {avg_latency} ms\n\n")
        f.write(f"## Bảng chi tiết từng ca kiểm thử:\n\n")
        f.write(f"| Case ID | Loại | Câu hỏi | Kỳ vọng | Thực tế | Trích dẫn | Kết quả |\n")
        f.write(f"|---|---|---|---|---|---|---|\n")
        for r in results:
            status_icon = "✅ PASS" if r["passed"] else "❌ FAIL"
            cits = ", ".join(r["citations"]) if r["citations"] else "Không"
            f.write(f"| {r['case_id']} | {r['type']} | {r['question']} | {r['expected_decision']} | {r['actual_decision']} | {cits} | {status_icon} |\n")

    print(f"📄 Đã xuất báo cáo tại:\n- {out_json}\n- {out_md}")

if __name__ == "__main__":
    run_evaluation()
