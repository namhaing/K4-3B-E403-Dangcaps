# Hợp đồng giữa 3 tầng — web (Hiền) · api (Duy) · ai (Nam)

> Chốt trước khi code. Muốn đổi tên trường hay format → báo cả 3 người, sửa file này trước, rồi mới sửa code.

```text
web (Hiền)  ──HTTP JSON──▶  api (Duy)  ──gọi hàm Python──▶  ai (Nam)
                                  ▲
                 eval/run_eval.py (Duy) cũng gọi thẳng hàm của Nam
```

## 1. Dữ liệu dùng chung — `codebase/data/`

| File | Ai sở hữu | Commit? | Dạng |
|---|---|---|---|
| `pages.json` | Nam (sinh bằng `python codebase/ai/extract_pages.py`) | **Không** (nội dung data pack) | `{"3": "text trang 3", ...}` |
| `concepts.json` | Hiền chốt (Nam đã làm bản nháp) | Có | `{"lecture", "level_guide": {"1","2","3"}, "concepts": [{"concept_id", "name", "pages": [3]}]}` |

## 2. Hàm AI — Nam giao cho Duy

```python
from codebase.ai import generate_question, load_concepts, load_pages

pages, concepts = load_pages(), load_concepts()
q = generate_question(concept_id="ai_layers", level=2, pages=pages, history=[{"question": "..."}], concepts=concepts)
```

**Khi thành công:**
```json
{
  "status": "ok",
  "concept_id": "ai_layers",
  "level": 2,
  "page": 3,
  "evidence_quote": "Machine learning — học từ dữ liệu thay vì viết luật tay.",
  "question": "Điểm khác biệt cốt lõi của ML so với lập trình truyền thống là gì?",
  "options": ["Học từ dữ liệu", "Viết luật bằng tay", "Luôn dùng mạng nơ-ron", "Chỉ xử lý văn bản"],
  "answer": 0,
  "explanation": "Slide trang 3: ML học từ dữ liệu thay vì viết luật tay.",
  "meta": {"provider": "openai", "model": "gpt-4o-mini", "attempts": 1, "errors": [], "latency_ms": 2140}
}
```

**Khi không ra được câu hợp lệ:**
```json
{"status": "no_evidence", "reason": "validation_failed", "meta": {...}}
```

| `reason` | Nghĩa | API nên làm |
|---|---|---|
| `concept_not_in_lecture` | Khái niệm không có trong slide buổi này (lớp ①) | Chọn khái niệm khác |
| `validation_failed` | AI sinh 2 lần đều bị validator loại | Chọn khái niệm khác, báo web `no_evidence` |
| `llm_error` | Lỗi mạng, timeout, thiếu key | Báo web `no_evidence` |
| `invalid_level` · `page_text_missing` | Lỗi input | Lỗi phía API/dữ liệu, cần sửa |

Quy ước:
- `answer` là **số thứ tự 0–3** trong `options`.
- `history` chỉ cần mỗi phần tử có `"question"`. Hàm dùng nó để không hỏi trùng câu.
- `meta` chỉ để **ghi trace** vào `eval/traces/*.jsonl`. **Không gửi xuống web.**
- **Chưa có hàm thật?** Đặt `LLM_PROVIDER=mock` trong `.env`. Hàm vẫn chạy như thật nhưng trả câu giả có chữ `[MOCK]`.

## 3. API — Duy giao cho Hiền

Base URL: `http://localhost:8000`. **Bật CORS** cho web.

⚠️ Câu hỏi gửi xuống web **không có `answer`**. Nếu gửi, học viên mở DevTools là thấy đáp án.

**Question (dạng câu hỏi gửi xuống web)**
```json
{"question_id": "q3", "index": 3, "total": 5, "concept_name": "Các tầng AI", "level": 2, "page": 8,
 "question": "...", "options": ["...", "...", "...", "..."], "skips_left": 2}
```

