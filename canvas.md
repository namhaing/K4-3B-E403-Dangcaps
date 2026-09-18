# Canvas CP1 — VLearn Solo Arena

**Lớp:** 3B · **Phòng:** E403 · **Cụm:** 6 · **Đội trưởng:** Nguyễn Hải Nam — MSSV `__________`


| # | Dòng | Nội dung |
|---|---|---|
| 1 | Track + đề | **A2** · VLearn — tính năng mới: **Solo Arena**, luyện tập đúng sức sau buổi học |
| 2 | Job executor (ai · đang ở đâu · làm gì) | Học viên **vừa học xong một buổi trên VLearn**, muốn tự luyện lại nhưng không biết nên luyện gì và ở mức nào |
| 3 | Pain một câu (ai – đang làm gì – vướng đâu – hậu quả) | Sau buổi học, học viên chỉ có cách đọc lại slide hoặc hỏi tutor giảng lại; không có hoạt động nào để tự kiểm, không biết mình đang ở mức nào và nên ôn gì tiếp, nên hoặc luyện thứ đã biết hoặc bỏ luôn — 1/4 học viên tương tác đúng một lần rồi không quay lại |
| 4 | 1–2 bằng chứng đầu | `understanding_level` có dữ liệu ở **20/13.494 lượt (0,15%)** · `suggest_next_topic` **18/13.494 (0,13%)** · `motivate` **21 (0,16%)** và `celebrate_progress` **7 (0,05%)** — bốn cơ chế "biết mình ở đâu / học gì tiếp / giữ động lực" đều đã được thiết kế sẵn vào tutor và bỏ trống. Trong **19 cột** chatlog không có cột nào ghi nhận học viên **làm bài** — 13.494 lượt đều là hỏi-đáp. **114/448 học viên K4 (25,4%)** chỉ hỏi một lần *(proxy cho rời bỏ)*. *Cách đếm:* `move_used.value_counts()`, `understanding_level.notna()`, `student.value_counts()==1`, lọc `cohort_hint=K4` — script `mining.py` trong repo. *Mã minh hoạ khái niệm học viên hay lẫn:* `T10417`, `T10427`, `T10438`, `T10455`. **+ Khảo sát:** `__/20` học viên nói lần gần nhất tự ôn sau buổi học thì không biết bắt đầu từ đâu |
| 5 | Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả) | Một học viên vừa xong buổi học, đang trong một lượt luyện 5 câu · cần câu tiếp theo vừa sức để luyện đúng chỗ còn yếu · hệ thống chọn khái niệm × mức khó theo câu vừa rồi đúng hay sai, rồi **AI sinh câu hỏi bám đúng trang slide của khái niệm đó trong buổi học** · kết quả là câu hỏi mới kèm `[trang N]`, và cuối lượt là một chủ đề cần ôn có dẫn nguồn; **kết quả cộng dồn qua nhiều lượt thành bản đồ "chỗ bạn đang yếu", lượt sau ưu tiên ôn đúng chỗ đó** |
| 6 | AI tự làm đến đâu + 1 dòng lý do · ≥3 willing users ngoài nhóm | **Conditional.** *AI tự:* sinh câu hỏi trắc nghiệm cho khái niệm × mức đã chọn, **chỉ khi** trích được câu nguyên văn từ trang slide làm căn cứ (code kiểm lại). *Rule làm, không giao AI:* chọn mức khó, chọn khái niệm, chấm đúng/sai theo đáp án. *AI không tự:* sinh câu về khái niệm không có trong slide buổi đó (không có căn cứ → "chưa có căn cứ", đổi khái niệm); không kết luận học viên yếu khi dưới 3 câu hoặc trả lời quá nhanh → "chưa đủ dữ liệu để đánh giá". *Lý do cost-of-error:* answer key sai thì học viên bị chấm oan, mất đúng thứ sản phẩm đang cố tạo ra là động lực, và có thể học sai kiến thức, rất khó sửa. Vì vậy chấm điểm để rule làm, còn câu hỏi AI sinh ra phải có trích dẫn. Ngược lại, câu hơi lệch mức thì học viên chỉ cần bấm "Cho tôi câu khác", mất 3 giây. **Willing users (đã hỏi và đồng ý):** `[Tên 1]` · `[Tên 2]` · `[Tên 3]` |
| 7 | Phân công có tên | **Nguyễn Hải Nam** (đội trưởng) — **AI + vòng eval**: prompt, `generate_question()`, validator bám trang slide, chạy eval từng lượt + phân tích case fail, chốt quality bar; spec §4 §9, nộp form · **Nguyễn Trần Bảo Tâm** — **evidence + data script**: `mining.py`, `extract_cases.py` lọc case từ chatlog vào golden set, khảo sát 20 người + log, user test; spec §1 §2 §3 §8, slide · **Trần Thị Thu Hiền** — **frontend**: màn luyện 5 câu, 4 đường đi (happy / chưa đủ dữ liệu / không có căn cứ / báo câu sai), `concepts.json`; spec §6, video · **Bùi Phương Duy** — **bộ đo + backend**: golden set, `run_eval.py`, rubric chấm tay, API + rule mức khó + trace log; spec §5 §7 |

## Non-goals — những thứ KHÔNG build

*(Cập nhật 18/9 cho khớp bản build — bản chi tiết ở `spec.md` §4.)*

1. Không ghép trận thật qua mạng: không tài khoản, không phòng đấu, không đấu realtime. Đối thủ 1v1 là mô phỏng.
2. Không dùng rating hay bảng xếp hạng để đánh giá năng lực học.
3. Không để AI phán học viên yếu: "đang yếu" do luật minh bạch quyết định (≥ 3 câu), AI chỉ sinh câu hỏi.
4. Không lưu danh tính: hồ sơ chỉ gắn với mã ngẫu nhiên của trình duyệt, không xem được hồ sơ người khác.
5. Không có xu, cửa hàng, vật phẩm.
6. Không sinh câu hỏi ngoài slide của buổi đang luyện (demo: Day 1).

> Phần mở rộng (thách đấu, XP, bảng xếp hạng) **chỉ làm sau khi core xong**, xem `ke-hoach-nhom.md` mục 9. Phần này không thêm quyết định AI mới.

## Quality bar dự kiến *(chốt chính thức trong `spec.md` §7 tại CP4, 21:00 18/9)*

> Đạt khi **≥80%** câu có trích dẫn khớp đúng trang slide và đúng khái niệm đã chọn · **≥90%** answer key đúng (người chấm) · **≤10%** câu lộ đáp án trong đề · **≥70%** câu đúng mức khó yêu cầu (người ngoài nhóm chấm) · **100%** case ngoài phạm vi (①, ③) được từ chối đúng.

*Đổi so với bản CP1:* bỏ chiều "mức khó đổi đúng chiều ≥75%" vì mức khó do rule quyết định nên luôn đạt 100%, không đo được gì. Thêm chiều answer key vì đây là lỗi nguy hiểm nhất.
