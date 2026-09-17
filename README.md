# Mini Hackathon AI â€” Batch 04 Â· Lá»›p 3A

**SPEC â†’ Prototype â†’ Demo.** ÄÃ¢y khÃ´ng pháº£i cuá»™c thi code â€” Ä‘Ã¢y lÃ  cuá»™c thi **tÆ° duy sáº£n pháº©m AI**.

---

## ðŸ‘¥ 1. THÃ€NH VIÃŠN NHÃ“M & PHÃ‚N CÃ”NG VAI TRÃ’

**Lá»›p:** 3A Â· **PhÃ²ng:** E403 Â· **Cá»¥m:** ____ Â· **Track:** A1 Â· VLearn Grounded Tutor  
**TÃªn nhÃ³m:** **BTN** Â· **Äá» tÃ i:** Cháº·n áº£o giÃ¡c, tráº£ lá»i cÃ³ cÄƒn cá»© trÃ­ch dáº«n vÃ  báº£o vá»‡ ranh giá»›i bÃ i giáº£ng

| Há» vÃ  TÃªn | MÃ£ Há»c ViÃªn | Vai trÃ² chÃ­nh | Pháº§n viá»‡c Ä‘áº£m nhiá»‡m cá»¥ thá»ƒ trong dá»± Ã¡n |
|---|---|---|---|
| **Chu PhÃºc Anh** | *2A202602370* | **Product Lead (Äá»™i trÆ°á»Ÿng)** | Phá»¥ trÃ¡ch Canvas CP1, AI Spec, Ã¡p dá»¥ng nguyÃªn táº¯c HAX/PAIR, Ä‘iá»u phá»‘i nhÃ³m vÃ  ná»™p bÃ i cÃ¡c Checkpoint |
| **Tráº§n Äá»©c QuÃ¢n** | *2A202602922* | **Data & Eval Lead** | Khai thÃ¡c 13.494 chatlog tháº­t, chá»n báº±ng chá»©ng, xÃ¢y dá»±ng bá»™ test Golden Set 20 cases (4 lá»›p) vÃ  Ä‘o Ä‘áº¡c káº¿t quáº£ CP3 |
| **BÃ¹i Minh QuÃ¢n** | *2A202602958* | **AI & Prompt Engineer** | Thiáº¿t káº¿ Grounding Guardrail Prompt, phÃ¢n táº§ng 4 lá»›p chá»— khÃ³, tÃ­ch há»£p káº¿t ná»‘i Google Gemini API |
| **Äá»— Quang Vinh** | *2A202602989* | **Tech & Prototype Lead** | XÃ¢y dá»±ng Full-Stack App (Backend Flask + Frontend Web LMS Split-Screen), tÃ­ch há»£p AI Inspector vÃ  quay Video Demo |

> **Willing users (KhÃ¡ch thá»­ nghiá»‡m CP5):** ÄÃ£ káº¿t ná»‘i vá»›i 2 há»c viÃªn ngoÃ i nhÃ³m sáºµn sÃ ng tham gia kiá»ƒm thá»­ prototype táº¡i vÃ²ng validation.

---

## ðŸŒŸ 2. Tá»”NG QUAN Äá»€ TÃ€I & LÃT Cáº®T GIáº¢I PHÃP (TRACK A1)

### Ná»—i Ä‘au & Báº±ng chá»©ng thá»±c táº¿ (Mining tá»« 13.494 turns chatlog trong `tutor_turns.csv`):
- **28.0%** (3.781 lÆ°á»£t) cÃ¢u tráº£ lá»i cá»§a AI Tutor trÆ°á»›c Ä‘Ã¢y khÃ´ng há» cÃ³ trÃ­ch dáº«n tÃ i liá»‡u (`has_citation = False`).
- **90.3%** pháº£n há»“i dáº­p khuÃ´n á»Ÿ má»©c `review_concept`; chá»‰ **0.2%** (28 lÆ°á»£t) biáº¿t há»i ngÆ°á»£c khi há»c viÃªn há»i mÆ¡ há»“.
- Khi cÃ¢u há»i ngoÃ i pháº¡m vi tÃ i liá»‡u hoáº·c quÃ¡ mÆ¡ há»“, tutor thÆ°á»ng Ä‘oÃ¡n mÃ², giáº£i thÃ­ch lan man, khiáº¿n há»c viÃªn tiáº¿p nháº­n sai kiáº¿n thá»©c vÃ  máº¥t niá»m tin.