| Endpoint | Gửi lên | Nhận về |
|---|---|---|
| `POST /session/start` | `{"lecture": "D01", "learner_id": "uuid-cua-trinh-duyet", "focus_concept": "ai_types" (tuỳ chọn)}` | `{"session_id": "abc", "question": Question, "status": "ok", "focus_weak": ["Tên khái niệm đang yếu", …]}` |
| `POST /answer` | `{"session_id", "question_id", "choice": 1, "answer_ms": 4200, "timed_out": false}` — chế độ đấu hết giờ chưa chọn: `choice = -1`, `timed_out = true` | `{"correct": false, "correct_choice": 0, "explanation", "page", "evidence_quote", "next_question": Question \| null, "done": false, "status"}` |
| `POST /skip` | `{"session_id", "question_id"}` | `{"question": Question, "status"}` |
| `POST /report` | `{"session_id", "question_id", "reason": "wrong_answer" \| "unclear" \| "not_in_slide"}` | `{"question": Question, "status": "reported"}` |
| `GET /session/{id}/result` | — | `{"items": [{"concept_name", "level", "correct"}], "review_concept", "page", "evidence_quote", "status"}` |
| `GET /health` | — | `{"ok": true, "concepts": 12, "pages": 29}` |
| `GET /learner/{learner_id}/progress` | — | `{"lecture", "min_answers": 3, "summary": {"dang_yeu": n, "chua_du_du_lieu": n, "chua_luyen": n, "da_vung": n}, "concepts": [{"concept_id", "concept_name", "pages", "status", "status_label", "attempts", "correct", "recent": [true, false…], "status_reason": "Sai 2/3 câu gần nhất"}], "weak": [...]}` |
| `GET /learner/{learner_id}/concept/{concept_id}/review` | — | `{"concept_name", "status", "status_label", "status_reason", "attempts", "correct", "recent", "mistakes": [{"question", "options", "choice", "correct_choice", "explanation", "evidence_quote", "page", "level", "at"}], "quotes": [{"page", "quote"}], "slides": [{"page", "text"}]}` · 404 nếu khái niệm lạ |
| `GET /slide/{page}.png` | — | Ảnh PNG đúng trang slide (vẽ từ PDF gốc trên máy chạy server, giữ trong RAM). **404** nếu máy không có PDF (`data/vlearn-pack/slides/d1-slide-hackathon.pdf`, hoặc biến môi trường `SLIDE_PDF`) hoặc trang không tồn tại → web tự hiện chữ thay ảnh |

- `done = true` nghĩa là đã xong 5 câu, web chuyển sang gọi `/result`.
- `done = false` và `next_question = null` nghĩa là không khái niệm nào còn ra được câu có căn cứ (`status = no_evidence`). Web hiện thông báo và cho xem kết quả.
- `status = no_evidence` **kèm** `next_question` khác null nghĩa là AI không ra câu cho khái niệm định hỏi, API đã **tự đổi sang khái niệm khác**. Web hiện dòng thông báo phía trên câu mới.
- `review_concept = null` với `status = ok` nghĩa là **đúng hết**, không có chủ đề cần ôn. Web không được bịa chủ đề.
- Lỗi HTTP: `404` khi không có lượt luyện (session lạ), `409` khi `question_id` không phải câu đang hỏi (ví dụ câu đã bị skip/report) **hoặc** khi `/skip` đã hết lượt đổi (`skips_left = 0`), `400` khi buổi không hỗ trợ.
- `status` chỉ có 4 giá trị:

| `status` | Web hiển thị |
|---|---|
| `ok` | Bình thường |
| `no_evidence` | "Chưa có căn cứ trong slide cho khái niệm này, chuyển sang khái niệm khác" |
| `not_enough_data` | Màn kết quả: "Chưa đủ dữ liệu để đánh giá. Làm thêm 2 câu?" |
| `reported` | "Đã ghi nhận, câu này không tính điểm" + câu thay thế |

