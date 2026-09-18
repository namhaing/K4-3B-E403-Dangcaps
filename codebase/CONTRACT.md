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
 "question": "...", "options": ["...", "...", "...", "..."]}
```

| Endpoint | Gửi lên | Nhận về |
|---|---|---|
| `POST /session/start` | `{"lecture": "D01"}` | `{"session_id": "abc", "question": Question, "status": "ok"}` |
| `POST /answer` | `{"session_id", "question_id", "choice": 1, "answer_ms": 4200}` | `{"correct": false, "correct_choice": 0, "explanation", "page", "evidence_quote", "next_question": Question \| null, "done": false, "status"}` |
| `POST /skip` | `{"session_id", "question_id"}` | `{"question": Question, "status"}` |
| `POST /report` | `{"session_id", "question_id", "reason": "wrong_answer" \| "unclear" \| "not_in_slide"}` | `{"question": Question, "status": "reported"}` |
| `GET /session/{id}/result` | — | `{"items": [{"concept_name", "level", "correct"}], "review_concept", "page", "evidence_quote", "status"}` |
| `GET /health` | — | `{"ok": true, "concepts": 12, "pages": 29}` |

- `done = true` nghĩa là đã xong 5 câu, web chuyển sang gọi `/result`.
- `done = false` và `next_question = null` nghĩa là không khái niệm nào còn ra được câu có căn cứ (`status = no_evidence`). Web hiện thông báo và cho xem kết quả.
- `status = no_evidence` **kèm** `next_question` khác null nghĩa là AI không ra câu cho khái niệm định hỏi, API đã **tự đổi sang khái niệm khác**. Web hiện dòng thông báo phía trên câu mới.
- `review_concept = null` với `status = ok` nghĩa là **đúng hết**, không có chủ đề cần ôn. Web không được bịa chủ đề.
- Lỗi HTTP: `404` khi không có lượt luyện (session lạ), `409` khi `question_id` không phải câu đang hỏi (ví dụ câu đã bị skip/report), `400` khi buổi không hỗ trợ.
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
- `/skip`: cùng khái niệm, cùng mức, đưa câu cũ vào `history`.

## 5. Chạy thử

```bash
uvicorn codebase.api.main:app --reload --port 8000   # rồi mở http://localhost:8000/docs
python -m codebase.api.test_api                       # 25 test rule + API, dùng AI giả
```

## 6. Môi trường

`.env` ở gốc repo (copy từ `.env.example`):
```text
LLM_PROVIDER=openai | gemini | mock
LLM_MODEL=...
LLM_API_KEY=...
```
Cài thư viện: `pip install -r codebase/ai/requirements.txt -r codebase/api/requirements.txt`
