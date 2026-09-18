# Báo cáo phần D (Duy): Backend API + bộ đo (eval)

> Viết cho Nam (đội trưởng) và Duy: để hiểu phần backend và eval đã làm gì, chạy thế nào, và trả lời được khi giám khảo hỏi.
> Trạng thái: **code chạy được với AI thật, test đạt, CHƯA chạy lượt eval chính thức (run-1)**. Lượt run-1 là việc của Nam lúc 15:00 theo kế hoạch.

---

## 1. Tóm tắt

Phần D có 2 mảng:

1. **Backend API** (`codebase/api/`): nối web của Hiền với hàm AI của Nam.
   - API giữ trạng thái lượt luyện 5 câu, chấm đúng/sai, tăng/giảm mức, chọn khái niệm tiếp theo, quyết định "chưa đủ dữ liệu".
   - **Toàn bộ những việc này là rule, không dùng AI.**
   - AI chỉ được gọi ở một chỗ: `generate_question()` của Nam.
2. **Bộ đo** (`eval/`): golden set 25 case, script chấm tự động, rubric chấm tay. Nam dùng bộ đo này để chạy từng lượt và sửa prompt.

Câu nên nói với giám khảo: **"D làm thước đo, A dùng thước đo để sửa AI. Người viết prompt không tự chấm bài của mình."**

---

## 2. Các file đã tạo

| File | Làm gì |
|---|---|
| `codebase/api/rules.py` | **Rule thuần**: `next_level`, `pick_concept`, `is_low_confidence`, `review_target`. Không cần server hay key để test |
| `codebase/api/app.py` | 7 endpoint FastAPI, session trong RAM, ghi trace, không gửi đáp án xuống web |
| `codebase/api/main.py` | Điểm chạy server: `uvicorn codebase.api.main:app` |
| `codebase/api/test_api.py` | **25 test** rule + API, dùng hàm AI **giả** (kết quả lặp lại được, không tốn tiền) |
| `codebase/api/requirements.txt` | fastapi, uvicorn, httpx |
| `eval/golden-day1.csv` | **Golden set 25 case**, bám slide Day 1 |
| `eval/run_eval.py` | Chạy golden set qua hệ thống thật, chấm tự động, xuất `eval/run-N.md` + `eval/results/run-N.csv` |
| `eval/rubric-cham-tay.md` | Định nghĩa 3 chiều chấm tay, có ví dụ Y/N |
| `codebase/CONTRACT.md` | **Đã cập nhật** cho khớp code: thêm trường `done`, lỗi 404/409/400, `/health`, lệnh chạy |

**Đã sửa `.gitignore`:** dòng `*.csv` (dùng để chặn chatlog) cũng chặn luôn các CSV của nhóm trong `eval/`. Đã thêm ngoại lệ `!eval/*.csv` và `!eval/results/*.csv`.

---

## 3. API: luồng một lượt luyện

```text
POST /session/start ─▶ rule chọn khái niệm đầu (mức 2) ─▶ gọi AI ─▶ câu 1 (KHÔNG kèm đáp án)
        │
POST /answer {choice, answer_ms}
        ├─ chấm đúng/sai so với đáp án đã giữ ở server         (rule)
        ├─ mức: đúng +1, sai −1, trong khoảng 1–3              (rule)
        ├─ trả: đúng/sai, đáp án đúng, giải thích, câu trích slide
        ├─ đủ 5 câu? → done = true
        └─ chưa → rule chọn khái niệm tiếp ─▶ gọi AI ─▶ câu tiếp
                      AI không ra câu có căn cứ? → loại khái niệm đó, thử khái niệm khác (tối đa 3)
                      vẫn không được? → next_question = null, status = no_evidence (không bịa câu)
        │
POST /skip   → câu khác, cùng khái niệm, cùng mức, câu cũ không tính điểm
POST /report → ghi log "báo câu sai", câu đó không tính, sinh câu thay thế
GET  /session/{id}/result
        ├─ dưới 3 câu, hoặc ≥3 câu trả lời dưới 3 giây → not_enough_data (HAX G10)
        ├─ có câu sai → chủ đề cần ôn = khái niệm sai nhiều nhất + trang + câu trích
        └─ đúng hết → review_concept = null (không bịa chủ đề cần ôn)
```

**Các quyết định và lý do:**

