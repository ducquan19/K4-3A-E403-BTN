# Mini Hackathon AI — Batch 04 · Lớp 3A

**SPEC → Prototype → Demo.** Đây không phải cuộc thi code — đây là cuộc thi **tư duy sản phẩm AI**.

---

## 👥 1. THÀNH VIÊN NHÓM & PHÂN CÔNG VAI TRÒ

**Lớp:** 3A · **Phòng:** E403 · **Cụm:** ____ · **Track:** A1 · VLearn Grounded Tutor
**Tên nhóm:** **BTN** · **Đề tài:** Chặn ảo giác, trả lời có căn cứ trích dẫn và bảo vệ ranh giới bài giảng

| Họ và Tên | Mã Học Viên | Vai trò chính | Phần việc đảm nhiệm cụ thể trong dự án |
|---|---|---|---|
| **Chu Phúc Anh** | *2A202602370* | **Product Lead (Đội trưởng)** | Phụ trách Canvas CP1, AI Spec, áp dụng nguyên tắc HAX/PAIR, điều phối nhóm và nộp bài các Checkpoint |
| **Trần Đức Quân** | *2A202602922* | **Data & Eval Lead** | Khai thác 13.494 chatlog thật, chọn bằng chứng, xây dựng bộ test Golden Set 20 cases (4 lớp) và đo đạc kết quả CP3 |
| **Bùi Minh Quân** | *2A202602958* | **AI & Prompt Engineer** | Thiết kế Grounding Guardrail Prompt, phân tầng 4 lớp chỗ khó, tích hợp kết nối Google Gemini API |
| **Đỗ Quang Vinh** | *2A202602989* | **Tech & Prototype Lead** | Xây dựng Full-Stack App (Backend Flask + Frontend Web LMS Split-Screen), tích hợp AI Inspector và quay Video Demo |

> **Willing users (Khách thử nghiệm CP5):** Đã kết nối với 2 học viên ngoài nhóm sẵn sàng tham gia kiểm thử prototype tại vòng validation.

---

## 🌟 2. TỔNG QUAN ĐỀ TÀI & LÁT CẮT GIẢI PHÁP (TRACK A1)

### Nỗi đau & Bằng chứng thực tế (Mining từ 13.494 turns chatlog trong `tutor_turns.csv`):
- **28.0%** (3.781 lượt) câu trả lời của AI Tutor trước đây không hề có trích dẫn tài liệu (`has_citation = False`).
- **90.3%** phản hồi dập khuôn ở mức `review_concept`; chỉ **0.2%** (28 lượt) biết hỏi ngược khi học viên hỏi mơ hồ.
- Khi câu hỏi ngoài phạm vi tài liệu hoặc quá mơ hồ, tutor thường đoán mò, giải thích lan man, khiến học viên tiếp nhận sai kiến thức và mất niềm tin.

### Lát cắt sản phẩm (Đúng chuẩn 1 câu):
> **Một học viên · hỏi khái niệm ngoài phạm vi tài liệu đang mở · AI nhận diện thiếu căn cứ, từ chối giải thích lan man và chỉ dẫn nguồn chuẩn · học viên không bị tiếp nhận kiến thức sai.**

### Mức tự động hoá (Theo Cost-of-error):
- **Conditional Automation:** Tự trả lời khi có căn cứ chắc chắn trong bài; hỏi lại khi mơ hồ (HAX G10); từ chối lịch sự và hướng dẫn kênh hỗ trợ khi câu hỏi vượt ngoài ranh giới bài giảng.

---

## 🚀 3. ĐIỂM NỔI BẬT & CHỨNG MINH HOẠT ĐỘNG THẬT (KHÔNG PHẢI MOCKUP)

1. **Kết nối Google Gemini API thật (`gemini-1.5-flash` / `gemini-2.0-flash`):**
   - Tích hợp trực tiếp qua SDK `google-genai` và REST API của Google, xử lý phân loại ngữ nghĩa thời gian thực.
