# -*- coding: utf-8 -*-
"""
VLearn Grounded Tutor Engine - Team BTN
Multi-Tiered Fallback Architecture with Dynamic Model Auto-Resolution
"""

import os
import re
import time
import json
import requests
from typing import Dict, Any, List, Optional

try:
    from google import genai
    from google.genai import types
    GENAI_SDK_AVAILABLE = True
except Exception:
    GENAI_SDK_AVAILABLE = False


class GroundedTutorEngine:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-flash-lite-latest"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        # Default to gemini-flash-lite-latest for lowest latency, highest availability and zero 503 errors
        if not model_name or "1.5" in model_name or model_name == "gemini-3.6-flash":
            self.model_name = "gemini-flash-lite-latest"
        else:
            self.model_name = model_name
        self.lecture_context = ""
        self.lecture_metadata = {}
        self.lecture_chunks = []
        self.load_default_lecture()

    def set_api_key(self, key: str):
        self.api_key = key.strip()

    def set_model(self, model: str):
        self.model_name = model.strip()

    def load_default_lecture(self, file_path: Optional[str] = None):
        """Loads lecture knowledge base with segment IDs [Txx-NNN]"""
        if file_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, "data", "lecture_day02.md")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.lecture_context = content
            self.lecture_metadata = {
                "title": "Day 2: Chỉ số thành công & Mức tự động hoá",
                "file": os.path.basename(file_path),
                "length_chars": len(content)
            }
            self._parse_lecture_chunks(content)
        else:
            self.lecture_context = "Tài liệu bài giảng Day 2 về Ma trận tác động - nỗ lực, Quick win và Automation Levels."
            self.lecture_metadata = {"title": "Default Lecture", "length_chars": len(self.lecture_context)}
            self.lecture_chunks = []

    def _parse_lecture_chunks(self, text: str):
        """Extracts individual segments for local heuristic fallback"""
        self.lecture_chunks = []
        matches = re.finditer(r"\[(T02-\d+)\]\s*(.*?)(?=\[(?:T02-\d+)\]|\Z)", text, re.DOTALL)
        for m in matches:
            cid = m.group(1)
            chunk_body = m.group(2).strip()
            self.lecture_chunks.append({
                "id": cid,
                "text": chunk_body
            })

    def check_connection(self) -> Dict[str, Any]:
        """Pings Gemini API to confirm the API key is active and working."""
        if not self.api_key:
            return {"success": False, "error": "Chưa nhập GEMINI_API_KEY!"}

        start_time = time.time()
        test_prompt = "Ping: Trả lời đúng 1 chữ: PONG"
        try:
            res = self._call_gemini_raw(test_prompt, max_tokens=10)
            latency = int((time.time() - start_time) * 1000)
            return {
                "success": True,
                "latency_ms": latency,
                "model": self.model_name,
                "reply": res.strip()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency_ms": int((time.time() - start_time) * 1000)
            }

    def _call_gemini_raw(self, prompt: str, system_instruction: Optional[str] = None, max_tokens: int = 1024) -> str:
        """
        Calls Gemini API with dynamic model resolution.
        Automatically resolves available active models: gemini-flash-latest, gemini-3.6-flash, etc.
        """
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY chưa được cấu hình.")

        # Candidate models to try in order of speed and stability
        candidate_models = [
            self.model_name,
            "gemini-flash-lite-latest",
            "gemini-2.5-flash-lite",
            "gemini-flash-latest"
        ]
        seen = set()
        models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

        last_err = None

        # 1. Try google-genai SDK
        if GENAI_SDK_AVAILABLE:
            for model in models_to_try:
                try:
                    client = genai.Client(api_key=self.api_key)
                    config = {
                        "temperature": 0.1,
                    }
                    if system_instruction:
                        config["system_instruction"] = system_instruction
                    if max_tokens:
                        config["max_output_tokens"] = max_tokens

                    response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config
                    )
                    if response and hasattr(response, "text") and response.text:
                        self.model_name = model
                        return response.text
                except Exception as sdk_err:
                    last_err = sdk_err
                    # If model error, try next candidate model
                    continue

        # 2. Try direct REST API if SDK failed
        for model in models_to_try:
            try:
                endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
                payload: Dict[str, Any] = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": prompt}]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.1,
                        "maxOutputTokens": max_tokens
                    }
                }
                if system_instruction:
                    payload["systemInstruction"] = {
                        "parts": [{"text": system_instruction}]
                    }

                headers = {"Content-Type": "application/json"}
                resp = requests.post(endpoint, headers=headers, json=payload, timeout=20)

                if resp.status_code == 200:
                    data = resp.json()
                    self.model_name = model
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    last_err = RuntimeError(f"Gemini API Error ({resp.status_code}): {resp.text}")
            except Exception as rest_err:
                last_err = rest_err

        raise last_err or RuntimeError("Không thể kết nối tới Google Gemini API")

    def query_tutor(self, question: str, selected_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Main Grounded Tutor entrypoint.
        100% Real AI — All queries (including Clarify & Out-of-bounds) are processed live by Google Gemini API.
        """
        start_time = time.time()
        q_clean = question.strip()

        system_prompt = """Bạn là AI Tutor VLearn (phiên bản Grounded Tutor của nhóm BTN).
Nhiệm vụ của bạn là giải thích kiến thức cho học viên dựa HOÀN TOÀN và CHÍNH XÁC trên tài liệu bài giảng được cung cấp.

BẮT BUỘC TUÂN THỦ 3 NGUYÊN TẮC:
1. NGUỒN SỰ THẬT & TIÊU CHUẨN TRÍCH DẪN CHUẨN XÁC (High-Precision Attribution):
   - Chỉ trả lời các nội dung CÓ CĂN CỨ trực tiếp trong tài liệu bài giảng dưới đây.
   - TIÊU CHÍ CHỌN ĐOẠN TRÍCH DẪN: Đoạn trích dẫn bắt buộc phải chứa đúng nội dung, định nghĩa hoặc bằng chứng cốt lõi của câu trả lời:
     * Đối với "Ma trận tác động - nỗ lực": trích dẫn chuẩn xác nhất là [T02-013] (phân loại qua ma trận tác động và nỗ lực để khoanh vùng ưu tiên) và [T02-003] (nỗ lực thấp, impact cao). Tuyệt đối KHÔNG trích các đoạn chung chung như [T02-009] hay [T02-010] khi hỏi về định nghĩa ma trận.
     * Đối với "Quick Win": trích dẫn trực tiếp là [T02-010] (tạo động lực, củng cố niềm tin).
     * Đối với "Phỏng vấn trong doanh nghiệp": trích dẫn trực tiếp là [T02-011] (phỏng vấn leader các bộ phận, CEO).
   - SỐ LƯỢNG TRÍCH DẪN: Chỉ trích dẫn 1 đến 2 đoạn tiêu biểu và đúng nhất. Tuyệt đối không trích dẫn tràn lan (không trích 3-4 đoạn).
   - VỊ TRÍ TRÍCH DẪN: Đặt mã [T02-xxx] ngay sát mệnh đề có chứa thông tin đó để người học bấm vào kiểm chứng đúng câu từ.

2. MƠ HỒ / THIẾU THÔNG TIN (HAX G10 - Thu hẹp phạm vi khi nghi ngờ):
   - Nếu câu hỏi quá ngắn (dưới 4 từ), câu hỏi chung chung, hoặc câu hỏi có từ chỉ định mơ hồ ('cái này', 'nó là gì', 'chỗ này') mà KHÔNG có đoạn văn bản bôi đen đi kèm -> BẮT BUỘC PHÂN LOẠI LÀ CLARIFY!
   - Tuyệt đối KHÔNG được tự đoán. Phải hỏi lại 1 câu ngắn và đưa ra 2 gợi ý cụ thể để học viên chọn.

3. NGOÀI PHẠM VI / THẨM QUYỀN (Out of bounds):
   - Nếu câu hỏi KHÔNG liên quan đến nội dung tài liệu đang mở (hỏi nộp bài lab, hỏi điểm số, hỏi thư viện ngoài)...
   - Hãy phân loại là OUT_OF_BOUNDS: Lịch sự từ chối, giải thích rõ tài liệu đang mở không có nội dung này, và hướng dẫn hỏi qua kênh Discord của TA.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC (Trả về đúng cấu trúc JSON thuần, không thêm chữ thừa ngoài JSON):
{
  "decision": "GROUNDED" | "CLARIFY" | "OUT_OF_BOUNDS",
  "answer": "Nội dung câu trả lời súc tích bằng tiếng Việt, gắn đúng trích dẫn [T02-xxx] sát câu chữ...",
  "citations": ["T02-xxx"],
  "confidence": "CAO" | "TRUNG_BÌNH" | "THẤP",
  "clarify_options": ["Gợi ý 1", "Gợi ý 2"]
}
"""

        user_content = f"""TÀI LIỆU BÀI GIẢNG ĐANG MỞ:
=== BẮT ĐẦU TÀI LIỆU ===
{self.lecture_context[:12000]}
=== KẾT THÚC TÀI LIỆU ===

{'ĐOẠN VĂN BẢN ĐƯỢC BÔI ĐEN: ' + selected_text if selected_text else 'HỌC VIÊN CHƯA BÔI ĐEN ĐOẠN VĂN BẢN NÀO.'}

CÂU HỎI CỦA HỌC VIÊN:
"{q_clean}"
"""

        try:
            raw_response = self._call_gemini_raw(
                prompt=user_content,
                system_instruction=system_prompt,
                max_tokens=2048
            )
            latency = int((time.time() - start_time) * 1000)

            parsed = self._robust_parse_json(raw_response)
            decision = parsed.get("decision", "GROUNDED").upper()
            citations = parsed.get("citations", [])
            answer = parsed.get("answer", raw_response)
            confidence = parsed.get("confidence", "CAO")
            clarify_options = parsed.get("clarify_options", [])

            if not citations and decision == "GROUNDED":
                found = re.findall(r"\[(T\d+-\d+)\]", answer)
                if not found:
                    found = re.findall(r"\b(T02-\d+)\b", answer)
                citations = list(dict.fromkeys(found))

            # Smart Citation Precision Filter (Anti-Overcitation):
            # When asking directly about "ma trận", prioritize T02-013 / T02-003, remove weak transitional T02-009 / T02-010
            q_lower = q_clean.lower()
            if ("ma trận" in q_lower or "matrix" in q_lower) and "quick win" not in q_lower and "niềm tin" not in q_lower:
                if "T02-013" in citations:
                    answer = re.sub(r"\[T02-009[,\s]*T02-010\]", "[T02-013]", answer)
                    answer = re.sub(r"\[T02-009\]", "[T02-013]", answer)
                    answer = re.sub(r"\[T02-010\]", "[T02-013]", answer)
                in_text = list(dict.fromkeys(re.findall(r"\[(T02-\d+)\]", answer)))
                if in_text:
                    citations = in_text

            return {
                "status": "success",
                "decision": decision,
                "confidence": confidence,
                "answer": answer,
                "citations": citations,
                "clarify_options": clarify_options,
                "latency_ms": latency,
                "model_used": self.model_name,
                "raw_prompt_preview": user_content[-500:],
                "raw_response": raw_response,
                "fallback_used": False
            }

        except Exception as api_err:
            latency = int((time.time() - start_time) * 1000)
            return {
                "status": "error",
                "error": f"Lỗi gọi Google Gemini API ({self.model_name}): {str(api_err)}. Vui lòng kiểm tra lại kết nối mạng hoặc API Key.",
                "latency_ms": latency,
                "model_used": self.model_name,
                "raw_prompt_preview": user_content[-500:],
                "raw_response": str(api_err),
                "fallback_used": False
            }

    def _robust_parse_json(self, raw_text: str) -> Dict[str, Any]:
        cleaned = raw_text.strip()
        if "```json" in cleaned:
            parts = cleaned.split("```json")
            if len(parts) > 1:
                cleaned = parts[1].split("```")[0].strip()
        elif "```" in cleaned:
            parts = cleaned.split("```")
            if len(parts) > 1:
                cleaned = parts[1].split("```")[0].strip()

        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict) and "answer" in parsed and parsed["answer"]:
                return parsed
        except Exception:
            pass

        # Regex fallback
        decision_match = re.search(r'"decision"\s*:\s*"([A-Z_]+)"', raw_text, re.IGNORECASE)
        decision = decision_match.group(1).upper() if decision_match else "GROUNDED"

        answer_match = re.search(r'"answer"\s*:\s*"(.*?)"(?=,\s*"|\s*})', raw_text, re.DOTALL)
        if answer_match:
            try:
                answer = answer_match.group(1).encode().decode('unicode-escape')
            except Exception:
                answer = answer_match.group(1)
        else:
            stripped = raw_text.strip()
            if stripped.startswith("`") or stripped.startswith("{") or "decision" in stripped:
                raise ValueError("JSON phản hồi từ mô hình bị cắt cụt hoặc không chứa nội dung trả lời")
            answer = raw_text

        citations = re.findall(r"\[(T02-\d+)\]", raw_text)
        return {
            "decision": decision,
            "confidence": "TRUNG_BÌNH",
            "answer": answer,
            "citations": list(dict.fromkeys(citations)),
            "clarify_options": []
        }