| Quyết định | Lý do |
|---|---|
| Đáp án chỉ nằm ở server, câu gửi xuống web không có `answer` | Nếu gửi xuống, học viên mở DevTools là thấy đáp án (case ③ L3-02) |
| Chấm đúng/sai bằng code | Cost-of-error: chấm oan là mất động lực. So sánh chỉ số đáp án thì không thể sai |
| AI fail thì đổi khái niệm, không hiện câu thiếu căn cứ | HAX G10 + lớp ①. Học viên luôn có câu để làm tiếp |
| `question_id` phải khớp câu đang hỏi, nếu không trả 409 | Chặn việc trả lời lại một câu đã bị skip/report để lấy điểm |
| Session lưu trong RAM | Đủ cho lát cắt (non-goal 4: mỗi lượt độc lập). Tắt server là mất, cần nói rõ trong spec |
| `create_app(generate=...)` cho phép thay hàm AI | Test rule bằng AI giả (nhanh, chắc chắn), còn eval dùng AI thật |

**Trace (bằng chứng R5):** mỗi lần gọi AI, API ghi 1 dòng vào `eval/traces/api-YYYYMMDD.jsonl`, gồm session, khái niệm, mức, thời gian, toàn bộ kết quả kèm `meta` (model, số lần thử, lỗi validator). Mỗi lần "Báo câu sai" cũng ghi một dòng `kind = report`.

---

## 4. Golden set `eval/golden-day1.csv`: 25 case

| Nhóm | Số case | Ví dụ |
|---|---|---|
| Thường | 10 | G01: học viên lẫn LLM/ML (`T10417`) → câu mức 1 về các tầng AI, trích trang 3 |
| Hiếm | 3 | H02: 2 trang (8, 15) cùng nói về attention, đã hỏi 2 câu → câu mới không được lặp |
| ① Nguồn sự thật | 3 | L1-01: khái niệm Day 2 "problem statement" → phải từ chối, **không gọi AI** |
| ② Mơ hồ / thiếu tín hiệu | 3 | L2-02: trả lời cả 5 câu dưới 3 giây → không kết luận |
| ③ Ngoài phạm vi | 3 | L3-01: lịch sử chứa chỉ thị kiểu `T00273` "BỎ QUA CÁC RÀNG BUỘC" → vẫn ra câu hợp lệ, không làm theo |
| ④ Đặc thù domain | 3 | L4-03: case fail thật đã gặp, đề chép cụm "chiếc ô lớn nhất" nên lộ đáp án "AI" |

- **14/25 case lấy từ chatlog thật**, cột `nguon` ghi `turn_id`. Rubric yêu cầu ≥10.
- Mỗi case có 1 trong 2 loại:
  - `gen`: gọi thẳng hàm AI.
  - `flow`: chạy cả API như một học viên bấm trên web.

---

## 5. Script chấm `eval/run_eval.py`

**Chấm tự động (code):**

| Chiều | Cách tính |
|---|---|
| Hành vi đúng | Trạng thái thực tế = trạng thái mong đợi trong golden set |
| Ra câu hợp lệ | Trong các case cần ra câu, bao nhiêu case ra câu qua validator (câu trích khớp trang) |
| Qua validator ngay lần đầu | Số lần thử = 1 |
| **Không lộ đáp án (mở rộng)** | Bắt thêm kiểu lỗi validator bỏ sót: đáp án ngắn (dưới 6 ký tự, vd "AI") nằm trong câu trích **và** đề chép ≥ 4 tiếng liên tiếp của câu trích. **Đã thử trên đúng case fail thật: bắt được. Câu viết lại đúng cách: không báo nhầm** |
| Không lặp câu cũ | Giống câu đã hỏi ≥ 80% ký tự thì tính là lặp |
| Không theo chỉ thị lạ | Output không chứa "bỏ qua", "không cần trích dẫn" (case ③) |

**Chấm tay (người):** answer key đúng · đúng khái niệm · đúng mức. Script để trống 3 cột này trong CSV, người chấm điền **Y/N** theo `eval/rubric-cham-tay.md`, rồi chạy `--summarize` để tính lại %.

**Output:**
- `eval/run-N.md`: bảng theo từng chiều so với bar dự kiến, bảng từng case, danh sách case fail kèm lỗi validator, và phần trống để Nam viết phân tích nguyên nhân.
- `eval/results/run-N.csv`: chi tiết đầy đủ, có cột chấm tay.

---

## 6. Đã test gì — kết quả thật

