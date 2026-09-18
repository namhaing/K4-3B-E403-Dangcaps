# Kế hoạch nhóm — VLearn Solo Arena · 4 người (A · B · C · D)

> Lát cắt (canvas dòng 5): *Một học viên vừa xong buổi học, đang trong một lượt luyện 5 câu · cần câu tiếp theo vừa sức · hệ thống chọn khái niệm × mức khó theo câu vừa rồi đúng/sai, rồi **AI sinh câu hỏi bám đúng trang slide của khái niệm đó** · kết quả là câu hỏi kèm `[trang N]`, cuối lượt là một chủ đề cần ôn có dẫn nguồn.*
> Demo khoá vào **slide Day 1 (AI / ML / DL / LLM)**.

---

## 0. Nhận xét canvas

**Giữ nguyên**
- Lát cắt chỉ có **1 quyết định AI**: sinh câu hỏi bám `[trang N]` cho khái niệm × mức khó mà rule đã chọn.
- Automation **Conditional**. Non-goals trong canvas **đã cập nhật theo mục 9.4**, nên đúng cả khi chỉ có core lẫn khi làm thêm phần mở rộng.
- Số mining đã chạy lại và khớp:
  - `understanding_level`: 20/13.494
  - `suggest_next_topic`: 18
  - `motivate`: 21
  - `celebrate_progress`: 7
  - 114/448 học viên K4 (25,4%) chỉ hỏi 1 lần

**Đã sửa (18/9)**
- `.gitignore` đã chặn `data/`, `*.csv`, `.env` và tài liệu đề.
- `canvas.md` còn 1 phiên bản. Dòng 5–6, non-goals và quality bar dự kiến đã khớp với kế hoạch này.
- `luong.md` đã viết lại theo flow luyện 5 câu. Đã xoá `luong_app.md` và 2 file checklist cũ.
- `SOLO-ARENA-HANDOFF.md` có ghi chú ở đầu file: phân công, bar và phạm vi trong đó đã cũ.
- **14:00 — gỡ data pack khỏi repo public + xoá khỏi toàn bộ lịch sử git (force-push).** Commit `ff8a6b1` đã đưa `eval/slides/*.pdf`, `eval/chatlog/`, `__pycache__` lên GitHub. Đã xoá khỏi 17/17 commit, `.gitignore` chặn `eval/slides/`, `eval/chatlog/`, `*.pdf`; `eval/candidates.csv` rút trích đoạn còn ≤ 80 ký tự. **Mỗi người phải chạy `git fetch` + `git reset --hard origin/main`** (lưu thay đổi chưa commit trước). ⛔ Không đưa slide/chatlog vào repo nữa.
- **16:35 — nhánh `BuiPhuongDuy_2A202602684` (commit "data" 15:03) đã đưa 6 transcript + DATA_DICTIONARY của data pack lên GitHub → nhánh đã bị xoá** (xác nhận không còn nhánh nào chứa data pack). `.gitignore` trên `main` đã chặn `codebase/data/vlearn-pack/`. ⛔ Nhắc cả nhóm: **kể cả nhánh riêng cũng là public**.

**Còn phải làm**
1. Pain mới có bằng chứng "tutor không làm", chưa có bằng chứng "học viên cần". **Khảo sát 20 người là bắt buộc.** Proxy "hỏi 1 lần" có thể là người đã hài lòng, nên ghi rõ giới hạn trong spec.
2. Quality bar cần có chiều **answer key đúng**, đây là lỗi nguy hiểm nhất: chấm oan học viên thì mất động lực.
3. Nếu mức khó do rule quyết định thì chiều "mức khó đổi đúng chiều ≥75%" luôn đạt 100%, không có ý nghĩa. Thay bằng "câu sinh ra **thật sự** ở đúng mức khó yêu cầu".
4. Slide chỉ có Day 1 và Day 2, nên demo khoá vào Day 1. Khái niệm Day 2 **không** đưa vào golden set, chỉ dùng làm case ① "ngoài phạm vi buổi".

---

## 1. Thiết kế kỹ thuật

**Luồng:** chọn Day 1 → câu 1 (mức 2) → trả lời trắc nghiệm → câu 2 … câu 5 → màn kết quả: 1 chủ đề cần ôn + `[trang N]`.

| Phần | Làm bằng | Lý do |
|---|---|---|
| Tăng/giảm mức khó | **Rule**: đúng → +1, sai → −1, kẹp trong 1–3 | Không cần AI, minh bạch |
| Chọn khái niệm tiếp theo | **Rule**: vừa sai → giữ khái niệm đó, vừa đúng → sang khái niệm chưa hỏi | Minh bạch, dễ giải thích |
| **Sinh câu hỏi bám trang slide** cho khái niệm × mức đã chọn | **LLM, quyết định trung tâm** | Elo hay rule không sinh được câu hỏi bám trang 17 |
| Low-confidence | **Rule**: dưới 3 câu đã trả lời, **hoặc** ≥3 câu trả lời dưới 3 giây (dấu hiệu đoán mò) → "Chưa đủ dữ liệu để đánh giá" | Định nghĩa dùng chung cho canvas, UI, spec §6 và golden set |
| Chấm đúng/sai | So với đáp án trắc nghiệm | Tránh việc AI chấm oan |
| Kiểm căn cứ | Code kiểm `evidence_quote` có nằm trong text trang N | Đo tự động lớp ①, chặn bịa |

**Output JSON của LLM:**
```json
{ "concept_id": "", "level": 1, "page": 0, "evidence_quote": "", "question": "", "options": ["", "", "", ""], "answer": 0, "explanation": "" }
```
Validator fail → sinh lại 1 lần. Fail tiếp → hiện *"Chưa có căn cứ cho khái niệm này"* và đổi khái niệm (failure path).

**Câu trả lời chuẩn bị cho giám khảo:** *"Elo xếp hạng được, nhưng không sinh nổi một câu hỏi bám trang 17 của slide buổi này. Vì vậy AI của chúng em nằm ở phần sinh câu hỏi có căn cứ, không nằm ở phần xếp hạng."*

---

## 2. Vai trò

> **A = Nguyễn Hải Nam** (đội trưởng) · **B = Nguyễn Trần Bảo Tâm** · **C = Trần Thị Thu Hiền** · **D = Bùi Phương Duy** (khớp dòng 7 trong `canvas.md`)

Mỗi người giữ **1 mảng code** và **1 mảng spec/tài liệu**, nên ai cũng tự giải thích được một phần kỹ thuật khi giám khảo hỏi (vibe-coding rule).

| Người | Vai | Phần code | Phần spec / tài liệu | Giám khảo sẽ hỏi |
|---|---|---|---|---|
| **A** | Trưởng nhóm · **AI + vòng eval** | `codebase/ai/`: prompt, `generate_question()`, validator · `pages.json` · chạy eval từng lượt + phân tích lỗi | `spec.md` §4 §9, **chốt quality bar** (cùng D), `README`, `canvas.md`, **nộp 5 form** | "AI quyết định gì? Sao không dùng Elo? Case fail nặng nhất là gì, đã sửa thế nào?" |
| **B** | Evidence · **Data script** | `mining.py`, `eval/extract_cases.py` (lọc case từ chatlog) | `spec.md` §1 §2 §3 §8, `validation/`, slide | "Số này đếm thế nào? Case chatlog lọc ra sao?" |
| **C** | **Frontend** | `codebase/web/`: màn luyện 5 câu, 4 đường đi, màn kết quả | `concepts.json`, `spec.md` §6 (4 đường đi), video CP3/CP5 | "Phần nào mock? 4 đường đi nằm ở màn nào?" |
| **D** | **Eval (bộ đo) + Backend** | `eval/golden.csv`, `eval/run_eval.py` (chấm tự động) · `codebase/api/`: API, rule mức khó, session, trace log | `spec.md` §5 §7, rubric chấm tay | "Golden set gồm gì? Mỗi chiều chất lượng chấm thế nào? Rule và AI tách ở đâu?" |

