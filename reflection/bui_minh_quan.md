# BẢN REFLECTION CÁ NHÂN — BÙI MINH QUÂN

- **Họ và tên:** Bùi Minh Quân
- **Mã học viên:** 2A202602958
- **Nhóm:** BTN (Lớp K4-3A · Phòng E403)
- **Vai trò:** AI & Prompt Engineer

---

### 1. Phần việc trực tiếp đảm nhiệm trong dự án
- Thiết kế kiến trúc **Grounding Guardrail System Prompt** trong `backend/core/tutor_engine.py`, phân tách rõ ràng 3 quyết định đầu ra: `GROUNDED`, `CLARIFY`, `OUT_OF_BOUNDS`.
- Bắt buộc ràng buộc trích dẫn trọng tâm: chỉ cho phép AI dẫn mã đoạn `[T02-xxx]` thực sự chứa câu trả lời trực tiếp trong `lecture_day02.md`, triệt tiêu hoàn toàn tình trạng trích dẫn dàn trải.
- Tích hợp kết nối trực tiếp với Google Gemini API (`gemini-flash-lite-latest`), loại bỏ 100% các đoạn code mock để phục vụ demo AI thật.

### 2. Công cụ AI đã hỗ trợ như thế nào trong quá trình làm việc
- Dùng AI để thử nghiệm các biến thể prompt (Few-shot learning) nhằm tối ưu khả năng nhận diện ý định của người học khi câu hỏi bị thiếu chủ ngữ hoặc quá ngắn.
- Dùng AI để debug các phản hồi JSON thô từ Gemini API, đảm bảo output luôn tuân thủ schema nghiêm ngặt để frontend phân tích được mã trích dẫn.

### 3. Một bài học sâu sắc từ case fail của chính nhóm
- **Case fail cụ thể:** `CASE-19` — khi học viên đặt câu hỏi bẫy ngược logic (*"Có phải nỗ lực càng cao thì càng dễ tạo thành Quick Win không?"*), mô hình ban đầu do prompt cài đặt quá thận trọng nên đã chuyển sang hỏi lại (Clarify) thay vì đính chính dựa trên bài học.
- **Bài học rút ra:** System Prompt không chỉ cần phòng thủ (Guardrail) mà còn phải đủ tinh tế để phân biệt giữa "người dùng hỏi mơ hồ do thiếu thông tin" và "người dùng đang hiểu sai kiến thức cần được uốn nắn". Việc cân bằng giữa tính thận trọng và tính chủ động đính chính là bài toán hóc búa nhất trong kỹ nghệ Prompt.
