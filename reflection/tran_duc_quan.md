# BẢN REFLECTION CÁ NHÂN — TRẦN ĐỨC QUÂN

- **Họ và tên:** Trần Đức Quân
- **Mã học viên:** 2A202602922
- **Nhóm:** BTN (Lớp K4-3A · Phòng E403)
- **Vai trò:** Data & Eval Lead

---

### 1. Phần việc trực tiếp đảm nhiệm trong dự án
- Khai thác và xử lý dữ liệu từ file chatlog thật **13.494 turns** (`data/vlearn-pack/chatlog/tutor_turns.csv`), phát hiện con số bằng chứng đắt giá: **28.0% (3.781 turns) thiếu trích dẫn** và **90.3% phản hồi một chiều** thiếu hỏi ngược.
- Xây dựng bộ kiểm thử **Golden Set 20 test cases** (`golden_set.json`) phân bổ đều trên 4 lớp chỗ khó (8 Grounded, 5 Clarify, 5 Out of Bounds, 2 Bẫy logic domain).
- Viết và thực thi script đánh giá tự động `eval_gemini.py`, ghi nhận số đo thực nghiệm khách quan (Pass rate **85.0%**, độ trễ trung bình **2.749 ms**).

### 2. Công cụ AI đã hỗ trợ như thế nào trong quá trình làm việc
- Dùng Python kết hợp AI để phân loại tự động các mẫu câu hỏi trong chatlog theo độ dài và mức độ mơ hồ, giúp lọc ra 5 ví dụ nguyên văn chân thực nhất (`CHATLOG_T06164`, `CHATLOG_T02371`,...).
- Dùng Gemini API làm giám khảo chấm tự động (LLM-as-a-judge) với rubric chặt chẽ: kiểm tra định dạng trích dẫn `[T02-xxx]` và từ khóa bắt buộc theo từng case.

### 3. Một bài học sâu sắc từ case fail của chính nhóm
- **Case fail cụ thể:** `CASE-18` — khi học viên hỏi về tính năng Studio của Track C, mô hình nhầm lẫn xếp vào nhóm "Clarify" thay vì "Out-of-bounds" (từ chối do ngoài phạm vi).
- **Bài học rút ra:** Đừng bao giờ đánh giá mô hình bằng "vibe check" (cảm nhận trực quan). Phải có một bộ Golden Set phong phú có cả case bẫy biên giới kiến thức và chạy đo đạc bằng script có số liệu lặp lại được. Nếu không chạy trọn bộ 20 case, nhóm sẽ không bao giờ phát hiện ra lỗ hổng phân loại ranh giới này.