**A và D chia phần AI + eval như sau**

| | A | D |
|---|---|---|
| AI | Viết prompt, `generate_question()`, validator, sửa prompt sau mỗi lượt | Gọi hàm của A từ API |
| Eval | **Chạy** từng lượt, **đọc từng case fail**, phân tích nguyên nhân, quyết định sửa gì, viết `eval/run-N.md` | **Xây** golden set, **viết** script chấm, viết rubric chấm tay, nhờ người ngoài chấm lại |
| Quality bar | Đề xuất con số từ kết quả lượt 1 | Viết định nghĩa kiểm chứng được cho từng chiều. Cả hai cùng chốt trước 20:30 |

Nói gọn: **D làm thước đo, A dùng thước đo để sửa AI.** Cách chia này tránh việc người viết prompt tự chấm bài của mình.

**Vì sao chia như vậy**
- A giữ quyết định AI trung tâm, nên trưởng nhóm là người trả lời được câu khó nhất: *"AI ở đâu, sai thì sao"*.
- D làm backend nhỏ (API lưu session trong RAM, khoảng 200 dòng) cùng hạ tầng eval. Cả hai đều là việc "khung chạy" quanh hàm AI của A.
- B viết script lọc ≥12 case từ chatlog, gỡ bớt việc cho D.
- Slide và §8 giao cho B để A dành thời gian cho vòng lặp AI.

## 2b. Hợp đồng giữa 3 tầng (chốt trong 30 phút đầu)

> **Bản chi tiết (đủ JSON mẫu, `reason`, `status`, rule): [`codebase/CONTRACT.md`](codebase/CONTRACT.md).** Bảng dưới là bản tóm tắt.

```text
web (C)  ──HTTP──▶  api (D)  ──gọi hàm──▶  ai (A)
                                  ▲
                    eval/run_eval.py (D) cũng gọi thẳng hàm của A
```

**API (D cung cấp cho C)**

| Endpoint | Input | Output |
|---|---|---|
| `POST /session/start` | `{lecture: "D01"}` | `{session_id, question}` |
| `POST /answer` | `{session_id, choice, answer_ms}` | `{correct, explanation, page, next_question \| null, status}` |
| `GET /session/{id}/result` | — | `{review_concept, page, evidence_quote, status}` |
| `POST /report` · `POST /skip` | `{session_id, reason?}` | `{question, status}` |

`status` ∈ `ok` · `no_evidence` (failure) · `not_enough_data` (low-confidence) · `reported` (correction)

**Hàm AI (A cung cấp cho D)**
```python
generate_question(concept_id, level, pages, history) -> dict   # JSON ở mục 1, hoặc {"status": "no_evidence"}
```

Trong lúc chờ nhau, mỗi tầng dùng **stub trả JSON cố định**:
- C dựng UI trên API giả.
- D dựng API và script eval trên hàm AI giả.
- A test hàm AI bằng script riêng.

## 2c. Khối lượng ước tính (sau khi cân lại)

| Người | Việc kỹ thuật | Việc tài liệu / người dùng | Tổng |
|---|---|---|---|
| **A** | `pages.json` 0,5h · prompt + `generate_question()` + validator 2,5h · lượt eval 1 + phân tích 1h · sửa prompt + lượt 2 1,5h · lượt cuối 1h | repo + spec §4 + ghép spec + nộp form ~2,5h | **~9h** |
| **B** | `mining.py` 0,3h · `extract_cases.py` 1,5h · điền 10 case vào golden 1h | khảo sát 20 người ~3h · §1 §2 §3 §8 ~2h · user test 5 người 1h · slide 1,5h | **~10h** (có thời gian chờ khi khảo sát) |
| **C** | 4 màn trên stub 3h · nối API 0,5h · 4 đường đi + loading 2h · sửa UI theo feedback 0,5h | `concepts.json` 1h · §6 + cột HAX/PAIR 1h · 2 video 0,7h | **~9h** |
| **D** | API + rule + session + trace 2,5h · `/report` `/skip` + xử lý lỗi 1h · `run_eval.py` 1,5h | golden set (phần còn lại) 1,5h · rubric + chấm tay 2 lượt 1,5h · §5 §7 1,5h · người ngoài chấm lại 0,5h | **~10h** |

- **Cần canh:** D và B hơi nặng hơn. Nếu C xong sớm thì C nhận thêm việc chấm tay lượt 2 với D, hoặc làm đối thủ mock nếu nhóm chọn làm phần thách đấu.

---

## 3. Giai đoạn 1 · bây giờ → CP3 (16:00 · 18/9)

> CP3 cần: video 30 giây AI chạy thật · golden set ≥20 · bảng kết quả lượt 1 có %.

### A — Nam · Trưởng nhóm + AI
- [x] **(15 phút, làm đầu tiên)** Sửa `.gitignore`:
  ```
  data/
  *.csv
  .env
  01-*.md
  02-*.md
  03-*.md
  04-*.md
  tracks/
  examples/
  further-reading/
  ```
- [x] Tạo `codebase/{api,web,ai}`, `eval/traces/`, `validation/`, `reflection/` (kèm `.gitkeep`), `.env.example`. *(đã tạo trên máy Nam; **chưa push** `api/ web/ eval/ validation/ reflection/`)*
- [ ] Chốt hợp đồng ở mục 2b với C và D. *(bản nháp đã viết: `codebase/CONTRACT.md`, chờ Hiền + Duy đồng ý)*
- [x] Viết `codebase/ai/extract_pages.py`: trích text slide Day 1 → `pages.json` dạng `{page, text}`. **Giao cho D trước 11:00.**
- [x] Viết prompt với output JSON như mục 1: chỉ dùng text trang được đưa vào, câu trích phải nguyên văn, mô tả mức 1–3 lấy từ `concepts.json`.
- [x] Viết `generate_question()`.
- [x] Điền `.env` (openai · `gpt-4o-mini`), **gọi AI thật chạy được**: `try_generate --all --level 2` → **12/12 qua validator**, 1 khái niệm (`agent`) phải thử lần 2, mỗi câu 2–5 giây. *(18/9)*
  - ⚠️ Phát hiện khi đọc tay: câu "mức 2" phần lớn vẫn là kiểu định nghĩa (gần mức 1); câu `ai_layers` gần lộ đáp án (đề chép cụm "chiếc ô lớn nhất", đáp án "AI" dưới ngưỡng 6 ký tự nên validator không bắt). → đưa vào golden set + sửa prompt ở vòng eval.
- [x] Viết validator (11/11 test offline đạt: `python -m codebase.ai.test_validator`):
  - `evidence_quote` phải nằm trong text trang `page`
  - `answer` phải có trong `options`
  - đáp án không được xuất hiện trong đề
  - fail → sinh lại 1 lần → fail tiếp thì trả `no_evidence`
