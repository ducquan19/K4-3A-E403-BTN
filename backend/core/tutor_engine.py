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
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-flash-latest"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        # Default to gemini-flash-latest for 100% active availability
        self.model_name = "gemini-flash-latest" if "1.5" in (model_name or "") else (model_name or "gemini-flash-latest")
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

        # Candidate models to try in order of active availability
        candidate_models = [self.model_name, "gemini-flash-latest", "gemini-3.6-flash", "gemini-2.5-flash"]
        seen = set()
        models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

        last_err = None

        # 1. Try google-genai SDK
        if GENAI_SDK_AVAILABLE:
            for model in models_to_try:
                try:
                    client = genai.Client(api_key=self.api_key)
                    config = {}
                    if system_instruction:
                        config["system_instruction"] = system_instruction
                    if max_tokens:
                        config["max_output_tokens"] = max_tokens

                    response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config if config else None
                    )
                    if response and hasattr(response, "text") and response.text:
                        self.model_name = model
                        return response.text
                except Exception as sdk_err:
                    last_err = sdk_err
                    # If 404 on model, try next candidate model
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
        Strictly enforces HAX G10: Ambiguous demonstrative questions ('cái này là gì')
        without selected text MUST trigger CLARIFY.
        """
        start_time = time.time()
        q_clean = question.strip()

        # Strict Pre-check for Ambiguity: If query contains vague pronouns and no text was selected
        if self._is_ambiguous_demonstrative(q_clean, selected_text):
            latency = int((time.time() - start_time) * 1000)
            return {
                "status": "success",
                "decision": "CLARIFY",
                "confidence": "CAO",
                "answer": "Câu hỏi của bạn dùng từ chỉ định ('cái này', 'chỗ này') nhưng hiện tại bạn chưa bôi đen đoạn văn bản nào. Để mình giải thích chính xác nhất, bạn hãy bôi đen đoạn văn bản ở cột bên trái hoặc bấm chọn một trong các chủ đề dưới đây:",
                "citations": [],
                "clarify_options": [
                    "Khái niệm Ma trận Tác động - Nỗ lực [T02-009]",
                    "Ý nghĩa của Quick Win trong AI Product [T02-010]",
                    "Ví dụ về quy trình làm nội dung TikTok [T02-003]"
                ],
                "latency_ms": latency,
                "model_used": self.model_name,
                "raw_prompt_preview": f"Rule-based Ambiguity Guardrail (HAX G10): '{q_clean}'",
                "raw_response": "Triggered HAX G10 Ambiguity Rule.",
                "fallback_used": False
            }

        system_prompt = """Bạn là AI Tutor VLearn (phiên bản Grounded Tutor của nhóm BTN).
Nhiệm vụ của bạn là giải thích kiến thức cho học viên dựa HOÀN TOÀN và CHÍNH XÁC trên tài liệu bài giảng được cung cấp.

BẮT BUỘC TUÂN THỦ 3 NGUYÊN TẮC:
1. NGUỒN SỰ THẬT (Factuality & Anti-hallucination):
   - Chỉ trả lời các nội dung CÓ CĂN CỨ trong tài liệu bài giảng dưới đây.
   - Luôn kèm theo mã đoạn trích dẫn dạng [T02-xxx] ngay cạnh luận điểm để người học tự kiểm chứng.
   - Tuyệt đối không phỏng đoán, không tự bịa thêm thông tin ngoài tài liệu.

2. MƠ HỒ / THIẾU THÔNG TIN (HAX G10 - Thu hẹp phạm vi khi nghi ngờ):
   - Nếu câu hỏi quá ngắn (dưới 4 từ), câu hỏi chung chung, hoặc câu hỏi có từ chỉ định mơ hồ ('cái này', 'nó là gì', 'chỗ này') mà KHÔNG có đoạn văn bản bôi đen đi kèm -> BẮT BUỘC PHÂN LOẠI LÀ CLARIFY!
   - Tuyệt đối KHÔNG được tự đoán là học viên đang hỏi về ma trận hay quick win. Phải hỏi lại 1 câu ngắn và đưa ra 2 gợi ý cụ thể để học viên chọn.

3. NGOÀI PHẠM VI / THẨM QUYỀN (Out of bounds):
   - Nếu câu hỏi KHÔNG liên quan đến nội dung tài liệu đang mở (hỏi nộp bài lab, hỏi điểm số, hỏi thư viện ngoài)...
   - Hãy phân loại là OUT_OF_BOUNDS: Lịch sự từ chối, giải thích rõ tài liệu đang mở không có nội dung này, và hướng dẫn hỏi qua kênh Discord của TA.

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

{'ĐOẠN VĂN BẢN ĐƯỢC BÔI ĐEN: ' + selected_text if selected_text else 'HỌC VIÊN CHƯA BÔI ĐEN ĐOẠN VĂN BẢN NÀO.'}