### LÃ¡t cáº¯t sáº£n pháº©m (ÄÃºng chuáº©n 1 cÃ¢u):
> **Má»™t há»c viÃªn Â· há»i khÃ¡i niá»‡m ngoÃ i pháº¡m vi tÃ i liá»‡u Ä‘ang má»Ÿ Â· AI nháº­n diá»‡n thiáº¿u cÄƒn cá»©, tá»« chá»‘i giáº£i thÃ­ch lan man vÃ  chá»‰ dáº«n nguá»“n chuáº©n Â· há»c viÃªn khÃ´ng bá»‹ tiáº¿p nháº­n kiáº¿n thá»©c sai.**

### Má»©c tá»± Ä‘á»™ng hoÃ¡ (Theo Cost-of-error):
- **Conditional Automation:** Tá»± tráº£ lá»i khi cÃ³ cÄƒn cá»© cháº¯c cháº¯n trong bÃ i; há»i láº¡i khi mÆ¡ há»“ (HAX G10); tá»« chá»‘i lá»‹ch sá»± vÃ  hÆ°á»›ng dáº«n kÃªnh há»— trá»£ khi cÃ¢u há»i vÆ°á»£t ngoÃ i ranh giá»›i bÃ i giáº£ng.

---

## ðŸš€ 3. ÄIá»‚M Ná»”I Báº¬T & CHá»¨NG MINH HOáº T Äá»˜NG THáº¬T (KHÃ”NG PHáº¢I MOCKUP)

1. **Káº¿t ná»‘i Google Gemini API tháº­t (`gemini-1.5-flash` / `gemini-2.0-flash`):**
   - TÃ­ch há»£p trá»±c tiáº¿p qua SDK `google-genai` vÃ  REST API cá»§a Google, xá»­ lÃ½ phÃ¢n loáº¡i ngá»¯ nghÄ©a thá»i gian thá»±c.
2. **AI Call Inspector (Minh báº¡ch 100% lÆ°á»£t gá»i AI):**
   - NÃºt **"ðŸ” AI Inspector"** trÃªn giao diá»‡n hiá»ƒn thá»‹: **Thá»i gian pháº£n há»“i thá»±c táº¿ (ms)**, **Model sá»­ dá»¥ng**, **Prompt gá»­i Ä‘i** vÃ  **JSON thÃ´ tráº£ vá» tá»« Google Gemini**.
3. **TrÃ¬nh xem bÃ i giáº£ng tÆ°Æ¡ng tÃ¡c hai chiá»u (Split-Screen LMS):**
   - Click vÃ o tag trÃ­ch dáº«n `ðŸ“Œ [T02-010]` trong khung chat, bÃ i giáº£ng bÃªn trÃ¡i tá»± Ä‘á»™ng cuá»™n Ä‘áº¿n vÃ  phÃ¡t sÃ¡ng viá»n ná»•i báº­t (glow animation).
4. **NÃºt thá»­ nhanh 1-Click cho 3 ká»‹ch báº£n chÃ­nh:**
   - ðŸŸ¢ **1. Trong bÃ i (Grounded):** Tráº£ lá»i cÃ³ trÃ­ch dáº«n nguá»“n `[T02-xxx]`.
   - ðŸŸ¡ **2. MÆ¡ há»“ (Clarify - HAX G10):** Há»i láº¡i 1 cÃ¢u kÃ¨m cÃ¡c lá»±a chá»n báº¥m nhanh.
   - ðŸ”´ **3. NgoÃ i bÃ i (Out of Bounds):** Tá»« chá»‘i giáº£i thÃ­ch bÃ i há»c, hÆ°á»›ng dáº«n sang kÃªnh Discord cá»§a TA.
5. **Bá»™ Ä‘o Ä‘áº¡c thá»±c nghiá»‡m tá»± Ä‘á»™ng (`scripts/eval_gemini.py`):**
   - Cháº¡y kiá»ƒm thá»­ 20 ca tá»« chatlog tháº­t (4 lá»›p) qua Gemini API vÃ  xuáº¥t bÃ¡o cÃ¡o Ä‘o Ä‘áº¡c sá»‘ liá»‡u cho Checkpoint 3.

---

## ðŸ› ï¸ 4. HÆ¯á»šNG DáºªN CÃ€I Äáº¶T & KHá»žI CHáº Y (TURNKEY RUN)