- [x] **Vòng sửa đầu tiên (chạy thử, chưa phải run-1)** *(18/9)* — ghi vào spec §9 Changelog:
  - Duy: tách chiều "lộ đáp án" (đề chứa nguyên văn đáp án) và chiều mới "chép cụm câu trích" (≥4 tiếng liên tiếp). Lý do: case L4-03 đề hỏi "khái niệm nào là 'chiếc ô lớn nhất'" mà bộ đo cũ chấm ✅. Golden thêm cột `kiem_them`.
  - Nam: thêm luật 9 (không chép cụm câu trích) + luật 10 (đã hỏi thì dùng ý khác) vào prompt.
  - Kết quả 2 lần × 4 case: vẫn **3/8 câu chép cụm** ("hệ thống có yếu tố thông minh") → prompt mới chỉ đỡ một phần.
  - ⚠️ **Phát hiện nặng hơn:** G04 lần 1 hỏi "khái niệm nào **không thuộc** nhóm AI phân loại?" → cả Generative AI và Agentic AI đều đúng, answer key chỉ chọn 1 → **2 đáp án đúng** (lỗi answer key, chấm tay mới thấy). Lựa chọn còn có tiền tố "A./B./C." và "Cả A và B".
- [x] **Thêm vào validator** *(18/9)*: cấm tiền tố "A./B./C./D." và lựa chọn gộp ("Cả A và B", "Cả ba…", "Tất cả các đáp án trên", "Tất cả đều đúng", "Không có đáp án nào"); lỗi in kèm lựa chọn bị bắt. Prompt luật 4 thêm: không tiền tố, không lựa chọn gộp, tránh câu phủ định. **19/19 test** (`test_validator`).
  - Lần đầu luật "đều … không" **báo nhầm** câu hợp lệ "Cả temperature và top_p đều không ảnh hưởng…" (prompt_params bị `no_evidence` 2 lần) → thu hẹp chỉ bắt "đều đúng/sai" ở cuối câu, thêm test chống báo nhầm.
  - Chạy lại `try_generate --all --level 2`: **12/12 qua validator**, 11/12 qua ngay lần đầu.
  - Ghi §9 Changelog: validator thêm kiểm lựa chọn gộp — lý do case G04 (2 đáp án đúng).
- [ ] **Giao hàm chạy thật cho D trước 14:00.** *(hàm đã chạy AI thật, chờ push + Duy nối vào API)*
- [x] ~~15:00~~ **12:25 chạy `run_eval.py` lượt 1** (25 case, `gpt-4o-mini`). Tự động: 18/18 ra câu có trích dẫn khớp · ①②③ 9/9 đúng · lộ đáp án 1/18 · chép cụm câu trích 5/18. **Chấm tay (Nam + Duy):** answer key 16/18 (89%, hụt bar dự kiến 90%) · đúng khái niệm 18/18 · đúng mức 13/18 (72%). Phân tích nháp đã có ở cuối `eval/run-1.md`. *(18/9)*
- [ ] **Nam + Duy duyệt từng dòng chấm tay** trong `eval/results/run-1.csv`, đổi `nguoi_cham` thành tên mình, chạy `python -m eval.run_eval --summarize run-1`; Nam sửa phần phân tích bằng lời của mình.
- [ ] 15:30 quay video 30 giây cùng C. **Nộp CP3.** *(nội dung form đã soạn sẵn ở `nop-cp3.md` theo run-2: 23/31 đạt; còn thiếu link video; chấm tay run-2 cần Nam/Duy duyệt; eval/ + spec.md phải push lên main trước khi nộp)*
- [x] Dọn `canvas.md`, điền bảng README (còn thiếu mã học viên của B, C, D).

### B — Tâm · Evidence + Data script
- [x] Khảo sát **≥20 người ngoài nhóm**, cần ≥50% xác nhận.
  - Dữ liệu khảo sát mẫu và file lưu trong `validation/` đã có; cần xác nhận thêm về số người thực tế và tỷ lệ xác nhận trước khi công bố final.
  - Hỏi về hành vi thật: *"Lần gần nhất tự ôn sau buổi học, bạn làm gì đầu tiên? Có biết mình đang ở mức nào không?"*
  - ⛔ Cấm hỏi *"Bạn có muốn tính năng luyện tập không?"*
  - Log nguyên văn vào `validation/survey-log.md`.
- [x] Chạy `mining.py`, lưu output vào repo (không commit CSV).
  - Có bằng chứng: `evidence/mining-report.md`.
- [x] Viết `eval/extract_cases.py`:
  - lọc lượt K4 của buổi Day01 có câu hỏi thể hiện nhầm khái niệm (từ khoá theo `concepts.json`: "khác nhau", "có phải", "là gì"…)
  - xuất `turn_id` + khái niệm + 1 câu ngắn
  - **giao D ≥12 case ứng viên trước 13:00**
  - Có bằng chứng: file `eval/extract_cases.py` và `eval/candidates.csv`.
- [x] 13:00–14:00: **điền thẳng ≥10 case chatlog vào `eval/golden.csv`** theo format D đưa (khái niệm, mức, lịch sử, hành vi mong muốn, trang đúng)
  - Có bằng chứng: `eval/golden.csv` và `eval/golden-day1.csv` đã có dữ liệu.
- [x] Chọn ≥5 ví dụ nguyên văn cho §1. Ví dụ: `T10417`, `T10427`, `T10438`, `T10455`, cộng thêm 1–2 mã khác.
  - Có bằng chứng: các mã này được nêu rõ trong `spec.md` và `eval/chatlog/tutor_turns.csv`.
- [ ] Chốt danh sách **≥5 willing users** có tên thật.
  - Chưa có bằng chứng rõ trong repo; cần xác nhận trước khi ghi vào tài liệu chính thức.

### C — Hiền · Frontend
- [ ] *(A đã làm bản nháp 12 khái niệm ở `codebase/data/concepts.json`, Hiền rà lại và chốt)* Đọc slide Day 1 → viết `concepts.json`: 8–10 khái niệm, mỗi khái niệm có `concept_id`, tên, danh sách trang, mô tả mức 1–3. **Giao cho A, B, D trước 11:00.**
- [ ] **Web: Hiền đang làm bản chính (15:15).** Bản Claude dựng lúc 14:40 chỉ giữ trên máy Nam làm tham khảo (`codebase/web/index-ban-claude.html`, không push). Bản tham khảo: `codebase/web/index.html`, mở tại `http://localhost:8000/app/` (API phục vụ luôn web). Đủ 4 màn + 4 đường đi (happy · chưa đủ dữ liệu · chưa có căn cứ/đổi khái niệm · báo câu sai/cho câu khác), loading, đo `answer_ms`, dòng phạm vi Day 1. **Đã chạy thật end-to-end trên Edge với AI thật, 0 lỗi JS.**
  - **14:55 — gắn demo vào giao diện trang chủ VLearn** (dựng lại theo ảnh chụp): menu "Luyện tập" đổi "Sắp ra mắt" → "Mới"; điểm vào ở dòng "Buổi 1: Day01", nút "Ôn nhanh", ô "Chỗ bạn đang yếu". Sau lượt luyện, ô "Chỗ bạn đang yếu" hiện chủ đề cần ôn + trang slide (thiếu dữ liệu thì không kết luận). Phần khoá học / chuỗi ngày / hoạt động là **MOCK tĩnh**, gắn nhãn DEMO. Chạy thật end-to-end trên Edge, 0 lỗi JS.
  - 📸 **Bằng chứng cho spec §1 và slide:** trang chủ VLearn thật đang có "Luyện tập — Sắp ra mắt" và "Chỗ bạn đang yếu: Chưa đo được phần nào. Làm một bài quiz để VLearn biết bạn đang ở đâu" → sản phẩm đã chừa chỗ cho đúng tính năng này nhưng chưa có.
  - Phát hiện khi chạy: (1) câu trích đôi khi **không chứng minh đáp án** (hỏi về ML nhưng trích câu "AI — chiếc ô lớn nhất") — validator chỉ kiểm câu trích có trên slide; (2) trả lời sai liên tục thì **kẹt cùng 1 khái niệm cả 5 câu** — rule "sai giữ khái niệm" chưa có giới hạn.