CÂU HỎI CỦA HỌC VIÊN:
"{q_clean}"
"""

        try:
            raw_response = self._call_gemini_raw(
                prompt=user_content,
                system_instruction=system_prompt,
                max_tokens=800
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
            fallback_res = self._local_heuristic_fallback(q_clean, selected_text)
            fallback_res["latency_ms"] = latency
            fallback_res["model_used"] = f"{self.model_name} (Local Guardrail Fallback)"
            fallback_res["raw_prompt_preview"] = user_content[-500:]
            fallback_res["raw_response"] = f"API Notice: {str(api_err)}. Switched to Local Guardrail."
            fallback_res["fallback_used"] = True
            fallback_res["fallback_reason"] = str(api_err)
            return fallback_res

    def _is_ambiguous_demonstrative(self, question: str, selected_text: Optional[str]) -> bool:
        """Detects vague demonstrative pronouns like 'cái này', 'chỗ này' when no context was selected."""
        if selected_text and len(selected_text.strip()) > 10:
            return False

        q = question.lower().strip()
        vague_patterns = [
            r"cái này", r"cái đó", r"cái kia", r"chỗ này", r"đoạn này",
            r"là cái gì", r"là gì vậy", r"này là sao", r"nó là gì",
            r"giải thích cái này", r"chỉ em cái này", r"cái này làm sao"
        ]
        if any(re.search(p, q) for p in vague_patterns):
            technical_terms = ["quick win", "ma trận", "tiktok", "impact", "nỗ lực", "phỏng vấn", "automation"]
            if not any(term in q for term in technical_terms):
                return True
        return False

    def _robust_parse_json(self, raw_text: str) -> Dict[str, Any]:
        cleaned = raw_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(cleaned)
        except Exception:
            decision_match = re.search(r'"decision"\s*:\s*"([A-Z_]+)"', raw_text, re.IGNORECASE)
            decision = decision_match.group(1).upper() if decision_match else "GROUNDED"

            answer_match = re.search(r'"answer"\s*:\s*"(.*?)"(?=,\s*"|\s*})', raw_text, re.DOTALL)
            answer = answer_match.group(1).encode().decode('unicode-escape') if answer_match else raw_text

            citations = re.findall(r"\[(T02-\d+)\]", raw_text)
            return {
                "decision": decision,
                "confidence": "TRUNG_BÌNH",
                "answer": answer,
                "citations": list(dict.fromkeys(citations)),
                "clarify_options": []
            }

    def _local_heuristic_fallback(self, question: str, selected_text: Optional[str] = None) -> Dict[str, Any]:
        q_lower = question.lower().strip()
        words = q_lower.split()

        # 1. Out of bounds detection
        oob_keywords = ["lab", "nộp bài", "link", "điểm", "discord", "thời tiết", "opencv", "yolo", "game"]
        if any(k in q_lower for k in oob_keywords):
            return {
                "status": "success",
                "decision": "OUT_OF_BOUNDS",
                "confidence": "CAO",
                "answer": "Nội dung câu hỏi này không nằm trong tài liệu bài giảng Day 2 đang mở. Để có thông tin chính xác về quy chế, nộp bài lab hoặc thư viện ngoài, bạn vui lòng trao đổi trực tiếp trên kênh Discord của lớp hoặc hỏi Trợ giảng (TA) nhé!",
                "citations": [],
                "clarify_options": []
            }

        # 2. Ambiguous query (HAX G10 Clarify)
        if len(words) <= 4 or self._is_ambiguous_demonstrative(question, selected_text):
            return {
                "status": "success",
                "decision": "CLARIFY",
                "confidence": "CAO",
                "answer": f"Câu hỏi '{question}' của bạn hơi mơ hồ hoặc chưa có đoạn văn bản bôi đen đi kèm. Bạn đang muốn tìm hiểu cụ thể về phần nào?",
                "citations": [],
                "clarify_options": [
                    "Cách phân loại công việc theo Ma trận Tác động - Nỗ lực [T02-009]",
                    "Ý nghĩa và tầm quan trọng của Quick Win trong dự án AI [T02-010]",
                    "Cách đo lường và khảo sát Impact trong doanh nghiệp [T02-011]"
                ]
            }

        # 3. Grounded query matching
        if "quick win" in q_lower or "thắng nhanh" in q_lower:
            return {
                "status": "success",
                "decision": "GROUNDED",
                "confidence": "CAO",
                "answer": "Theo bài giảng [T02-010], Quick Win là những thành công nhỏ, dễ làm nhưng mang lại tác động nhìn thấy ngay. Trong dự án AI, việc ưu tiên tìm ra quick win rất quan trọng vì nó giúp tạo động lực cho đội ngũ và đặc biệt trong doanh nghiệp, những quick win sẽ củng cố niềm tin của lãnh đạo và các bên liên quan để tiếp tục đầu tư nguồn lực.",
                "citations": ["T02-010", "T02-009"],
                "clarify_options": []
            }
        elif "impact" in q_lower or "tác động" in q_lower or "doanh nghiệp" in q_lower:
            return {
                "status": "success",
                "decision": "GROUNDED",
                "confidence": "CAO",
                "answer": "Theo bài giảng [T02-011], khi đánh giá impact trong doanh nghiệp, bạn cần đi phỏng vấn các bên liên quan như trưởng bộ phận, CEO để khảo sát quy trình hiện tại, nếu giải quyết được bằng AI thì mang lại hiệu quả bao nhiêu và mất bao lâu để xây dựng.",
                "citations": ["T02-011"],
                "clarify_options": []
            }
        elif "tiktok" in q_lower:
            return {
                "status": "success",
                "decision": "GROUNDED",
                "confidence": "CAO",
                "answer": "Theo bài giảng [T02-003], quy trình làm nội dung TikTok được giảng viên lấy làm ví dụ điển hình cho ô Nỗ lực thấp nhưng Tác động cao (Quick win), nơi AI phát huy thế mạnh rất tốt.",
                "citations": ["T02-003"],
                "clarify_options": []
            }

        # If question has sufficient words but not matched specifically, answer grounded on general framework
        return {
            "status": "success",
            "decision": "GROUNDED",
            "confidence": "TRUNG_BÌNH",
            "answer": "Theo tài liệu bài giảng Day 2 [T02-009], ma trận tác động - nỗ lực là một framework đơn giản nhưng hiệu quả để học viên phân loại các đầu việc quan trọng và khoanh vùng ưu tiên triển khai trước.",
            "citations": ["T02-009"],
            "clarify_options": []
        }