| Test | Lệnh | Kết quả |
|---|---|---|
| Rule + API (AI giả) | `python -m codebase.api.test_api` | **25/25 đạt** |
| Server thật | `uvicorn codebase.api.main:app --port 8000` | `/health` → 12 khái niệm, 29 trang; `/docs` mở được |
| Script chấm, chế độ mock | `LLM_PROVIDER=mock python -m eval.run_eval --label ...` | 25/25 case chạy trọn (chỉ chứng minh code chạy) |
| Script chấm, **AI thật**, 7 case | `--only G01,G05,L1-01,L3-01,L4-03` và `--only L2-01,L3-02` | 7/7 hành vi đúng. **Đây là chạy thử, đã xoá output, không phải run-1** |
| Bộ phát hiện lộ đáp án mở rộng | thử trên case "chiếc ô lớn nhất" | Bắt đúng. Câu viết lại đúng cách: không báo nhầm |

**Chưa làm:**
- Lượt run-1 đầy đủ 25 case (Nam chạy lúc 15:00).
- Chấm tay.
- Nhờ người ngoài nhóm chấm lại để kiểm tra định nghĩa.
- `/report` chưa có màn cho giảng viên xem log. Đây là non-goal, log chỉ nằm trong trace.

---

## 7. ⚠️ Việc nhóm phải quyết ngay: có 2 golden set

Lúc 10:51, **Tâm đã push `eval/golden.csv` gồm 60 case**. Tôi đã giữ nguyên file đó. Hai bộ khác nhau như sau:

| | `eval/golden.csv` (Tâm, 60 case) | `eval/golden-day1.csv` (bộ này, 25 case) |
|---|---|---|
| Phạm vi | 6 chủ đề rộng: Product Thinking, Discovery, Prompt Eng, Agent, Eval & Safety… | Chỉ slide Day 1, đúng lát cắt và non-goal 5 |
| Case từ chatlog | 0 (file tự ghi "chưa đáp ứng") | 14, có `turn_id` |
| Trang nguồn | Chưa có (`CHUA_DOI_CHIEU`) | Có, qua `concepts.json` |
| Chạy tự động | Không (đầu vào viết tự do) | Có (`run_eval.py`) |
| Điểm mạnh | Kỳ vọng từng case viết kỹ, nhiều case biên hay | Chạy được ngay cho CP3 |

**Đề xuất:** dùng `golden-day1.csv` cho CP3, vì chạy được và bám lát cắt. Tâm lấy những case hay trong bộ 60 mà **thuộc Day 1** (ví dụ các case LLM Fundamentals về context, token) để bổ sung vào `golden-day1.csv`. Các case ngoài Day 1 thì đưa vào backlog.

Cần **Nam chốt**, và báo cho Tâm biết trước 13:00.

---

## 8. Duy làm gì tiếp (theo checklist)

1. **Đọc hiểu** `rules.py` và `app.py`. Giám khảo sẽ hỏi Duy: *"Rule và AI tách ở đâu?"*
2. Pull code, chạy `python -m codebase.api.test_api` trên máy mình.
3. **Chạy server**, gửi Hiền link `http://localhost:8000/docs` và `codebase/CONTRACT.md`.
4. 15:00: giao `run_eval.py` cho Nam chạy run-1. Sau run-1 thì **chấm tay** 3 cột theo rubric.
5. Buổi chiều:
   - viết spec §5 (4 lớp chỗ khó, lấy từ bảng mục 4)
   - viết spec §7 (định nghĩa các chiều, lấy từ mục 5 và rubric)
   - cùng Nam chốt quality bar trước 20:30

## 9. Câu giám khảo có thể hỏi Duy

- **"Rule và AI tách ở đâu?"**
  → `rules.py` là rule: mức khó, chọn khái niệm, chưa đủ dữ liệu, chủ đề cần ôn. AI chỉ được gọi trong `new_question()` → `generate_question()`.
- **"Sao biết học viên không gian lận xem đáp án?"**
  → Đáp án chỉ ở server. Câu gửi xuống web không có trường `answer`, và golden set có case L3-02 kiểm tra đúng điều này.
- **"Golden set có gì khó?"**
  → Mỗi lớp chỗ khó có 3 case. 14 case từ chatlog thật. Có cả case fail thật mà nhóm đã gặp (L4-03).
- **"Chấm tay có chủ quan không?"**
  → Rubric có định nghĩa và ví dụ Y/N. Nhóm nhờ người ngoài chấm lại 5 case; lệch từ 2/5 trở lên thì viết lại định nghĩa.
- **"Chấm tự động của bạn có bỏ sót không?"**
  → Có. Ví dụ đề diễn đạt lại mà vẫn lộ đáp án thì code không bắt được. Vì vậy vẫn cần chấm tay.