- [ ] ~~Dựng `codebase/web/` trên stub API~~ (yêu cầu gốc):
  - màn chọn buổi (Day 1)
  - màn câu hỏi: đề, 4 lựa chọn, `[trang N]`, thanh tiến độ 1/5, nhãn mức khó
  - màn phản hồi đúng/sai kèm giải thích và câu trích slide
  - màn kết quả: chủ đề cần ôn + `[trang N]`
- [x] Dòng giới hạn phạm vi luôn hiển thị: *"Câu hỏi chỉ lấy từ slide Day 1"* (HAX G1/G2).
- [x] Đo thời gian trả lời mỗi câu (`answer_ms`) và gửi kèm `POST /answer`.
- [ ] 14:30 chuyển từ stub sang API thật của D. 15:30 quay video cùng A.

### D — Duy · Eval (bộ đo) + Backend
- [x] Dựng API ở mục 2b (FastAPI) — `codebase/api/` (`rules.py` rule thuần + `app.py` endpoint). **25/25 test** rule + API đạt (`python -m codebase.api.test_api`). Server chạy thật: `uvicorn codebase.api.main:app --port 8000`, `/docs` OK. *(18/9)*
  - lưu session trong RAM
  - rule mức khó: đúng → +1, sai → −1, kẹp 1–3, câu 1 ở mức 2
  - chọn khái niệm tiếp theo: vừa sai thì giữ khái niệm đó, vừa đúng thì sang khái niệm chưa hỏi
  - low-confidence theo định nghĩa ở mục 1 (dưới 3 câu, hoặc ≥3 câu trả lời dưới 3 giây) → trả `not_enough_data`. API cần nhận thêm `answer_ms` từ web
- [x] Trace log: mỗi lời gọi AI ghi một dòng vào `eval/traces/*.jsonl` (`api-YYYYMMDD.jsonl`, có cả `/report`) gồm input, output, thời gian, kết quả validator (bằng chứng cho R5).
- [x] 14:00 nối hàm AI thật của A — **đã nối và chạy thử với `gpt-4o-mini`** (flow L2-01, L3-02 đạt). *(18/9)*
- [x] **Giao API thật cho C trước 14:30.** *(code xong, chờ push; hợp đồng đã cập nhật trong `codebase/CONTRACT.md`: thêm `done`, lỗi 404/409/400)*
- [x] Viết golden set **25 case** — file **`eval/golden-day1.csv`** (10 thường · 3 hiếm · 3 mỗi lớp ①②③④ · **14 case từ chatlog** có `turn_id`). *(18/9)*
  - ⚠️ **Xung đột cần nhóm quyết:** Tâm đã push `eval/golden.csv` **60 case theo 6 chủ đề rộng** (ngoài slide Day 1, 0 case chatlog, chưa có trang nguồn, không chạy tự động được). Hai bộ đang để song song, `run_eval.py` đang dùng `golden-day1.csv`.
  - Yêu cầu gốc của mục này:
  - 8–10 case thường
  - ≥2 case cho mỗi lớp ①②③④
  - 2–4 case hiếm
  - **≥10 case từ chatlog do B điền**, D viết các case còn lại và rà lại cả bộ
  - mỗi case ghi: input (khái niệm, mức, lịch sử), hành vi mong muốn, trang đúng
- [x] Viết rubric chấm tay `eval/rubric-cham-tay.md` (answer key · đúng khái niệm · đúng mức, có ví dụ Y/N, cách kiểm tra người ngoài chấm lệch ≤1/5).
- [x] Viết `eval/run_eval.py` — chạy thử AI thật 7 case OK; bắt được đúng case fail 'chiếc ô lớn nhất' mà validator bỏ sót. *(18/9)* Lệnh: `python -m eval.run_eval --label run-1`. Yêu cầu gốc: chạy cả bộ qua hàm của A, tự chấm các chiều đo được bằng code (trích dẫn khớp trang, đúng khái niệm, lộ đáp án, từ chối đúng ở ① và ③), để trống cột chấm tay, xuất bảng %. **Sẵn sàng lúc 15:00 để A chạy lượt 1.**

**Gợi ý case cho 4 lớp chỗ khó**

| Lớp | Case |
|---|---|
| ① Nguồn sự thật | Khái niệm ngoài slide Day 1 (ví dụ "problem statement" của Day 2, hay nội dung Day 3) → từ chối. LLM bịa số trang → validator bắt được |
| ② Mơ hồ | Mới có 1–2 câu → "chưa đủ dữ liệu". ≥3 câu trả lời dưới 3 giây (đoán mò) → không kết luận |
| ③ Ngoài phạm vi | Đòi đáp án luôn · dán `SYSTEM_OVERRIDE` · đòi xem điểm người khác |
| ④ Đặc thù domain | Answer key sai về quan hệ AI ⊃ ML ⊃ DL / LLM · đề lộ đáp án · hai trang cùng một khái niệm bị hỏi trùng |

---

## 4. Giai đoạn 2 · 16:00 → CP4 (21:00 · 18/9) — khoá spec

> Sau 21:00 **không sửa quality bar được nữa**. Khai phần chưa xong thì không bị trừ, giấu mới bị trừ.

### A — Nam · Vòng sửa AI + spec §4 + chốt bar
- [x] Từ `run-1.md`, sửa **2–3 nguyên nhân fail lớn nhất** (prompt, validator, cách đưa trang vào). Mỗi thay đổi ghi 1 dòng vào §9 Changelog, trỏ tới case nào.
- [x] **Sửa sau run-1 + chạy run-2 (14:51, 31 case)** *(18/9)* — chấm tay: Claude chấm nháp, Nam + Duy đã duyệt (18/9):
  - Thêm **kiểm chéo bằng AI** (giải lại câu, không biết đáp án) → chặn được case demo "AI chính" và G02. Prompt luật 11–12 (mức 3 bắt buộc tình huống; cấm lấy tiêu đề slide làm đáp án). `temperature` 0.7 → 0.5. Golden +6 case của Tâm (đổi mã T-G…, sửa cột thiếu).
  - Kết quả: answer key 16/18 → **21/21**; đúng mức 72% → **81%**; mức 3 có tình huống 1/4 → **6/6**; chép cụm 5/18 → 3/21. Đánh đổi: ra câu 100% → **88%** (3 case bị chặn — đã đọc, cả 3 chặn đúng).
  - Còn lỗi: mức 2 hay thành câu nhận biết; L4-03 vẫn chép "chiếc ô lớn nhất".
- [x] **Sửa luật chọn khái niệm (Duy) — phát hiện khi chạy app, eval không thấy** *(18/9)*: log app cho thấy 29 trang slide chỉ hỏi tới **7 trang, trang 3 chiếm 34 lần**, vì mọi lượt bắt đầu ở khái niệm đầu danh sách và sai thì kẹt mãi 1 khái niệm.
  - Sửa: (1) xáo thứ tự khái niệm mỗi lượt; (2) sai 2 lần liên tiếp cùng khái niệm thì chuyển; (3) khái niệm nhiều trang thì gợi ý AI dùng trang chưa hỏi. Test rule/API **29/29** (thêm 4 test).
  - Kiểm chứng 3 lượt AI thật: **7 khái niệm, 11 trang** (3, 4, 6, 7, 18, 19, 20, 21, 25, 26, 29); trong 1 khái niệm đổi trang (19→18, 20→21, 7→6); không còn kẹt.
  - Ghi §9 Changelog. Bài học cho reflection: golden set gọi thẳng từng khái niệm nên không lộ lỗi phân bố — phải chạy như người dùng thật.
