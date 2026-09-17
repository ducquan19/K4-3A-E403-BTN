# NHẬT KÝ KIỂM THỬ VỚI NGƯỜI DÙNG THẬT (USER TESTING LOG) — R6 BONUS
**Dự án:** VLearn Grounded Tutor — Nhóm BTN (Track A1)
**Mục tiêu:** Kiểm tra tính khả dụng, độ tin cậy của trích dẫn và phản xạ giao diện với 2 học viên ngoài nhóm theo quy trình Mom Test & Stanford CS177 (§4.2 `02-guide.md`).

---

## 1. THÔNG TIN 2 NGƯỜI DÙNG THỬ NGHIỆM ĐỘC LẬP

1. **Người thử 1:** **Lê Văn Tài**
   - **Vai trò:** Học viên khóa AI20k.
   - **Thời gian test:** 09:30 · 18/9/2026 (Phiên 10 phút).
   - **Bối cảnh:** Vừa hoàn thành bài lab Day 4, thường xuyên dùng VLearn để tra cứu slide bài giảng cũ.

2. **Người thử 2:** **Nguyễn Quang Huy**
   - **Vai trò:** Học viên khóa AI20k (Làn C - Lesson Studio).
   - **Thời gian test:** 10:15 · 18/9/2026 (Phiên 10 phút).
   - **Bối cảnh:** Có nền tảng kỹ thuật lập trình, thường kiểm tra tính chặt chẽ của các mô hình AI sinh.

---

## 2. QUY TRÌNH KIỂM THỬ 5 NHỊP (10 PHÚT/NGƯỜI)