2. **AI Call Inspector (Minh bạch 100% lượt gọi AI):**
   - Nút **"🔍 AI Inspector"** trên giao diện hiển thị: **Thời gian phản hồi thực tế (ms)**, **Model sử dụng**, **Prompt gửi đi** và **JSON thô trả về từ Google Gemini**.
3. **Trình xem bài giảng tương tác hai chiều (Split-Screen LMS):**
   - Click vào tag trích dẫn `📌 [T02-010]` trong khung chat, bài giảng bên trái tự động cuộn đến và phát sáng viền nổi bật (glow animation).
4. **Nút thử nhanh 1-Click cho 3 kịch bản chính:**
   - 🟢 **1. Trong bài (Grounded):** Trả lời có trích dẫn nguồn `[T02-xxx]`.
   - 🟡 **2. Mơ hồ (Clarify - HAX G10):** Hỏi lại 1 câu kèm các lựa chọn bấm nhanh.
   - 🔴 **3. Ngoài bài (Out of Bounds):** Từ chối giải thích bài học, hướng dẫn sang kênh Discord của TA.
5. **Bộ đo đạc thực nghiệm tự động (`scripts/eval_gemini.py`):**
   - Chạy kiểm thử 20 ca từ chatlog thật (4 lớp) qua Gemini API và xuất báo cáo đo đạc số liệu cho Checkpoint 3.

---

## 🛠️ 4. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY (TURNKEY RUN)

### Bước 1: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 2: Khởi chạy sản phẩm (1 lệnh duy nhất)
```bash
python run.py
```
> Hệ thống sẽ khởi động máy chủ Backend tại cổng `5000` và **tự động mở trình duyệt web** tại:
> 🔗 `http://localhost:5000`