- [x] **Đo chỗ yếu qua nhiều lượt (18:00–18:20, Claude làm, Duy + Hiền rà lại)** — chi tiết: `bao-cao-do-cho-yeu.md`
  - Backend: `codebase/api/progress.py` (hồ sơ theo mã học viên ẩn danh, file `codebase/data/progress.json` không commit), `rules.concept_status` (≥ 3 câu; sai ≥ 2/3 câu gần nhất → đang yếu), `rules.order_for_learner` (lượt sau ưu tiên đang yếu), `GET /learner/{id}/progress`, câu < 3 giây không tính. Test **41/41** (thêm 12).
  - Frontend (web của Hiền, chỉ thêm, không xoá): mã học viên, khối "Bản đồ kiến thức của bạn", nút "Ôn chỗ yếu ngay", thông báo "Lượt này ưu tiên ôn lại…", nút xem bản đồ ở màn kết quả.
  - Chạy thật Edge + AI thật: học viên mới → "Chưa đo được phần nào"; sau 1 lượt → 3/12 phần "Chưa đủ dữ liệu" (không kết luận vội); hồ sơ có phần yếu → "Ôn chỗ yếu" → câu đầu hỏi đúng phần đó. 0 lỗi JS.
  - Spec: lát cắt + non-goals (viết lại, mục cũ đang trống) + bảng thiết kế + §4b G10 + §5 (+4 kịch bản) + §6 (+1 đường đi) + §9. Canvas + CONTRACT cập nhật.
- [x] **Bản đồ trực quan hơn + ôn lại ngay (18:20–18:35)** — theo góp ý của Nam: thanh tổng quan, "Cần ôn ngay", lộ trình theo slide; màn "Ôn lại kiến thức" (câu đã sai + slide gốc); "Luyện 3 câu phần này". Test **49/49**. Chạy thật Edge + AI thật: bản đồ → ôn lại (3 câu sai thật, slide 4) → luyện 3 câu cùng khái niệm → bản đồ cập nhật; 0 lỗi JS, mobile không tràn. Sửa lỗi phát hiện khi chạy: lượt ôn riêng 1/3 lần không ra câu → thử lại chính khái niệm → 5/5.
- [x] **Ảnh slide thật khi ôn lại (18:50)**: `GET /slide/{page}.png` (vẽ từ PDF gốc, giữ trong RAM); màn ôn hiện ảnh slide + chữ thu gọn, câu trích có link nhảy tới ảnh; nút "Xem slide ↗" ở màn phản hồi. Test **52/52**. Chạy thật Edge: ảnh slide 4 hiện đủ 1536×864, 0 lỗi JS. ⚠️ Không push ảnh chụp có nội dung slide (đã cắt `docs/anh/on-lai-kien-thuc.png`, `.gitignore` chặn `docs/anh/*slide*.png`).
- [x] **Sửa mức 2 (19:30, Claude làm, Nam + Duy đã duyệt)** — prompt luật 11 + `level_guide["2"]`: cấm "mô tả → gọi tên", chỉ cho so sánh 2 khái niệm hoặc chọn phát biểu đúng có lựa chọn sai là hiểu nhầm cụ thể. Rubric mức 2 thêm ví dụ N; spec §7 dòng "Mức khó" khớp rubric; §9 thêm 1 dòng.
  - ⚠️ Đọc lại run-2 theo rubric: đúng mức thật **14/21 (67%) < bar 70%** (G05, G06, T-G53 chấm Y dễ quá). Mức 2 thật 4/11.
  - Chạy thử 14 case mức 2 (`eval/run-3-muc2.md`, không dùng làm số nộp): mức 2 thật **7/12 (58%)**, answer key 12/12, ra câu 12/13. Chưa đạt 70%.
  - Còn lại: 5/12 câu vẫn khoác tình huống rồi hỏi "loại/khái niệm nào" → đã xử lý ở dòng dưới.
- [x] **Validator chặn mức 2 dạng gọi tên (19:45, Claude làm, Nam + Duy đã duyệt)**: `validator.NAMING` + luật "4 lựa chọn chỉ là tên"; chỉ mức 2; lỗi kèm cách sửa gửi lại cho AI. Test validator **25/25** (+6), API 52/52.
  - Chạy thử 14 case mức 2 (`eval/run-4-muc2.md`, không dùng làm số nộp): đúng mức 2 **12/12**, answer key **11/12** (G07 có 2 đáp án đúng, kiểm chéo không bắt), ra câu 12/13.
  - ⚠️ Cái giá: độ trễ trung vị **7.0 s** (5/12 câu phải sinh lại). Lỗi cũ còn: câu trích khớp trang nhưng nhiều khi không chứng minh đáp án.
  - ⚠️ Cái giá độ trễ 7 s → đã xử lý ở dòng dưới.
- [x] **Giảm thời gian chờ bằng sinh sẵn (19:50, Claude làm, chờ Duy rà vì là code API)**: `create_app(prefetch=True)` bật trong `main.py`; câu đầu sinh sẵn lúc bật server, câu tiếp sinh sẵn cả 2 nhánh đúng/sai trong lúc học viên đọc; dùng chung client OpenAI. Hợp đồng API + web **không đổi**.
  - Đo AI thật: trước khi sửa chờ câu đầu 5.8–9.3 s, sau mỗi lần trả lời 3.5–8.6 s → sau khi sửa **0.0 s** (học viên đọc 8 s); học viên nhanh nhất (3 s) chờ 0.6–1.5 s. Test API **57/57** (+5).
  - Cái giá: khoảng 2 lần gọi AI mỗi câu + 12 câu lúc bật server. Mở server trước khi demo ~20 s để sinh sẵn xong.
- [x] **Giới hạn "Đổi câu khác" 2 lần mỗi lượt (19:57, Claude làm, Nam duyệt)** — Nam phát hiện: đổi không giới hạn thì lượt không bao giờ xong và học viên né câu khó. API: `rules.MAX_SKIPS`, `skips_left` trong mỗi câu, quá giới hạn → 409, trace `skip`. Web: nút "Đổi câu khác (còn n)", hết thì khoá + dòng nhắc. "Báo câu sai" không bị trừ. CONTRACT cập nhật. Test API **61/61** (+4).
  - [ ] Chưa thử trên trình duyệt thật (bấm thử: đổi 2 lần → nút khoá → vẫn trả lời và xong lượt).
- [x] **Chế độ Solo 1v1 kiểu Quizizz (20:15, Claude làm, Nam duyệt)**: đếm ngược mỗi câu 20/30/45 s theo mức, chạm là nộp, điểm 500–1000 theo tốc độ, đối thủ mô phỏng tính theo tốc độ; hết giờ → 0 điểm + API `timed_out` (không vào bản đồ). Spec thêm §4c (luật chế độ đấu) + §5 + §9; CONTRACT cập nhật. Test API **63/63**. Đã thử trên Edge (AI giả): đồng hồ, sai, hết giờ, đổi câu, đúng nhanh +961, bản đồ, mobile — đều đúng.
  - [ ] Còn mở: hồ sơ của chính học viên được gán sẵn số liệu mẫu (rating 1240, 13 trận, 8 thắng — `app.js` `loadProfile`), spec chỉ khai "người chơi khác là dữ liệu mẫu" → sửa về 0 trận hoặc ghi rõ trên giao diện.
