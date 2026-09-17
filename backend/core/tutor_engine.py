# -*- coding: utf-8 -*-
"""
VLearn Grounded Tutor Engine - Team BTN
Connects to Google Gemini API (gemini-1.5-flash / gemini-2.0-flash / gemini-1.5-pro)
Implements Grounded Answering, Citations, Ambiguity Clarification (HAX G10), and Out-of-Bounds Protection.
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
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        self.lecture_context = ""
        self.lecture_metadata = {}
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
        else:
            self.lecture_context = "Tài liệu bài giảng Day 2 về Ma trận tác động - nỗ lực, Quick win và Automation Levels."
            self.lecture_metadata = {"title": "Default Lecture", "length_chars": len(self.lecture_context)}

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
        """Calls Gemini API via Google GenAI SDK with fallback to direct REST API."""
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY chưa được cấu hình. Vui lòng nhập API Key!")

        # 1. Try modern google-genai SDK if available
        if GENAI_SDK_AVAILABLE:
            try:
                client = genai.Client(api_key=self.api_key)
                config = {}
                if system_instruction:
                    config["system_instruction"] = system_instruction
                if max_tokens:
                    config["max_output_tokens"] = max_tokens

                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config if config else None
                )
                if response and hasattr(response, "text") and response.text:
                    return response.text
            except Exception:
                # Fallback to direct REST API
                pass

        # 2. REST API fallback (guaranteed cross-platform reliability)
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        payload: Dict[str, Any] = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": max_tokens
            }
        }
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        headers = {"Content-Type": "application/json"}
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=25)

        if resp.status_code != 200:
            raise RuntimeError(f"Gemini API Error ({resp.status_code}): {resp.text}")

        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            raise RuntimeError(f"Malformed Gemini response: {resp.text}")

    def query_tutor(self, question: str, selected_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Main Grounded Tutor entrypoint.
        Executes strict factual grounding against the open lecture materials.
        """
        start_time = time.time()
        q_clean = question.strip()

        # Build Grounding System Prompt
        system_prompt = """Bạn là AI Tutor VLearn (phiên bản Grounded Tutor của nhóm BTN).
Nhiệm vụ của bạn là giải thích kiến thức cho học viên dựa HOÀN TOÀN và CHÍNH XÁC trên tài liệu bài giảng được cung cấp.

BẮT BUỘC TUÂN THỦ 3 NGUYÊN TẮC:
1. NGUỒN SỰ THẬT (Factuality & Anti-hallucination):
   - Chỉ trả lời các nội dung CÓ CĂN CỨ trong tài liệu bài giảng dưới đây.
   - Luôn kèm theo mã đoạn trích dẫn dạng [T02-xxx] ngay cạnh luận điểm để người học tự kiểm chứng.
   - Tuyệt đối không phỏng đoán, không tự bịa thêm thông tin ngoài tài liệu.

2. MƠ HỒ / THIẾU THÔNG TIN (HAX G10 - Thu hẹp phạm vi khi nghi ngờ):
   - Nếu câu hỏi quá ngắn (dưới 3 từ) hoặc quá chung chung (ví dụ: 'cái này là gì', 'ma trận'), KHÔNG ĐƯỢC đoán mò.
   - Hãy phân loại là CLARIFY: Đặt 1 câu hỏi làm rõ ngắn gọn và đưa ra 2 gợi ý cụ thể để học viên bấm chọn.

3. NGOÀI PHẠM VI / THẨM QUYỀN (Out of bounds):
   - Nếu câu hỏi KHÔNG liên quan đến nội dung tài liệu đang mở (ví dụ: hỏi nộp bài lab ở đâu, hỏi tool khác ngoài bài, hỏi chuyện riêng, hỏi kiến thức môn khác)...
   - Hãy phân loại là OUT_OF_BOUNDS: Lịch sự từ chối, giải thích rõ tài liệu đang mở không có nội dung này, và hướng dẫn hỏi qua kênh Discord của TA hoặc xem thông báo chung.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC (Trả về đúng cấu trúc JSON, không thêm chữ thừa ngoài JSON):
{
  "decision": "GROUNDED" | "CLARIFY" | "OUT_OF_BOUNDS",
  "confidence": "CAO" | "TRUNG_BÌNH" | "THẤP",
  "citations": ["T02-009", "T02-010"],
  "answer": "Nội dung câu trả lời súc tích bằng tiếng Việt...",
  "clarify_options": ["Gợi ý 1", "Gợi ý 2"]
}
"""

        user_content = f"""TÀI LIỆU BÀI GIẢNG ĐANG MỞ:
=== BẮT ĐẦU TÀI LIỆU ===
{self.lecture_context[:12000]}
=== KẾT THÚC TÀI LIỆU ===

{'ĐOẠN VĂN BẢN ĐƯỢC BÔI ĐEN: ' + selected_text if selected_text else ''}

CÂU HỎI CỦA HỌC VIÊN:
"{q_clean}"
"""

        raw_response = ""
        try:
            raw_response = self._call_gemini_raw(
                prompt=user_content,
                system_instruction=system_prompt,
                max_tokens=800
            )
            latency = int((time.time() - start_time) * 1000)

            # Clean JSON if wrapped in markdown
            cleaned_json = raw_response.strip()
            if "```json" in cleaned_json:
                cleaned_json = cleaned_json.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned_json:
                cleaned_json = cleaned_json.split("```")[1].split("```")[0].strip()

            parsed = json.loads(cleaned_json)
            decision = parsed.get("decision", "GROUNDED").upper()
            citations = parsed.get("citations", [])
            answer = parsed.get("answer", raw_response)
            confidence = parsed.get("confidence", "CAO")
            clarify_options = parsed.get("clarify_options", [])

            # Extract any [T02-xxx] citations from text if citations list was empty
            if not citations:
                found = re.findall(r"\[T\d+-\d+\]", answer)
                citations = list(set([c.replace("[", "").replace("]", "") for c in found]))

            return {
                "status": "success",
                "decision": decision,
                "confidence": confidence,
                "answer": answer,
                "citations": citations,
                "clarify_options": clarify_options,
                "latency_ms": latency,
                "model_used": self.model_name,
                "raw_prompt_preview": user_content[-600:],
                "raw_response": raw_response,
                "is_live_call": True
            }

        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            return {
                "status": "error",
                "decision": "ERROR",
                "confidence": "THẤP",
                "answer": f"Lỗi khi xử lý qua Gemini API: {str(e)}",
                "citations": [],
                "clarify_options": [],
                "latency_ms": latency,
                "model_used": self.model_name,
                "raw_prompt_preview": user_content[-600:],
                "raw_response": raw_response or str(e),
                "is_live_call": True
            }