### BÆ°á»›c 1: CÃ i Ä‘áº·t thÆ° viá»‡n
```bash
pip install -r requirements.txt
```

### BÆ°á»›c 2: Khá»Ÿi cháº¡y sáº£n pháº©m (1 lá»‡nh duy nháº¥t)
```bash
python run.py
```
> Há»‡ thá»‘ng sáº½ khá»Ÿi Ä‘á»™ng mÃ¡y chá»§ Backend táº¡i cá»•ng `5000` vÃ  **tá»± Ä‘á»™ng má»Ÿ trÃ¬nh duyá»‡t web** táº¡i:  
> ðŸ”— `http://localhost:5000`

### BÆ°á»›c 3: Cáº¥u hÃ¬nh Gemini API Key
- Báº¥m nÃºt **"âš™ï¸ Cáº¥u hÃ¬nh API"** á»Ÿ gÃ³c trÃªn bÃªn pháº£i mÃ n hÃ¬nh vÃ  dÃ¡n API Key cá»§a báº¡n (láº¥y miá»…n phÃ­ táº¡i [aistudio.google.com](https://aistudio.google.com/app/apikey)).
- Báº¥m **"âš¡ Thá»­ káº¿t ná»‘i API"** Ä‘á»ƒ kiá»ƒm tra Ä‘á»™ trá»… máº¡ng thá»±c táº¿.
- *(Hoáº·c táº¡o file `.env` vá»›i ná»™i dung `GEMINI_API_KEY=AIzaSy...` Ä‘á»ƒ há»‡ thá»‘ng tá»± nháº­n diá»‡n).*

---

## ðŸ§ª 5. CÃ”NG Cá»¤ ÄO Äáº C VÃ€ KIá»‚M THá»¬ TRONG THÆ¯ Má»¤C `scripts/`

### 1. Kiá»ƒm tra nhanh API qua dÃ²ng lá»‡nh (3 giÃ¢y):
```bash
python scripts/test_api.py
```
*(Hoáº·c truyá»n key trá»±c tiáº¿p: `python scripts/test_api.py --key YOUR_KEY`)*

### 2. Cháº¡y bá»™ Ä‘Ã¡nh giÃ¡ Golden Set phá»¥c vá»¥ Checkpoint 3 & Checkpoint 4:
```bash
python scripts/eval_gemini.py
```
Há»‡ thá»‘ng sáº½ cháº¡y qua 20 ca kiá»ƒm thá»­ thá»±c táº¿ (4 lá»›p chá»— khÃ³) tá»« chatlog vÃ  tá»± Ä‘á»™ng sinh 2 file bÃ¡o cÃ¡o bÃªn trong thÆ° má»¥c `scripts/`:
- `scripts/eval_results.json`: Chi tiáº¿t tá»«ng lÆ°á»£t gá»i AI, thá»i gian pháº£n há»“i, trÃ­ch dáº«n.
- `scripts/eval_report.md`: Báº£ng tá»•ng káº¿t sá»‘ Ä‘o vÃ  tá»· lá»‡ Ä‘áº¡t chuáº©n (Pass Rate %).

---

## ðŸ“ 6. Cáº¤U TRÃšC THÆ¯ Má»¤C REPO

```
K4-3A-E403-BTN/
â”œâ”€â”€ README.md              â† File nÃ y (Báº£ng thÃ nh viÃªn + HÆ°á»›ng dáº«n + ThÃ´ng tin Ä‘á» tÃ i)
â”œâ”€â”€ spec.md                â† AI Spec hoÃ n chá»‰nh 8 pháº§n (R1, R2, R3, R4)
â”œâ”€â”€ canvas-cp1.jpg & .md   â† Canvas 4 Ã´ Checkpoint 1
â”œâ”€â”€ run.py                 â† Launcher khá»Ÿi Ä‘á»™ng Fullstack 1 lá»‡nh (R5)
â”œâ”€â”€ requirements.txt       â† Danh má»¥c thÆ° viá»‡n phá»¥ thuá»™c
â”œâ”€â”€ .env.example           â† Máº«u biáº¿n mÃ´i trÆ°á»ng
â”‚
â”œâ”€â”€ scripts/               â† THÆ¯ Má»¤C CHá»¨A CÃC SCRIPT KIá»‚M THá»¬ & ÄO Äáº C
â”‚   â”œâ”€â”€ test_api.py        â† Script CLI kiá»ƒm tra nhanh Gemini API
â”‚   â”œâ”€â”€ eval_gemini.py     â† Script cháº¡y bá»™ Ä‘o Ä‘áº¡c Golden Set (CP3 / R4)
â”‚   â””â”€â”€ golden_set.json    â† Bá»™ 20 ca kiá»ƒm thá»­ 4 lá»›p trÃ­ch tá»« chatlog tháº­t
â”‚
â”œâ”€â”€ backend/               â† BACKEND (Python Flask REST API)
â”‚   â”œâ”€â”€ app.py             â† MÃ¡y chá»§ API phá»¥c vá»¥ /api/chat, /api/lecture
â”‚   â”œâ”€â”€ core/
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â””â”€â”€ tutor_engine.pyâ† LÃµi Guardrail Grounding & Gá»i Google Gemini API
â”‚   â””â”€â”€ data/
â”‚       â””â”€â”€ lecture_day02.mdâ† Dá»¯ liá»‡u bÃ i giáº£ng Day 2 cÃ³ mÃ£ Ä‘oáº¡n [T02-xxx]
â”‚
â””â”€â”€ frontend/              â† FRONTEND (Giao diá»‡n Web LMS Split-Screen)
    â”œâ”€â”€ index.html         â† Khung giao diá»‡n Split-Screen 2 cá»™t
    â”œâ”€â”€ style.css          â† Dark Navy Theme, hiá»‡u á»©ng highlight trÃ­ch dáº«n
    â””â”€â”€ app.js             â† Xá»­ lÃ½ tÆ°Æ¡ng tÃ¡c, 3 nÃºt demo 1-click, AI Inspector
```

---

## ðŸ“… 7. Lá»ŠCH CHECKPOINT & QUY Äá»ŠNH HACKATHON

| Má»‘c | Cáº§n hoÃ n thÃ nh | Háº¡n (ca 3A) | Tráº¡ng thÃ¡i nhÃ³m BTN |
|---|---|---|---|
| **CP1** | Canvas 4 Ã´ + Ä‘á»™i trÆ°á»Ÿng + link repo GitHub | 19:30 Â· 16/9 | **ÄÃƒ HOÃ€N THÃ€NH** |
| **CP2** | Cho tháº¥y luá»“ng hoáº¡t Ä‘á»™ng (mock báº¥m Ä‘Æ°á»£c / video) | 21:00 Â· 16/9 | **ÄÃƒ HOÃ€N THÃ€NH** |
| **CP3** | Video thao tÃ¡c 30s + sá»‘ Ä‘o (thá»­ bao nhiÃªu, Ä‘Ãºng bao nhiÃªu) | 16:00 Â· 17/9 | **ÄÃƒ Sáº´N SÃ€NG** (`scripts/eval_gemini.py`) |
| **CP4** | Chá»‘t `spec.md` â€” khoÃ¡ chuáº©n "Ä‘áº¡t" Â· tá»± khai pháº§n chÆ°a xong | 21:00 Â· 17/9 | **ÄÃƒ HOÃ€N THÃ€NH** (`spec.md`) |
| **CP5** | Slide PDF + video demo dá»± phÃ²ng cho buá»•i pitch | 13:00 Â· 18/9 | Äang chuáº©n bá»‹ |
| **CP6** | Thuyáº¿t trÃ¬nh vÃ²ng thi táº¡i phÃ²ng E403 | 17:30 Â· 18/9 | Sáºµn sÃ ng |

---

## âš–ï¸ 8. Báº¢O Máº¬T Dá»® LIá»†U ÄÆ¯á»¢C CUNG Cáº¤P
- ToÃ n bá»™ dá»¯ liá»‡u chatlog vÃ  transcript Ä‘Æ°á»£c cung cáº¥p trong hackathon thuá»™c quy Ä‘á»‹nh báº£o máº­t cá»§a khÃ³a há»c.
- NhÃ³m cam káº¿t: Chá»‰ sá»­ dá»¥ng dá»¯ liá»‡u trong pháº¡m vi bÃ i thi; khÃ´ng chia sáº» ra ngoÃ i khÃ³a há»c; khÃ´ng commit dá»¯ liá»‡u thÃ´ chÆ°a áº©n danh; tÃ´n trá»ng quyá»n riÃªng tÆ° cá»§a há»c viÃªn vÃ  giáº£ng viÃªn.
