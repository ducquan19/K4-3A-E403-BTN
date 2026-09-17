# BẢN REFLECTION CÁ NHÂN — CHU PHÚC ANH

- **Họ và tên:** Chu Phúc Anh
- **Mã học viên:** 2A202602370
- **Nhóm:** BTN (Lớp K4-3A · Phòng E403)
- **Vai trò:** Product Lead (Đội trưởng)

---

### 1. Phần việc trực tiếp đảm nhiệm trong dự án
- Trực tiếp xây dựng khung Canvas Checkpoint 1 (xác định Job Executor, Pain Point cốt lõi và định hình lát cắt 1 câu).
- Soạn thảo và hoàn thiện tài liệu **AI Spec (`spec.md`)** qua 9 phần chuẩn theo `03-ai-spec-template.md`.
- Nghiên cứu và lựa chọn áp dụng 4 nguyên tắc **HAX/PAIR** (G1, G2, G10, G15) vào đúng các vị trí tương tác trên giao diện prototype.
- Điều phối tiến độ cả nhóm qua 6 Checkpoint, đảm bảo chốt và khóa Quality Bar ($\ge 85\%$) đúng hạn 21:00 ngày 17/9.

### 2. Công cụ AI đã hỗ trợ như thế nào trong quá trình làm việc
- Sử dụng LLM để đối chiếu nhanh các kịch bản lỗi trong HAX Playbook nhằm xây dựng bảng 8 kịch bản rủi ro (KB-01 đến KB-08) bao phủ đủ 4 lớp chỗ khó.
- Tận dụng AI để rà soát format spec và kiểm tra tính logic giữa các con số trong bảng Impact (1.600 học viên $\times$ tần suất $\times$ cost of error).

### 3. Một bài học sâu sắc từ case fail của chính nhóm
- **Case fail cụ thể:** `CASE-12` trong Golden Set — khi người dùng gõ cụt ngủn *"phỏng vấn ai"*, ban đầu mô hình AI tự đoán mò ngữ cảnh phỏng vấn người dùng để trả lời thay vì dừng lại hỏi làm rõ theo HAX G10.
- **Bài học rút ra:** Khi thiết kế sản phẩm AI sinh, việc **đặt kỳ vọng thấp hơn khả năng (Mental Models)** và **dám từ chối hoặc hỏi lại khi thiếu thông tin** quan trọng hơn nhiều so với việc cố gắng trả lời bằng mọi giá. Một câu trả lời phỏng đoán sai sẽ hủy hoại hoàn toàn niềm tin của người học đối với nền tảng VLearn.