### Bước 3: Cấu hình Gemini API Key
- Bấm nút **"⚙️ Cấu hình API"** ở góc trên bên phải màn hình và dán API Key của bạn (lấy miễn phí tại [aistudio.google.com](https://aistudio.google.com/app/apikey)).
- Bấm **"⚡ Thử kết nối API"** để kiểm tra độ trễ mạng thực tế.
- *(Hoặc tạo file `.env` với nội dung `GEMINI_API_KEY=AIzaSy...` để hệ thống tự nhận diện).*

---

## 🧪 5. CÔNG CỤ ĐO ĐẠC VÀ KIỂM THỬ TRONG THƯ MỤC `scripts/`

### 1. Kiểm tra nhanh API qua dòng lệnh (3 giây):
```bash
python scripts/test_api.py
```
*(Hoặc truyền key trực tiếp: `python scripts/test_api.py --key YOUR_KEY`)*

### 2. Chạy bộ đánh giá Golden Set phục vụ Checkpoint 3 & Checkpoint 4:
```bash
python scripts/eval_gemini.py
```
Hệ thống sẽ chạy qua 20 ca kiểm thử thực tế (4 lớp chỗ khó) từ chatlog và tự động sinh 2 file báo cáo bên trong thư mục `scripts/`:
- `scripts/eval_results.json`: Chi tiết từng lượt gọi AI, thời gian phản hồi, trích dẫn.
- `scripts/eval_report.md`: Bảng tổng kết số đo và tỷ lệ đạt chuẩn (Pass Rate %).

---

## 📁 6. CẤU TRÚC THƯ MỤC REPO

```
K4-3A-E403-BTN/
├── README.md              ← Bảng thành viên + Phân công vai trò + Hướng dẫn
├── spec.md                ← AI Spec 9 phần hoàn chỉnh (Đã khóa Quality Bar ≥ 85%)
├── canvas-cp1.jpg & .md   ← Canvas 4 ô Checkpoint 1
├── demo-slides.pdf        ← File slide thuyết trình 6 trang (xuất PDF cho CP5/CP6)
├── run.py                 ← Launcher khởi động Fullstack 1 lệnh duy nhất (R5)
├── requirements.txt       ← Danh mục thư viện phụ thuộc
├── .env.example           ← Mẫu biến môi trường
│
├── eval/                  ← DỮ LIỆU ĐO ĐẠC & ĐÁNH GIÁ (R4 - 15 điểm)
│   ├── golden_set.json    ← Bộ 20 ca kiểm thử 4 lớp trích từ chatlog thật
│   ├── eval_gemini.py     ← Script chạy đo đạc tự động qua Gemini API
│   ├── eval_results.json  ← Dữ liệu thô kết quả đo đạc thời gian thực
│   └── eval_report.md     ← Bảng tổng kết số đo và tỷ lệ đạt chuẩn (85%)
│
├── validation/            ← NHẬT KÝ KIỂM THỬ VỚI NGƯỜI DÙNG THẬT (R6 BONUS - 8 điểm)
│   └── user_testing_log.md← Biên bản test 5 nhịp của 2 Willing Users ngoài nhóm
│
├── reflection/            ← BẢN REFLECTION CÁ NHÂN (Vibe-coding rule)
│   ├── chu_phuc_anh.md    ← Product Lead
│   ├── tran_duc_quan.md   ← Data & Eval Lead
│   ├── bui_minh_quan.md   ← AI & Prompt Engineer
│   └── do_quang_vinh.md   ← Tech & Prototype Lead
│
├── backend/               ← BACKEND (Python Flask REST API)
│   ├── app.py             ← Máy chủ API phục vụ /api/chat, /api/lecture
│   ├── core/
│   │   ├── __init__.py
│   │   └── tutor_engine.py← Lõi Guardrail Grounding & Gọi Google Gemini API
│   └── data/
│       └── lecture_day02.md← Dữ liệu bài giảng Day 2 có mã đoạn [T02-xxx]
│
└── frontend/              ← FRONTEND (Giao diện Web LMS Split-Screen)
    ├── index.html         ← Khung giao diện Split-Screen 2 cột
    ├── style.css          ← Dark Navy Theme, hiệu ứng highlight trích dẫn
    └── app.js             ← Xử lý tương tác, 3 nút demo 1-click, AI Inspector
```

---

## 📅 7. LỊCH CHECKPOINT & QUY ĐỊNH HACKATHON

| Mốc | Cần hoàn thành | Hạn (ca 3A) | Trạng thái nhóm BTN |
|---|---|---|---|
| **CP1** | Canvas 4 ô + đội trưởng + link repo GitHub | 19:30 · 16/9 | **ĐÃ HOÀN THÀNH** |
| **CP2** | Cho thấy luồng hoạt động (mock bấm được / video) | 21:00 · 16/9 | **ĐÃ HOÀN THÀNH** |
| **CP3** | Video thao tác 30s + số đo (thử bao nhiêu, đúng bao nhiêu) | 16:00 · 17/9 | **ĐÃ SẴN SÀNG** (`scripts/eval_gemini.py`) |
| **CP4** | Chốt `spec.md` — khoá chuẩn "đạt" · tự khai phần chưa xong | 21:00 · 17/9 | **ĐÃ HOÀN THÀNH** (`spec.md`) |
| **CP5** | Slide PDF + video demo dự phòng cho buổi pitch | 13:00 · 18/9 | Đang chuẩn bị |
| **CP6** | Thuyết trình vòng thi tại phòng E403 | 17:30 · 18/9 | Sẵn sàng |

---

## ⚖️ 8. BẢO MẬT DỮ LIỆU ĐƯỢC CUNG CẤP
- Toàn bộ dữ liệu chatlog và transcript được cung cấp trong hackathon thuộc quy định bảo mật của khóa học.
- Nhóm cam kết: Chỉ sử dụng dữ liệu trong phạm vi bài thi; không chia sẻ ra ngoài khóa học; không commit dữ liệu thô chưa ẩn danh; tôn trọng quyền riêng tư của học viên và giảng viên.