## 4. Rule do API (Duy) làm, không giao cho AI

- Câu 1: mức 2, khái niệm đầu tiên chưa hỏi.
- Đúng → mức +1, sai → mức −1, kẹp trong 1–3.
- Vừa sai → giữ khái niệm đó. Vừa đúng → sang khái niệm chưa hỏi.
- Low-confidence (`not_enough_data`): dưới 3 câu đã trả lời, **hoặc** ≥3 câu có `answer_ms < 3000`.
- `/report`: câu bị báo không tính điểm, ghi log.
- `/skip`: cùng khái niệm, cùng mức, đưa câu cũ vào `history`. **Tối đa 2 lần mỗi lượt** (`rules.MAX_SKIPS`); mỗi câu gửi xuống có `skips_left`, web hiện "Đổi câu khác (còn n)", hết thì khoá nút. `/report` **không** trừ lượt đổi (là đường báo lỗi). Mỗi lần đổi ghi trace `kind = "skip"`.

## 4b. Đo chỗ yếu qua nhiều lượt (thêm 18/9)

- Web tạo **mã học viên ngẫu nhiên** một lần (`localStorage["solo-arena-learner"]`, 8–64 ký tự `A-Za-z0-9-`) và gửi `learner_id` khi `/session/start`. Không gửi → lượt độc lập như cũ.
- Sai định dạng → **400**. Không có endpoint liệt kê học viên; hồ sơ lưu ở `codebase/data/progress.json` (**không commit**).
- Mỗi `/answer` cộng dồn theo khái niệm, **trừ** câu có `answer_ms < 3000` (đoán mò) và câu `timed_out = true` (hết giờ ở chế độ đấu). Câu bị `/skip`, `/report` không tính.
- `status` của khái niệm (rule, không AI):

| `status` | Khi nào | Web hiển thị |
|---|---|---|
| `chua_luyen` | 0 câu | "Chưa luyện" |
| `chua_du_du_lieu` | 1–2 câu | "Chưa đủ dữ liệu" (không kết luận) |
| `dang_yeu` | ≥ 3 câu và sai ≥ 2 trong 3 câu gần nhất | "Đang yếu" + nút "Ôn chỗ yếu ngay" |
| `da_vung` | ≥ 3 câu và đúng ≥ 2 trong 3 câu gần nhất | "Đã vững" |

- Lượt mới có hồ sơ: thứ tự khái niệm = đang yếu → chưa luyện/chưa đủ dữ liệu → đã vững (mỗi nhóm vẫn xáo). `focus_weak` liệt kê phần đang yếu để web báo "Lượt này ưu tiên ôn lại…".
- **`focus_concept`** ("Luyện 3 câu phần này"): lượt chỉ **3 câu**, cả 3 về đúng khái niệm đó, mức vẫn đổi theo đúng/sai. AI hụt thì thử lại chính khái niệm đó (không có khái niệm khác để chuyển). `question.total = 3`.
- **Màn "Ôn lại kiến thức"** (`/review`): các câu học viên đã sai (giữ 5 câu gần nhất) kèm đáp án đúng, giải thích, câu trích — đều là nội dung **đã qua validator + kiểm chéo** — cùng nội dung slide gốc. **Không gọi AI.**

## 5. Chạy thử

```bash
.\.venv\Scripts\python.exe -m uvicorn codebase.api.main:app --reload --port 8000   # rồi mở http://localhost:8000/docs
.\.venv\Scripts\python.exe -m codebase.api.test_api                               # 41 test rule + API + tiến độ, dùng AI giả
```

## 6. Môi trường

`.env` ở gốc repo (copy từ `.env.example`):
```text
LLM_PROVIDER=openai | gemini | mock
LLM_MODEL=...
LLM_API_KEY=...
```
Cài thư viện vào môi trường riêng:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r codebase/ai/requirements.txt -r codebase/api/requirements.txt
```