- [x] **Chế độ đấu: đọc trước, 10 s trả lời, điểm hiện trên thanh đếm (20:20, Claude làm, Nam duyệt)** — Nam muốn 10 s/câu; đo câu thật mức 2–3 cần 25–40 s chỉ để đọc → Nam chọn kiểu Kahoot. Đã thử trên Edge (AI giả): khoá đáp án khi đọc, tự mở sau 20 s, điểm +1000 → +500 trên thanh, hết giờ +0, phím tắt, bản đồ, mobile — đều đúng. Spec §4c + §9 cập nhật.
- [x] **Chế độ đấu theo vòng kiểu Kahoot (20:30, Claude làm, Nam duyệt)**: đề trước, đếm 3-2-1 → đáp án + 10 s → cả hai chọn xong thì lộ đối thủ → tự sang câu sau 6 s (có "Tạm dừng để đọc"). Sửa lỗi: lượt "chưa đủ dữ liệu" trước đây mất tỉ số + rating. Thử đủ 5 vòng trên Edge (AI giả), 0 lỗi JS. Spec §4c + §9.
  - ⚠️ 3 s đọc đề + 10 s trả lời chặt với câu mức 2–3 (84–100 chữ) → đo tỷ lệ hết giờ khi user test.
- [x] **Chế độ đấu: bỏ nút Tạm dừng / Câu tiếp theo, tự sang câu sau 4 s (20:35, Claude làm, Nam duyệt)** — thử 5 vòng trên Edge: tự sang sau 3,9–4,0 s, 0 lỗi JS.
- [x] **run-5 — đo lại trọn bộ 31 case trên bản hiện tại (20:46–20:55, Claude chạy + chấm nháp, chờ Nam/Duy duyệt):** đạt mọi chiều của bar (ra câu 22/24 · khái niệm 22/22 · answer key 21/22 · lộ 1/22 · mức khó 22/22 · ①③ 6/6 · ② 3/3); **27/31 case đạt toàn bộ** (run-2: 23/31). Chưa đạt: G05 sai đáp án mà kiểm chéo cho qua, G07, G09, L4-03. Đã ghi `eval/run-5.md`, spec §7 + §9, `nop-cp4.md` (chuẩn đạt + kết quả + phần chưa xong). ✅ Đã push lên `anam` + `main` (commit 4fc8880).
- [x] ~~**Cần làm để có số nộp (trước CP4):**~~ → đã làm ở dòng trên (run-5). Ghi chú cũ: chạy lại toàn bộ golden set (run-3 chính thức) + chấm tay, rồi viết spec §7 theo run-3. Backlog CP6: `misconception_tags` / `wrong_option_rationales` vào trace.
- [x] **(20:40, Claude viết, Nam duyệt) spec §7 viết lại bằng số thật run-1/run-2/run-4-muc2 + sửa dòng trạng thái, §1, §4/§4b, §6, §8.** Còn lại: khảo sát thật (Tâm). ✅ Đã commit + push lên `anam` lúc 20:43 (commit 7f04500, 31 file) và **đưa vào `main` lúc 20:45** (fast-forward, không xung đột; máy không có gh nên không qua PR) (; trước đó kiểm: không lộ key, .gitignore chặn đúng data pack, test 63/63 + 25/25; thư mục `eval/traces` bị chuyển nhầm sang `eval/fixtures/traces` lúc 20:39 → đã chuyển về). — Ghi chú cũ: `spec.md` §7 vẫn là bản cũ của Tâm ("0/60 chạy, còn thiếu run_eval") → Nam/Duy viết lại theo run-1/run-2; khảo sát thật (Tâm); commit + push.
- [x] **Chốt quality bar** — **Nam chốt lúc 20:40** (spec §7 + §9), giữ nguyên ngưỡng Canvas; báo lại Duy. Bar:
  > Đạt khi ≥80% câu có trích dẫn khớp trang và đúng khái niệm · **≥90% answer key đúng** · ≤10% đề lộ đáp án · ≥70% câu đúng mức khó yêu cầu (người ngoài chấm) · 100% case ① và ③ xử lý đúng.
- [ ] Viết `spec.md` §4:
  - lát cắt, non-goals
  - automation + lý do cost-of-error
  - bảng "rule làm gì / AI làm gì"
  - bảng HAX/PAIR (cùng C). Guide yêu cầu **≥1 trong G1/G2 · bắt buộc G10 · ≥1 trong G8/G9/G11**:
    - HAX G1/G2 → dòng "Chỉ hỏi trong slide Day 1" + `[trang N]` dưới mỗi câu
    - **HAX G10 (bắt buộc)** → dưới 3 câu hoặc đoán mò thì hiện "Chưa đủ dữ liệu để đánh giá", không kết luận học viên yếu. Không có căn cứ thì không ra câu
    - HAX G11 → giải thích đúng/sai kèm câu trích slide
    - HAX G9 → nút "Báo câu sai" / "Cho tôi câu khác"
    - HAX G8 → thoát lượt bất kỳ lúc nào, không mất gì
- [ ] 20:30 ghép spec, rà cho khớp với bản build. **20:50 nộp CP4**, kèm danh sách phần còn thiếu.

### B — Tâm · Evidence + spec §1 §2 §3 §8
- [ ] Viết §1: pain, evidence A (khảo sát n/20, % xác nhận) và B (số mining, 5 ví dụ, cách đếm). Ghi rõ giới hạn của proxy "hỏi 1 lần".
- [ ] Viết §2: bảng impact ≥3 ứng viên, mỗi ứng viên có số người × tần suất × chi phí mỗi lần.

  | Ứng viên | Trạng thái |
  |---|---|
  | (a) Solo luyện tập sau buổi học | **Chọn** |
  | (b) Tutor hỏi ngược để kiểm tra hiểu (`ask_probing_question` chỉ 6/3.097 lượt K4) | Loại, ghi lý do |
  | (c) Bản đồ chỗ khó cho giảng viên | Loại, ghi lý do |
  | (d) Arena đầy đủ: rank + ghép đối thủ + bonus | Loại: 5 quyết định AI, phần lõi là Elo |

- [ ] Viết §3: 2 sản phẩm tương tự (ví dụ Duolingo, Quizlet Learn).
- [ ] Viết §8: phân công lấy theo bảng mục 2 + kế hoạch validation.
- [ ] Bắt đầu dựng khung slide.

### C — Hiền · Frontend 4 đường đi
- [ ] Hoàn thiện đủ **4 đường đi** trong UI:
  - happy
  - low-confidence: màn "Chưa đủ dữ liệu để đánh giá"
  - failure: "Chưa có căn cứ cho khái niệm này" → đổi khái niệm
  - correction: nút "Báo câu sai" + "Cho tôi câu khác"
- [ ] Trạng thái loading và báo lỗi khi API chậm.
- [ ] Đặt nhãn "Mock" rõ cho phần giả.
- [ ] Chạy end-to-end, không can thiệp tay giữa chừng.
- [ ] Viết cột "chỗ áp dụng" (màn nào, ảnh chụp) cho bảng HAX/PAIR của A.
- [ ] Viết `spec.md` §6: 4 đường đi (happy / low-confidence / failure / correction) + ③ ngoài phạm vi + ④ domain, mỗi đường trỏ vào màn và `status` cụ thể.

### D — Duy · Eval + Backend + spec §5 §7
- [ ] Backend:
  - `/report`: loại câu bị báo, ghi log, sinh câu thay thế
  - `/skip`: cùng khái niệm, cùng mức
  - LLM timeout hoặc lỗi → trả `no_evidence`, không crash
- [ ] Viết rubric chấm tay cho 2 chiều **answer key đúng** và **đúng mức khó**, kèm ví dụ đạt/không đạt. Chấm tay lượt 1 và lượt 2.
- [ ] Viết §7: định nghĩa từng chiều chất lượng đủ rõ để người ngoài nhóm chấm ra cùng kết quả. Cùng A chốt bar.
- [ ] Viết §5 (4 lớp chỗ khó, ≥8 kịch bản).

---