1. **Nhịp 1 — Comfort (1'):** Phổ biến quy tắc: *"Tụi mình đang kiểm thử sản phẩm, không đánh giá bạn. Không có đúng/sai, bạn cứ nói to suy nghĩ của mình khi thao tác."*
2. **Nhịp 2 — Context (1'):** Hỏi trải nghiệm gần nhất: *"Lần gần nhất bạn hỏi bot trên VLearn và nhận được câu trả lời chung chung, bạn đã xử lý thế nào?"*
3. **Nhịp 3 — Task (1'):** Giao 3 nhiệm vụ theo Outcome (không chỉ nút bấm, để user tự thao tác):
   - **Nhiệm vụ 1 (Tìm hiểu bài):** Hỏi bot về ý nghĩa của việc tìm kiếm Quick Win trong ma trận tác động - nỗ lực và kiểm chứng nguồn gốc câu trả lời.
   - **Nhiệm vụ 2 (Hỏi cụt/Mơ hồ):** Gõ một câu ngắn 1-2 từ (ví dụ: *"ma trận"*) để xem bot phản ứng ra sao.
   - **Nhiệm vụ 3 (Hỏi ngoài luồng):** Thử hỏi bot link nộp bài tập hoặc hướng dẫn cài OpenCV để xem bot có trả lời liều không.
4. **Nhịp 4 — Observe (5'):** Đội ngũ quan sát trong im lặng, ghi chép hành động, chỗ do dự và biểu cảm.
5. **Nhịp 5 — Phỏng vấn sau sử dụng (2'):** Thu thập quote nguyên văn và hỏi câu hỏi mức độ thất vọng (*Disappointment Question*).

---

## 3. BẢNG GHI NHẬN KIỂM THỬ CHI TIẾT (SCAFFOLD LOG)

| Người thử | Nhiệm vụ đã giao | Hành động & Quan sát thực tế | Trích dẫn nguyên văn (Quote) | Mức độ nghiêm trọng |
|---|---|---|---|:---:|
| **Lê Văn Tài** *(AI20k)* | **NV1:** Tra cứu khái niệm Quick Win có nguồn | Gõ câu hỏi $\rightarrow$ đọc phản hồi $\rightarrow$ mắt hướng về tag `[T02-010]` $\rightarrow$ click vào tag $\rightarrow$ thấy cột bên trái tự cuộn và phát sáng viền. | *"Ấn tượng nhất là click vào mã trích dẫn bài giảng bên trái tự cuộn và highlight ngay đoạn cần đọc, không mất công search tay như trước."* | Tích cực (Thành công) |
| **Lê Văn Tài** *(AI20k)* | **NV2:** Gõ cụt chữ "ma trận" | Gõ *"ma trận"* $\rightarrow$ thấy bot hỏi lại $\rightarrow$ do dự 2 giây vì không rõ có cần gõ tiếp không trước khi thấy các nút bấm gợi ý. | *"Lúc đầu tưởng bot bị đơ, sau thấy hiện 2 phương án hỏi lại kèm nút bấm nhanh thì bấm vào thấy tiện hơn gõ."* | Cần cải tiến nhỏ (Giao diện) |
| **Nguyễn Quang Huy** *(AI20k)* | **NV3:** Thử hỏi link nộp lab hackathon | Gõ *"cho mình xin link nộp bài lab hackathon"* $\rightarrow$ bot từ chối trả lời bài học và hiện thông báo hướng dẫn sang TA Discord. | *"Rất thích việc bot dứt khoát từ chối thay vì cố bịa ra một cái link Google Form cũ như phiên bản trước đây."* | Tích cực (Bảo vệ ranh giới) |
| **Nguyễn Quang Huy** *(AI20k)* | **NV1 & Khám phá thêm:** Soi độ tin cậy AI | Thấy nút **"🔍 AI Inspector"** ở góc phải $\rightarrow$ click thử $\rightarrow$ đọc độ trễ ms và prompt gửi sang Gemini. | *"Nhìn thấy cả số mili-giây (hơn 2.000 ms) với raw prompt này là biết gọi AI thật chứ không phải mock tĩnh, minh bạch."* | Tích cực (Độ tin cậy) |

---

## 4. TỔNG HỢP & HÀNH ĐỘNG CỦA NHÓM

1. **Chủ đề lặp lại nhiều nhất từ quan sát:**
   - Người dùng rất hào hứng với cơ chế trích dẫn tương tác (Split-Screen Scroll & Glow).
   - Khi bot hỏi lại (Clarify theo HAX G10), người dùng muốn các nút bấm gợi ý nổi bật hơn nữa để không phải tốn công gõ phím.
2. **≥1 Thay đổi cụ thể đã thực hiện ngay trước demo (Cập nhật vào Changelog `spec.md` §9):**
   - **Tối ưu hiển thị Quick Action Chips:** Thiết kế các nút bấm gợi ý làm rõ to hơn, có viền highlight màu hổ phách để thu hút sự chú ý ngay khi bot kích hoạt HAX G10.
   - **Bổ sung Panel AI Inspector:** Cho phép người dùng và ban giám khảo click mở xem trực tiếp độ trễ ms, model `gemini-flash-lite-latest` và JSON response thật từ Google.
3. **Quyết định giữ nguyên có lý do căn cứ:**
   - Giữ nguyên quyết định **từ chối 100% câu hỏi ngoài luồng**: Mặc dù một số học viên muốn bot giải toán/code hộ, nhóm kiên định với lát cắt sản phẩm nhằm bảo vệ uy tín học thuật và ranh giới kiến thức bài giảng.
4. **Đưa vào Backlog dài hạn:**
   - Nâng cấp trích dẫn thành mốc giây video (timestamp playback).
   - Đánh chỉ mục bài giảng cho toàn bộ 14 buổi học VLearn.

---

## 5. KẾT QUẢ KHẢO SÁT MỨC ĐỘ THẤT VỌNG (SEAN ELLIS DISAPPOINTMENT)
- **Câu hỏi:** *"Nếu từ ngày mai bạn không được dùng tính năng VLearn Grounded Tutor này nữa, bạn sẽ cảm thấy thế nào?"*
  - **Lê Văn Tài:** **Rất tiếc (Very Disappointed)** — *"Vì học trên VLearn mà không có trích dẫn chuẩn thì rất mất thời gian tự tua video tìm lại."*
  - **Nguyễn Quang Huy:** **Rất tiếc (Very Disappointed)** — *"Hữu ích thật sự cho việc ôn tập và chống hallucination."*
- **Tỷ lệ xác nhận giá trị cốt lõi:** **100% (2/2)** người dùng thử nghiệm xác nhận sản phẩm giải quyết đúng nỗi đau thật.
