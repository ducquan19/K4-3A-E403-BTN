# BẢN REFLECTION CÁ NHÂN — ĐỖ QUANG VINH

- **Họ và tên:** Đỗ Quang Vinh
- **Mã học viên:** 2A202602989
- **Nhóm:** BTN (Lớp K4-3A · Phòng E403)
- **Vai trò:** Tech & Prototype Lead

---

### 1. Phần việc trực tiếp đảm nhiệm trong dự án
- Xây dựng kiến trúc fullstack hoàn chỉnh cho ứng dụng VLearn Grounded Tutor: Backend bằng **Python Flask REST API** (`backend/app.py`) và Frontend bằng **Vanilla HTML/CSS/JS** (`frontend/`).
- Triển khai giao diện **LMS Split-Screen**: Cột bên trái hiển thị bài giảng Day 2 có đánh mã `[T02-xxx]`, cột bên phải là khung tương tác chat AI.
- Hiện thực hóa tính năng tương tác hai chiều: khi click vào badge trích dẫn `[T02-xxx]` trong chat, giao diện bên trái tự động cuộn (smooth scroll) và phát hiệu ứng viền sáng (glow animation) nổi bật đoạn văn bản gốc.
- Xây dựng bảng **AI Inspector** hiển thị thời gian phản hồi thực tế (ms) và raw JSON để minh bạch 100% việc gọi AI thật trước ban giám khảo.

### 2. Công cụ AI đã hỗ trợ như thế nào trong quá trình làm việc
- Dùng AI để tối ưu hóa hiệu ứng DOM cuộn mượt và highlight bằng Vanilla CSS & JavaScript, đảm bảo không bị xung đột layout và không cần phụ thuộc vào các thư viện UI cồng kềnh.
- Dùng AI để sinh file `run.py` launcher tiện lợi: tự động cài dependency, kiểm tra cổng 5000 và tự động mở trình duyệt một cách mượt mà.

### 3. Một bài học sâu sắc từ case fail của chính nhóm
- **Case fail cụ thể:** Trong quá trình test ban đầu ở CP2, khi người dùng click liên tục vào nhiều trích dẫn khác nhau, giao diện bị giật và hiệu ứng highlight bị đè lên nhau gây mất tập trung.
- **Bài học rút ra:** Một sản phẩm AI xuất sắc không chỉ nằm ở mô hình phía sau mà còn phụ thuộc rất lớn vào **trải nghiệm người dùng (UX) tại điểm chạm**. Giao diện phải được thiết kế để hỗ trợ việc kiểm chứng nguồn một cách tự nhiên và nhẹ nhàng nhất (Explainability + Trust theo Google PAIR), nếu UI phức tạp hoặc giật lag thì người dùng sẽ bỏ qua việc kiểm chứng nguồn.