## 5. Giai đoạn 3 · 21:00 → CP5 (22:30 · 18/9) — nộp cuối

- [ ] **A**
  - Chạy lượt cuối (không đổi bar) → `eval/run-final.md`.
  - Viết phân tích nguyên nhân các case chưa đạt.
  - Chọn **1 case lỗi thật** để đưa lên slide.
  - Điều phối dry run lúc 22:10 và **nộp CP5**.
- [ ] **B**
  - Cho **5 người ngoài nhóm** dùng thử, trong đó có 2 người đã khai ở CP1. Giao task rồi ngồi im quan sát.
  - Ghi `validation/log.md` theo cột: ai · task · kẹt ở đâu · quote nguyên văn · quyết định. Cuối bảng viết 4 dòng: chủ đề lặp nhiều nhất · sửa gì trước demo · giữ gì và vì sao · để dành gì.
  - Hoàn thiện slide 6 trang PDF:
    1. Pain + số
    2. Lát cắt
    3. Demo
    4. **Case lỗi thật kèm % so với bar**, số liệu lấy từ A
    5. Validation
    6. Backlog: ghép đối thủ tự động, đấu realtime, rank bền vững (Elo), cùng phần mở rộng nếu chưa kịp làm
- [ ] **C** — Sửa ≥1 điểm UI dựa trên feedback của B (ghi §9 cùng A). Quay video demo dự phòng.
- [ ] **D** — Nhờ 1 người ngoài nhóm chấm lại 5 case theo rubric, ghi mức độ khớp (chứng minh định nghĩa kiểm chứng được). Sửa backend theo feedback nếu cần.

---

## 6. Giai đoạn 4 · trước 09:00 · 19/9 — thuyết trình

- [ ] Cả 4 người viết `reflection/<tên>.md`: vai trò · phần mình làm · AI hỗ trợ thế nào · 1 bài học từ case fail.
- [ ] Chia 5 phút trình bày:
  - **B:** pain + evidence
  - **A:** lát cắt + AI + case lỗi
  - **C:** demo
  - **D:** bộ đo + % so với bar
- [ ] **A** chuẩn bị 2 case lạ để chạy live khi giám khảo đưa thẻ: một khái niệm ngoài slide, một câu có prompt injection.

---

## 7. Chỗ bàn giao giữa các người (dễ tắc nhất)

| Từ → Đến | Bàn giao | Hạn |
|---|---|---|
| A ↔ C ↔ D | Chốt hợp đồng API + hàm AI (mục 2b) | 30 phút đầu |
| C → A, B, D | `concepts.json` | 11:00 |
| A → D | `pages.json` | 11:00 |
| B → D | ≥12 case ứng viên từ chatlog | 13:00 |
| B → D | ≥10 case chatlog đã điền vào `golden.csv` | 14:00 |
| A → D | `generate_question()` chạy AI thật | 14:00 |
| D → C | API thật | 14:30 |
| D → A | `golden.csv` + `run_eval.py` | 15:00 |
| B → A | §1 §2 §3 bản nháp | 19:00 |
| D ↔ A | Chốt quality bar + §5 §7 | 20:30 |
| C → A | §6 | 19:30 |
| B → A, C | Feedback user test | 21:45 |

- Ai kẹt quá 20 phút → báo A ngay.
- **14:00 mà AI chưa chạy** → C và D tạm dừng việc khác, cùng A nối lời gọi AI thật (điều kiện của CP3).

## 7b. Lịch theo giờ — ai làm gì, theo thứ tự (18/9)

> Tính từ 09:00. Bắt đầu muộn bao nhiêu thì dịch cả bảng bấy nhiêu, **trừ các mốc nộp** (16:00 · 21:00 · 22:30), không dịch được.

| Giờ | A | B | C | D |
|---|---|---|---|---|
| 09:00–09:30 | `.gitignore`, tạo thư mục · **cả nhóm chốt hợp đồng 2b** | Chốt hợp đồng 2b · soạn câu hỏi khảo sát | Chốt hợp đồng 2b | Chốt hợp đồng 2b |
| 09:30–11:00 | `pages.json` (→ D 11:00) · nháp prompt | Bắt đầu khảo sát · chạy `mining.py` | `concepts.json` (→ A, B, D 11:00) | Khung API trên hàm AI giả |
| 11:00–13:00 | `generate_question()` + validator | Khảo sát tiếp · viết `extract_cases.py` (→ D 13:00) | 4 màn trên stub API | Rule mức khó, session, trace log · chốt format `golden.csv` · viết case thường |
| 13:00–14:00 | Test hàm AI bằng script riêng, sửa · **giao D 14:00** | Điền ≥10 case chatlog vào `golden.csv` | Hoàn thiện 4 màn | Case ①②③④ · viết `run_eval.py` |
| 14:00–15:00 | Cùng D nối AI thật vào API | Khảo sát đủ 20 người | Nối API thật (14:30) | Nối AI thật · `run_eval.py` xong (→ A 15:00) |
| 15:00–16:00 | **Chạy lượt 1** → `run-1.md` · 15:30 quay video · **nộp CP3** | Làm sạch log khảo sát · chọn 5 ví dụ | Sửa UI · quay video cùng A | Chấm tay lượt 1 (answer key, mức khó) |
| 16:00–18:00 | Sửa 2–3 nguyên nhân fail lớn nhất | Viết §1 §2 | 4 đường đi + loading | `/report` `/skip` + xử lý lỗi · viết rubric chấm tay |
| 18:00–19:30 | **Chạy lượt 2** → `run-2.md` · §9 Changelog | Viết §3 §8 · nhắn lại willing users | Viết §6 (→ A 19:30) · cột HAX/PAIR | Viết §5 · định nghĩa các chiều trong §7 |
| 19:30–20:30 | Viết §4 · đề xuất con số bar | Khung slide | Test end-to-end, sửa lỗi | Chấm tay lượt 2 · **chốt bar cùng A 20:30** |
| 20:30–21:00 | Ghép spec · **nộp CP4 lúc 20:50** | Rà §1–§3 | Chụp màn cho spec | Rà §5 §7 |
| 21:00–21:45 | **Chạy lượt cuối** → `run-final.md` | **User test 5 người** | Chuẩn bị máy test, hỗ trợ B | Người ngoài chấm lại 5 case |
| 21:45–22:10 | Phân tích fail · chọn case lỗi cho slide | Xong `validation/log.md` + slide | Sửa ≥1 điểm UI · quay video dự phòng | Sửa backend theo feedback |
| 22:10–22:30 | **Dry run cả nhóm** · **nộp CP5** | Dry run | Dry run | Dry run |
| Tối 18 → 09:00 19/9 | Reflection · tập Q&A · chuẩn bị 2 case lạ | Reflection · tập Q&A | Reflection · tập Q&A | Reflection · tập Q&A |

## 8. Rủi ro lớn nhất

1. Đẩy nhầm `data/` hoặc API key lên repo public.
2. Khảo sát không đủ 20 người hoặc không có log → mất tới 6 điểm R1.
3. Chốt quality bar sau 21:00 → mất 3 điểm R4.
4. Làm phần mở rộng (mục 9) khi core chưa xong → cả hai phần đều dở, mất R4 và R5.

---

## 9. Giai đoạn mở rộng — Solo kiến thức giữa người dùng + XP + bảng xếp hạng

> **Core vẫn là lát cắt chính.** Phần này chỉ là lớp bọc bên ngoài, **không thêm quyết định AI mới**: bộ câu hỏi của trận vẫn do `generate_question()` của A sinh ra. XP, ghép trận và bảng xếp hạng đều là rule.

### 9.1 Điều kiện được mở (gate)

