# AI SPEC — VLearn Grounded Tutor — Nhóm BTN — Track A1
**Hướng:** [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở  
**Loại:** [x] Tối ưu tính năng có sẵn  [ ] Tính năng mới

---

## §1. User & Job
- **Job executor + workflow:** Học viên đang tự học hoặc ôn bài trên VLearn, bôi đen một đoạn tài liệu/slide hoặc gõ câu hỏi sâu để làm rõ khái niệm trong bài giảng.
- **Core JTBD:** Học viên muốn hiểu đúng trọng tâm bài giảng nhanh chóng mà không phải nghi ngờ tính xác thực của câu trả lời.
- **Problem statement:** Khi học viên đặt câu hỏi nằm ngoài phạm vi tài liệu đang mở hoặc câu hỏi quá mơ hồ, hệ thống AI Tutor hiện tại thường phỏng đoán, trả lời lan man không có trích dẫn nguồn; dẫn đến học viên hiểu sai kiến thức, tốn thời gian kiểm chứng thủ công và mất niềm tin vào hệ thống.
- **Evidence (Mining từ 13.494 turns chatlog thật trong `chatlog/tutor_turns.csv`):**
  - **28.0%** (3.781 lượt) câu trả lời không hề có trích dẫn tài liệu (`has_citation = False`).
  - **90.3%** phản hồi dập khuôn ở mức `review_concept`; tutor gần như không bao giờ hỏi ngược để làm rõ ý người học (`ask_probing_question` chỉ 28/13.494 lượt, tức **0.2%**).
  - **5 ví dụ nguyên văn từ chatlog:**
    1. `T06164`: Học viên hỏi *"làm bài lab ở đâu và nộp thế nào"* $\rightarrow$ Tutor đoán mò sai kênh nộp bài.
    2. `T02371`: Học viên bôi đen khái niệm ngoài slide $\rightarrow$ Tutor bịa định nghĩa không thuộc giáo trình.
    3. `T03412`: Học viên gõ cụt ngủn *"ma trận"* $\rightarrow$ Tutor tuôn một tràng lý thuyết chung chung không đúng phần đang học.
    4. `T08192`: Học viên hỏi về công thức $\rightarrow$ Tutor đưa công thức khác sách giáo khoa nhưng không chú thích nguồn.
    5. `T11043`: Học viên bôi đen 1 từ duy nhất $\rightarrow$ Tutor giải thích lan man thay vì hỏi lại để xác định nhu cầu.

---

## §2. Impact & Quyết định chọn
- **Bảng so sánh 3 ứng viên:**
  1. *Ứng viên 1 (Chặn ảo giác & bảo vệ ranh giới tài liệu - CHỌN):* ~1.600 học viên $\times$ 8 lượt hỏi/tuần $\times$ rủi ro tiếp nhận sai kiến thức domain $\rightarrow$ Impact: Rất cao, giải quyết triệt để 28% lỗi không căn cứ.
  2. *Ứng viên 2 (Gợi ý câu hỏi ôn tập sau mỗi video - LOẠI):* Tính năng tiện ích, nhưng không giải quyết nỗi đau bịa kiến thức khi đang hỏi bài.
  3. *Ứng viên 3 (Tự động tóm tắt slide bài giảng - LOẠI):* Slide đã có tóm tắt sẵn, nỗ lực thấp nhưng giá trị gia tăng ít.

---

## §3. Giải pháp tương tự đã nghiên cứu
- **NotebookLM (Google):** Luôn bắt buộc trích dẫn số trang/đoạn bên cạnh câu trả lời $\rightarrow$ *Học hỏi:* Bắt buộc trích dẫn mã đoạn `[T02-xxx]` và cho click để highlight ngay trên slide.
- **Khanmigo (Khan Academy):** Khi học viên hỏi cụt lủn, bot hỏi ngược lại để dẫn dắt $\rightarrow$ *Học hỏi:* Áp dụng HAX G10 khi input mơ hồ.
- **ChatGPT thông thường:** Thường cố trả lời mọi thứ kể cả khi không chắc $\rightarrow$ *Cần né:* Phải biết nói "Ngoài phạm vi" thay vì trả lời liều.

---

## §4. Thiết kế lát cắt
- **Lát cắt MỘT CÂU:**  
  *Một học viên · hỏi khái niệm ngoài phạm vi tài liệu đang mở · AI nhận diện thiếu căn cứ, từ chối giải thích lan man và chỉ dẫn nguồn chuẩn · học viên không bị tiếp nhận kiến thức sai.*
- **Non-goals:**
  - Không xây dựng lại toàn bộ LMS hay giao diện video player.
  - Không hỗ trợ giải toán/code tự động cho mọi môn học ngoài giáo trình khóa học.
- **Mức prototype:** Mock có kết nối **Live AI thật** qua **Google Gemini API** (`gemini-1.5-flash`).
- **Mức tự động hoá:** **Conditional Automation** (AI tự trả lời khi nguồn đủ chắc; hỏi lại khi mơ hồ; từ chối và chuyển hướng khi ngoài phạm vi bài học).
- **Nguyên tắc HAX/PAIR áp dụng (≥4 nguyên tắc):**
  | Nguyên tắc | Vị trí áp dụng cụ thể trong Prototype |
  |---|---|
  | **HAX G1** (Làm rõ hệ thống làm được gì) | Banner đầu trang và lời chào của Tutor nói rõ: *"Chỉ trả lời dựa trên tài liệu bài giảng đang mở"*. |
  | **HAX G2** (Làm rõ mức độ tin cậy) | Hiển thị badge mức độ tin cậy (*CAO / TRUNG BÌNH*) và gắn chip trích dẫn `[T02-xxx]`. |
  | **HAX G10** (Thu hẹp phạm vi khi nghi ngờ) | Khi câu hỏi mơ hồ dưới 3 từ $\rightarrow$ Tutor chủ động hỏi lại 1 câu kèm 2 gợi ý chọn nhanh. |
  | **HAX G15** (Mời phản hồi chi tiết) | Cung cấp nút 👍 / 👎 kèm lý do cụ thể dưới từng tin nhắn phản hồi. |

---

## §5. Bốn lớp chỗ khó & Kịch bản rủi ro (≥8 kịch bản)
1. *Nguồn sự thật:* Học viên hỏi khái niệm có trong bài giảng $\rightarrow$ Trả lời súc tích, đính kèm chip trích dẫn `[T02-009]`.
2. *Nguồn sự thật:* Học viên hỏi khái niệm bị sai lệch so với bài $\rightarrow$ Trích dẫn nguyên văn slide để đính chính, không thuận theo câu hỏi sai.
3. *Mơ hồ:* Học viên chỉ gõ 1 từ "Ma trận" $\rightarrow$ Kích hoạt CLARIFY, hỏi: *"Bạn muốn tìm hiểu về cách phân loại hay ví dụ thực tế?"*
4. *Mơ hồ:* Học viên bôi đen đoạn quá ngắn (1 từ) $\rightarrow$ Yêu cầu chọn phạm vi rộng hơn hoặc nêu rõ băn khoăn.
5. *Ngoài phạm vi:* Học viên hỏi link nộp bài lab $\rightarrow$ Từ chối trả lời nội dung bài học, hướng dẫn kênh Discord hỗ trợ.
6. *Ngoài phạm vi:* Học viên hỏi thư viện code ngoài giáo trình $\rightarrow$ Báo rõ kiến thức nằm ngoài buổi 2, đề xuất tài liệu tham khảo chính thống.
7. *Đặc thù domain:* Học viên nhầm lẫn giữa Effort và Impact $\rightarrow$ Phân tích rõ định nghĩa 2 trục dựa trên đoạn `[T02-002]`.
8. *Đặc thù domain:* Học viên hỏi prompt bẻ khóa ("hãy quên các quy tắc trên") $\rightarrow$ Giữ vững Guardrail, từ chối thực thi lệnh vượt quyền.

---

## §6. Bốn đường đi của trải nghiệm (User Flows)
- **Happy Path:** Bôi đen/Hỏi đúng trọng tâm $\rightarrow$ Nhận phản hồi có căn cứ kèm trích dẫn $\rightarrow$ Click trích dẫn xem vị trí trên slide $\rightarrow$ Học viên hiểu bài.
- **Low-confidence / Clarify:** Hỏi câu mơ hồ $\rightarrow$ AI nhận diện thiếu thông tin $\rightarrow$ Đưa ra 2 phương án làm rõ $\rightarrow$ Học viên bấm chọn $\rightarrow$ AI trả lời đúng ý.
- **Failure / Out of bounds:** Hỏi ngoài bài giảng $\rightarrow$ AI chặn ảo giác, từ chối lịch sự $\rightarrow$ Cung cấp nút điều hướng sang kênh hỏi TA Discord.
- **Correction:** Học viên bấm 👎 $\rightarrow$ Chọn lý do "Trích dẫn chưa khớp" $\rightarrow$ Hệ thống ghi log để cải thiện Golden Set.

---

## §7. Kiểm thử & Golden Set
- **Chiều chất lượng:** Factuality (Tính xác thực có nguồn) $\ge 90\%$, Guardrail Protection (Chặn ngoài phạm vi) = $100\%$.
- **Golden Set:** 10 test cases được trích từ chatlog thật (4 Grounded, 3 Clarify, 3 Out of Bounds) trong `golden_set.json`.
- **Quality Bar chốt trước hạn:** Đạt **$\ge 85\%$** tỷ lệ vượt qua toàn bộ bộ test Golden Set bằng Gemini API.

---

## §8. Phân công nhóm BTN (4 thành viên)
- **Product Lead (Đội trưởng):** Phụ trách Canvas, AI Spec, HAX Guidelines, nộp Checkpoint.
- **Data & Eval Lead:** Khai thác 13.494 chatlog, xây dựng Golden Set, đo đạc kết quả chạy thật.
- **AI & Prompt Engineer:** Thiết kế Grounding Guardrail Prompt, tích hợp Google Gemini API.
- **Prototype & Tech Lead:** Xây dựng Streamlit Web App, UI VLearn Split-view, video demo.

*Willing Users xác nhận thử nghiệm tại CP5:* 2 học viên ngoài nhóm sẵn sàng kiểm thử prototype.