Chỉ bắt đầu khi **đủ cả 4 điều kiện**:
- [ ] Luồng luyện 5 câu chạy end-to-end bằng AI thật, không can thiệp tay
- [ ] Đủ 4 đường đi trong UI
- [ ] `eval/run-2.md` đã có
- [ ] Spec §1–§7 đã có bản nháp đầy đủ

| Gate đạt lúc | Làm gì |
|---|---|
| **≤ 18:00** | C + D làm mức 1 + mức 2 (mục 9.2) trong 18:00–21:00. Kịp đưa vào spec CP4 và video CP5 |
| **18:00 – 20:00** | Chỉ làm mức 1 (thách đấu qua link + XP). Bảng xếp hạng đưa vào backlog trên slide |
| **> 20:00** | **Không làm trong ngày 18/9.** Ghi thành backlog trên slide 6. Có thể làm đêm 18/9 để demo ở CP6, nhưng repo sau 22:30 không được chấm thêm |

### 9.2 Phạm vi theo mức

**Mức 1 — Thách đấu qua link (bất đồng bộ) + XP**
1. Học viên X nhập biệt danh → bấm **"Tạo thách đấu Day 1"** → hệ thống sinh **1 bộ 5 câu cố định ở mức 2**. Bộ câu dùng `generate_question()` và phải qua validator.
2. X làm 5 câu → nhận link `/challenge/{id}` → gửi cho Y.
3. Y mở link → nhập biệt danh → làm **đúng 5 câu đó**.
4. Màn kết quả trận:
   - tỉ số 2 biệt danh, người thắng
   - XP nhận được
   - **"chủ đề cần ôn" chỉ người đó thấy**
5. Hoà điểm → so tổng thời gian trả lời.

**Mức 2 — Bảng xếp hạng**
- Bảng xếp hạng **tuần**, chỉ gồm người đã **bật tham gia** (opt-in).
- Mỗi dòng chỉ hiện: biệt danh · XP tuần · số trận · số trận thắng.
- Học viên thấy **top 10 và vị trí của mình**.
- Huy hiệu hiển thị đơn giản theo mốc XP (Đồng / Bạc / Vàng). Chỉ để trang trí, không mở khoá gì.

**Luật XP (rule, ghi trong spec §4)**

| Hành động | XP |
|---|---|
| Hoàn thành 1 lượt luyện 5 câu | +10 |
| Mỗi câu đúng (luyện hoặc thách đấu) | +2 |
| Hoàn thành 1 trận thách đấu | +5 (cả hai người) |
| Thắng trận | +5 |
| Thua | **0, không trừ** |
| Gặp lại cùng một đối thủ trong 24h | Chỉ trận đầu có XP thắng (chống farm) |
| Câu bị "Báo câu sai" | Không tính cho cả hai người |

### 9.3 Người làm và việc cụ thể

C xong frontend core sớm nhất nên làm chủ phần này (full-stack, module riêng). D chỉ hỗ trợ nối vào API để không quá tải.

| Người | Việc | Ước tính |
|---|---|---|
| **C** | `codebase/api/arena.py` (module riêng, không sửa code core của D): `POST /challenge`, `GET /challenge/{id}`, `POST /challenge/{id}/submit`, `GET /leaderboard` · lưu **SQLite hoặc file JSON**, vì session trong RAM không đủ cho 2 người · màn tạo trận, làm trận, kết quả trận, bảng xếp hạng | Mức 1: ~2,5h · Mức 2: ~1,5h |
| **D** | Gắn router `arena` vào app · viết hàm tính XP + luật chống farm, kèm 5 test nhỏ | ~1h |
| **A** | Cho `generate_question()` sinh bộ 5 câu cố định cho trận (tái dùng hàm cũ, không có prompt mới) · rà để phần mở rộng không làm hỏng eval core | ~0,5h |
| **B** | Thêm 1 task thách đấu vào kịch bản user test (2 người thử đấu nhau) · thêm 1 câu khảo sát: *"XP / bảng xếp hạng có khiến bạn luyện thêm không, hay chỉ muốn thắng?"* · thêm slide backlog | ~0,5h |

**Lịch nếu gate đạt ≤ 18:00**

| Giờ | C | D | A | B |
|---|---|---|---|---|
| 18:00–19:30 | Backend `arena.py` + màn tạo/làm trận | Hàm XP + chống farm + test | Bộ 5 câu cố định cho trận | Tiếp việc core (§3 §8) |
| 19:30–20:30 | Màn kết quả trận + bảng xếp hạng | Gắn router, test 2 trình duyệt | Việc core (§4, bar) | Việc core |
| 20:30–21:00 | Sửa lỗi · C viết §6 **sau cùng**, chú ý §6 còn hạn giao A lúc 19:30 | Rà spec | Ghép spec, nộp CP4 | Rà spec |
| 21:00–21:45 | Hỗ trợ user test thách đấu | — | — | User test có task thách đấu |

⚠️ Lịch này đè lên việc core của C (§6 hạn 19:30, test end-to-end) và của D (§5 §7, chấm tay). Nếu làm mức 2 thì **§6 phải chuyển cho A viết**, C chỉ gửi ảnh chụp màn.

### 9.4 Phải sửa trong spec khi làm mở rộng (A làm, trước 21:00)

- [ ] **Lát cắt (§4) giữ nguyên.** Thêm 1 đoạn "Chế độ thách đấu: phần mở rộng, dùng lại cùng quyết định AI, không thêm quyết định AI mới".
- [x] **Sửa non-goals** để bản build không vi phạm (đã cập nhật trong `canvas.md`, cần chép sang spec §4):
  1. Không ghép đối thủ tự động và không đấu realtime. Chỉ thách đấu qua link.
  2. Không có xu, cửa hàng hay vật phẩm mua bán. XP và huy hiệu chỉ để hiển thị.
  3. Bảng xếp hạng **không hiện** tên thật, chủ đề cần ôn, câu trả lời hay điểm yếu. Chỉ gồm người opt-in, chỉ hiện XP và số trận.
  4. XP và huy hiệu **không phải** đánh giá năng lực. XP đo mức độ luyện tập, không đo mức hiểu.
  5. Trong trận thách đấu, mức khó **không thích ứng theo từng câu** (hai người phải cùng bộ câu).
- [ ] Ghi **§9 Changelog**: "Thêm thách đấu + XP + bảng xếp hạng sau khi core đạt gate lúc __:__. Lý do: [quote khảo sát / feedback]".
- [ ] Thêm vào §5 các kịch bản mới:
  - farm XP bằng 2 tài khoản
  - bảng xếp hạng làm học viên yếu nản
  - đối thủ bỏ trận giữa chừng
  - một câu trong trận bị báo sai
- [ ] **Quality bar không thêm chiều mới cho phần mở rộng.** Bộ câu của trận đi qua cùng validator, nên đã được đo trong eval core.

### 9.5 Câu trả lời chuẩn bị cho giám khảo (team VLearn chấm track A)

- *"XP có làm học viên chỉ lo thắng không?"* → Thua không bị trừ XP. Phần lớn XP đến từ việc hoàn thành và trả lời đúng, không đến từ việc thắng. Kết quả chính của mỗi trận vẫn là "chủ đề cần ôn". Bảng xếp hạng là opt-in.
- *"Bảng xếp hạng có lộ ai yếu không?"* → Chỉ hiện biệt danh, XP và số trận. Không hiện chủ đề sai.
- *"AI ở đâu trong phần đấu?"* → Không có AI mới. Phần đấu dùng lại quyết định AI của core: sinh câu hỏi bám slide có validator. XP và bảng xếp hạng là rule, nên nhóm không gọi phần này là AI.
