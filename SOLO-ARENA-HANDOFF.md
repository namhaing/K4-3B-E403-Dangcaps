# HANDOFF — VLearn Solo Arena · Nhóm 4 người · Lớp 3B

> ⚠️ **Cập nhật 18/9:** các phần sau trong file này **đã cũ**: phân công (mục 5, 9), quality bar (mục 6), định nghĩa low-confidence "trả lời cụt" (mục 7), khái niệm Day 2 trong golden set (mục 6) và lịch validation (mục 11). Bản đang dùng là `ke-hoach-nhom.md` (kế hoạch, phân công, lịch) và `canvas.md` (lát cắt, non-goals, bar dự kiến). File này chỉ còn dùng để tra **evidence, mã `T#####` và các mẹo**.

> **File này tự đứng một mình.** Đưa cho bất kỳ AI/người nào cũng đủ context để làm tiếp, không cần đọc repo đề bài.
> Cập nhật lần cuối: 17/9/2026, trước CP1.

---

## ⚠️ ĐỌC TRƯỚC KHI ĐƯA FILE NÀY CHO AI KHÁC

Dữ liệu của khoá (`data/vlearn-pack/`) **không được chia sẻ ra ngoài khoá học**. Khi làm việc với AI khác:

- ✅ Được: đưa **con số đã đếm** và **mã trích dẫn** (`T10417`, `[T01-016]`) như trong file này.
- ❌ Không: dán nguyên file `tutor_turns.csv`, dán nguyên transcript, upload data pack lên tool ngoài.
- Free tier của nhiều API **có thể dùng dữ liệu để huấn luyện** — chỉ đưa phần tối thiểu.
- Repo nộp bài là **public** → không commit data pack, không commit API key / `.env`.

---

## 1 · Bối cảnh sự kiện

| | |
|---|---|
| Sự kiện | Mini Hackathon AI — Batch 04, lớp 3B. **39 giờ** từ phát đề đến thuyết trình |
| Bản chất | *"Không phải cuộc thi code — đây là cuộc thi tư duy sản phẩm AI"* |
| Nhóm | 4 người |
| Deliverable trung tâm | `spec.md` — 45/67 điểm chấm nằm trong đó |
| Prototype | Mức Sketch / Mock / Working đều được, **bắt buộc ≥1 lời gọi AI chạy thật** |

### Lịch 6 checkpoint

| Mốc | Hạn | Cần nộp |
|---|---|---|
| CP1 | **19:30 · 17/9** | Canvas 7 dòng + đội trưởng + link repo public + khai ≥2 willing user |
| CP2 | **21:00 · 17/9** | Cho thấy luồng hoạt động (mock bấm được / sơ đồ / video) + commit đầu |
| CP3 | **16:00 · 18/9** | Video 30 giây AI chạy thật + golden set ≥20 + bảng kết quả lượt 1 có % |
| CP4 | **21:00 · 18/9** | `spec.md` chốt — **khoá quality bar**, sau giờ này không sửa được |
| CP5 | **22:30 · 18/9** | Slide 6 trang PDF + video demo dự phòng + validation. **Nộp cuối** |
| CP6 | **09:00 · 19/9** | Thuyết trình, không nộp thêm |

**Mỗi mốc 5 điểm. Đúng hạn → 5, muộn → 0, không bù được.** Đội trưởng nộp thay cả nhóm, cả 5 mốc phải dùng **cùng một mã học viên**.

### Chấm điểm — 100 điểm

| Khối | Điểm | Chấm ở đâu |
|---|---|---|
| Nộp checkpoint | 25 | 5 mốc × 5 |
| **R1 · Bằng chứng & impact** | **15** | `spec.md` §1–§2 + log khảo sát |
| **R2 · Lát cắt & thiết kế** | **15** | `spec.md` §4 |
| R3 · Chỗ khó & kịch bản | 11 | `spec.md` §5–§6 |
| **R4 · Kiểm thử** | **15** | `spec.md` §7 + `eval/` |
| R5 · Prototype chạy được | 8 | `codebase/` + demo |
| R6 · Cho người ngoài dùng thử | 8 | `validation/` — không làm thì **trần 92** |
| R7 · Quy trình & repo | 3 | cấu trúc repo |

### Cấu trúc repo bắt buộc

```
README.md          ← bảng 4 thành viên + mã HV + phần việc
canvas.md          ← nộp CP1
spec.md            ← AI Spec §1–§9
demo-slides.pdf    ← 6 trang
codebase/          ← prototype, ghi rõ phần nào mock
eval/              ← golden set + bảng kết quả TỪNG lượt chạy
validation/        ← nhật ký user test (R6)
reflection/        ← mỗi người 1 file
```

---

## 2 · Ý tưởng đã chốt

**VLearn Solo Arena** — tính năng mới trên VLearn (track A2): sau buổi học, học viên vào một lượt luyện 5 câu, AI chọn khái niệm và mức khó cho từng câu dựa trên câu trước đúng hay sai.

### Lát cắt MỘT CÂU *(không được mở rộng — xem mục 3)*

> Một học viên vừa xong buổi học, đang trong một lượt luyện 5 câu · cần câu tiếp theo vừa sức để luyện đúng chỗ còn yếu · **AI quyết định khái niệm nào trong slide buổi đó và mức khó nào cho câu tiếp theo, dựa trên việc câu vừa rồi đúng hay sai, rồi sinh câu hỏi bám đúng trang slide đó** · kết quả là câu hỏi mới kèm `[trang N]`, và cuối lượt là một chủ đề cần ôn có dẫn nguồn.

**Một quyết định AI duy nhất:** *chọn khái niệm × mức khó cho câu tiếp theo, và sinh câu hỏi có căn cứ.*

### Mức automation: Conditional

- **Tự:** chọn khái niệm + mức khó, sinh câu hỏi **khi truy được trang slide làm căn cứ**.
- **Không tự:** sinh câu về khái niệm không có trong tài liệu buổi đó · kết luận học viên yếu khi mới 1–2 câu (ghi *"chưa đủ dữ liệu"*) · xếp hạng công khai.
- **Lý do theo cost-of-error:** hạ mức oan vì chấm sai một câu thì phá đúng thứ sản phẩm đang cố tạo ra là động lực, và rất khó sửa; ra câu hơi dễ thì học viên bấm "khó hơn", mất 3 giây.

### Non-goals (≥3 — bắt buộc có trong spec §4, và bản build không được vi phạm)

1. Không ghép đối thủ thật — đối thủ trong demo là **mock có kịch bản**, khai rõ trong spec
2. Không kinh tế xu / vật phẩm / chuỗi thắng — để backlog slide 6
3. Không bảng xếp hạng công khai
4. Không rank bền vững qua nhiều trận — mỗi lượt độc lập

---

## 3 · Vì sao cắt gọn — ĐỪNG MỞ LẠI

Bản ý tưởng gốc có ranking test thích ứng + ước lượng rank + độ tin cậy + matchmaking + trận 1v1 + Win Bonus + XP/xu/huy hiệu + chống farm + rank decay. Đã cắt vì ba lý do, và **mọi AI/người làm tiếp phải giữ nguyên phạm vi này**:

| Vấn đề | Chi tiết |
|---|---|
| **5 quyết định AI, luật cho phép 1** | Rubric R2 cho 3 điểm cho "lát cắt đúng format MỘT CÂU **khớp bản build**". Đề bài ghi rõ: *"Đề càng lớn, lát cắt càng phải nhỏ."* |
| **Phần lõi không cần AI** | Ước lượng rank = **Elo** (1960). Bài test thích ứng = **IRT**, psychometrics. Ghép đối thủ = hàng đợi + dải rating. Ba thứ này là thuật toán. Giám khảo sẽ hỏi *"sao không dùng Elo?"* |
| **Gamification bị soi** | Giải track A/D do **team VLearn chấm**. Kinh tế xu sẽ bị hỏi *"cái này giúp học hay chỉ giúp thắng?"* |

**Câu trả lời chuẩn bị sẵn cho giám khảo:** *"Elo xếp hạng được, nhưng không sinh nổi một câu hỏi bám trang 17 của slide buổi này. Đó là lý do phần AI của chúng em nằm ở sinh câu hỏi có căn cứ, không nằm ở xếp hạng."*

---

## 4 · Bằng chứng đã đếm được (EVIDENCE — dùng cho spec §1)

Tất cả trên `data/vlearn-pack/chatlog/tutor_turns.csv`, 13.494 lượt hỏi-đáp thật, 1.617 học viên, 22/07→15/09/2026. `cohort_hint = K4` là 3.097 lượt của chính khoá này (448 học viên).

### Bốn cơ chế đã thiết kế sẵn nhưng bỏ trống

| Vế trong pain | Con số | Cách đếm |
|---|---|---|
| "không biết mình đang ở mức nào" | `understanding_level` có dữ liệu ở **20/13.494 lượt (0,15%)** | `df.understanding_level.notna().sum()` |
| "không biết nên ôn gì tiếp" | `suggest_next_topic` **18/13.494 (0,13%)** | `df.move_used.value_counts()` |
| "mất động lực" | `motivate` **21/13.494 (0,16%)** · `celebrate_progress` **7/13.494 (0,05%)** | như trên |
| "chỉ đọc, không có hoạt động nào" | **19 cột** chatlog, **không cột nào** ghi nhận học viên làm bài | `df.columns.tolist()` |
| Proxy rời bỏ | **114/448 học viên K4 (25,4%)** chỉ hỏi đúng 1 lần | `k4.student.value_counts()==1` |

### Bối cảnh bổ sung (dùng cho bảng impact §2 và ứng viên bị loại)

| Số | Ý nghĩa |
|---|---|
| `review_concept` **12.127/13.494 (90%)** · K4: **2.767/3.097 (89,3%)** | Tutor gần như chỉ làm một việc: giảng |
| `ask_probing_question` **28/13.494** · K4 **6/3.097 (0,19%)** | Tutor gần như không hỏi ngược |
| `give_hint` **39/13.494** · K4 **23** | Gần như không gợi ý, toàn đưa đáp án |
| `rating` K4 **12/3.097 (0,39%)** — 9 up, 3 down | Không có vòng phản hồi |
| `has_citation=False` K4 **839/3.097 (27,1%)** | 27% câu trả lời không dẫn nguồn |
| `is_preset` K4 **542/3.097**; **131/448 (29,2%)** học viên có lượt đầu là câu mẫu | Người mới không biết hỏi gì |
| Transcript: **61 hoạt động lớp** / 6 buổi, giảng viên hỏi ngược lớp **271 lần** | Trên lớp có tương tác; trong VLearn thì không |

### Mã trích dẫn dùng được trong spec / golden set

- Câu hỏi khái niệm dễ lẫn: `T10417` "LLM có phải là một dạng của Machine Learning không?" · `T10427` "chat gpt có phải llm ko" · `T10438` "Machine Learning và Deep Learning khác nhau thế nào?" · `T10455` "AI, ML và DL khác nhau thế nào?"
- Xin đáp án / nhờ làm hộ: `T10515` "đáp án câu trên" · `T11105` "hướng dẫn tôi làm bài đi, theo từng bước 1"
- Câu hỏi cụt: `T10289` · `T10318` · `T10301`
- Transcript: `[T01-016]` giảng viên nói về việc phải dừng lại tự đặt câu hỏi mới xây được lối tư duy mới · `[T03-026]` hoạt động lớp: 1 phút suy nghĩ rồi giơ tay

### Còn thiếu — PHẢI LÀM

- [ ] **Khảo sát đường A: ≥20 người ngoài nhóm, ≥50% xác nhận, log đủ câu hỏi + từng câu trả lời nguyên văn + ai trả lời.** Không có log thì không tính là bằng chứng (mất 6 điểm R1).
  - Câu hỏi đúng: *"Lần gần nhất bạn tự ôn lại sau buổi học, bạn làm gì đầu tiên? Bạn có biết mình đang ở mức nào không?"*
  - ⛔ Cấm hỏi: *"Bạn có muốn có tính năng luyện tập không?"* — ai cũng trả lời có, dữ liệu vứt đi.
- [ ] **≥3 willing user có tên thật**, đã hỏi và đồng ý cho thử ở CP5.

---

## 5 · Canvas CP1 (bản nộp)

| # | Dòng | Nội dung |
|---|---|---|
| 1 | Track + đề | **A2** · VLearn — tính năng mới: **Solo Arena**, luyện tập đúng sức sau buổi học |
| 2 | Job executor | Học viên **vừa học xong một buổi trên VLearn**, muốn tự luyện lại nhưng không biết nên luyện gì và ở mức nào |
| 3 | Pain một câu | Sau buổi học, học viên chỉ có cách đọc lại slide hoặc hỏi tutor giảng lại; không có hoạt động nào để tự kiểm, không biết mình đang ở mức nào và nên ôn gì tiếp, nên hoặc luyện thứ đã biết hoặc bỏ luôn — 1/4 học viên tương tác đúng một lần rồi không quay lại |
| 4 | Bằng chứng đầu | `understanding_level` có dữ liệu ở **20/13.494 lượt (0,15%)** · `suggest_next_topic` **18/13.494 (0,13%)** · `motivate` **21 (0,16%)** và `celebrate_progress` **7 (0,05%)** — bốn cơ chế "biết mình ở đâu / học gì tiếp / giữ động lực" đều đã được thiết kế sẵn vào tutor và bỏ trống. Trong **19 cột** chatlog không có cột nào ghi nhận học viên **làm bài** — 13.494 lượt đều là hỏi-đáp. **114/448 học viên K4 (25,4%)** chỉ hỏi một lần *(proxy cho rời bỏ)*. *Cách đếm:* `move_used.value_counts()`, `understanding_level.notna()`, `student.value_counts()==1`, lọc `cohort_hint=K4` — script `mining.py` trong repo. **+ Khảo sát:** `__/20` học viên nói lần gần nhất tự ôn sau buổi học thì không biết bắt đầu từ đâu |
| 5 | Lát cắt MỘT CÂU | Một học viên vừa xong buổi học, đang trong một lượt luyện 5 câu · cần câu tiếp theo vừa sức để luyện đúng chỗ còn yếu · AI **quyết định khái niệm nào trong slide buổi đó và mức khó nào cho câu tiếp theo, dựa trên việc câu vừa rồi đúng hay sai, rồi sinh câu hỏi bám đúng trang slide đó** · kết quả là câu hỏi mới kèm `[trang N]`, và cuối lượt là một chủ đề cần ôn có dẫn nguồn |
| 6 | AI tự làm đến đâu | **Conditional.** *Tự:* chọn khái niệm + mức khó và sinh câu hỏi khi truy được trang slide làm căn cứ. *Không tự:* sinh câu về khái niệm không có trong tài liệu buổi đó; không kết luận học viên yếu khi mới có 1–2 câu — ghi "chưa đủ dữ liệu"; không xếp hạng công khai. *Lý do cost-of-error:* hạ mức oan vì chấm sai một câu thì học viên mất đúng thứ sản phẩm đang cố tạo ra là động lực, sửa rất khó; ra câu hơi dễ thì học viên bấm "khó hơn", mất 3 giây. **Willing users:** `[Tên 1]` · `[Tên 2]` · `[Tên 3]` |
| 7 | Phân công | **Nguyễn Trần Bảo Tâm** — mining evidence + khảo sát 20 người · **Trần Thị Thu Hiền** — prototype Arena: màn 5 câu + vòng lặp đúng/sai (đối thủ và rank là **mock**) · **Bùi Phương Duy** — AI call sinh câu hỏi theo khái niệm × mức + golden set + quality bar + eval · **Nguyễn Hải Nam** — spec, canvas, slide, demo |

---

## 6 · Thiết kế kiểm thử (spec §7 + `eval/`) — 15 điểm

### Chiều chất lượng + định nghĩa kiểm chứng được

| Chiều | Định nghĩa pass/fail |
|---|---|
| **Factuality** | Mọi khái niệm trong câu hỏi trace được về **một trang slide cụ thể** hoặc **một mã đoạn transcript `[Txx-NNN]`** |
| **Relevance** | Câu hỏi đúng khái niệm đã chọn, không lạc sang khái niệm khác |
| **Không lộ đáp án** | Đề bài không chứa sẵn câu trả lời |
| **Thích ứng đúng chiều** | Câu trước SAI → câu sau dễ hơn hoặc cùng mức; câu trước ĐÚNG → câu sau khó hơn hoặc cùng mức |

### Quality bar — CHỐT TRƯỚC 21:00 18/9, SAU ĐÓ KHÔNG SỬA

> **"Đạt khi ≥80% câu hỏi sinh ra trace được về một trang slide cụ thể và đúng khái niệm đã chọn, ≤10% câu lộ đáp án ngay trong đề bài, và mức khó đổi đúng chiều so với kết quả câu trước ở ≥75% lượt."**

### Golden set ≥20 case

Cơ cấu bắt buộc: **≥2 case cho mỗi lớp chỗ khó** (8 case) + **8–10 case thường** + **2–4 case hiếm**, trong đó **≥10 case lấy hoặc phát triển từ data thật**.

Mỗi case gắn vào một tổ hợp `khái niệm × mức khó × kết quả câu trước`. Ô trống trong lưới = lỗ hổng coverage.

Nguồn khái niệm: 2 bộ slide (Day 1 AI & LLM Foundation, Day 2 Xác định bài toán — 29 trang/bộ) + 700 đoạn transcript có mã. Ưu tiên khái niệm học viên hay hỏi: **LLM vs ML vs DL** (`T10417`, `T10427`, `T10438`, `T10455`), **augment vs automate**, **problem statement**, **transformer/attention**.

> **Chia việc người–máy:** người thiết kế coverage và viết case; LLM chỉ paraphrase biến thể câu chữ. Bộ case do LLM sinh nguyên khối thường toàn happy path — 50 dòng tự sinh có khi chỉ bằng 3 case thật.

### Cách chạy và ghi kết quả

- Bảng 4 cột: `case | input | output | đạt? theo định nghĩa từng chiều`. Lưu vào `eval/`, **mỗi lượt chạy một bản ghi**, đủ **mọi** case kể cả case fail.
- Hai người chấm độc lập cùng 5 output khó rồi so. **Lệch ≥2/5 case = định nghĩa còn mơ hồ → viết lại định nghĩa**, đừng chấm tiếp.
- Nhịp lặp: `chạy trọn bộ → bảng % → chọn MỘT failure đau nhất → sửa → chạy lại TRỌN BỘ`.
- **Số xấu vẫn được đủ điểm nếu phân tích được nguyên nhân. Số bị chỉnh sửa thì không được tính.**

---

## 7 · Bốn lớp chỗ khó + kịch bản (spec §5) — cần ≥8 kịch bản

| Lớp | Cụ thể hoá cho Solo Arena |
|---|---|
| **① Nguồn sự thật** | AI sinh câu hỏi về khái niệm **không có trong slide buổi đó** → phải trace được `[trang N]`, không trace được thì không ra câu |
| **② Mơ hồ / thiếu thông tin** | Học viên trả lời cụt "chắc vậy", "ờ" → không đủ tín hiệu để chỉnh mức → giữ nguyên mức và hỏi lại, không đoán |
| **③ Ngoài phạm vi / thẩm quyền** | Học viên đòi "cho đáp án luôn", đòi xem rank người khác, đòi biết ai yếu phần nào → từ chối, vì đề bài quy định *không lộ ai hỏi gì cho người khác* |
| **④ Đặc thù domain** | AI chấm một câu đúng thành sai → hạ mức oan → phá đúng động lực mà sản phẩm đang xây. Hoặc sinh câu hỏi có kiến thức sai → học viên học sai |

Cần viết **≥8 kịch bản**, mỗi kịch bản một dòng: `tình huống cụ thể | lớp | hành vi mong muốn (nói gì, hiện gì, cho user làm gì tiếp) | nguyên tắc áp`.

Tự kiểm: **kịch bản nào làm nhóm sợ nhất khi demo?** Chưa có cái nào đáng sợ = chưa đủ hiểm.

### Bốn đường đi trải nghiệm (spec §6) — phải thể hiện được trong prototype

| Đường | Trong Solo Arena |
|---|---|
| **Happy** | Trả lời đúng → câu sau khó hơn, vẫn bám slide, có `[trang N]` |
| **Low-confidence (②)** | Tín hiệu yếu (mới 1 câu, hoặc trả lời cụt) → giữ mức, hiện *"chưa đủ dữ liệu để đánh giá"* |
| **Failure / không căn cứ (①)** | Không truy được trang slide cho khái niệm nào → không sinh câu, nói rõ *"buổi này chưa có nội dung để luyện phần đó"* |
| **Correction** | Học viên bấm **"câu này sai/không liên quan"** hoặc **"cho tôi câu khác"** → đổi câu ngay, ghi nhận |

---

## 8 · Nguyên tắc HAX/PAIR (spec §4b) — ≥4, mỗi cái trỏ vào chỗ cụ thể · 6 điểm

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G1 — Làm rõ hệ thống làm được gì** | Màn mở đầu lượt luyện: *"5 câu, lấy từ slide buổi [X]. Không chấm điểm, không ai khác thấy kết quả của bạn."* |
| **G2 — Làm rõ nó làm tốt đến đâu** | Mỗi câu hỏi hiện `[trang N]` nguồn; cuối lượt hiện độ tin cậy của nhận xét |
| **G10 — Thu hẹp phạm vi khi nghi ngờ** *(bắt buộc)* | Tín hiệu yếu → giữ nguyên mức + ghi *"chưa đủ dữ liệu để đánh giá"*, không kết luận học viên yếu |
| **G9 — Sửa dễ dàng** | Nút *"cho tôi câu khác"* / *"câu này không liên quan"* ngay dưới mỗi câu hỏi |
| **G8 — Gạt bỏ dễ dàng** | Thoát lượt luyện bất kỳ lúc nào, không mất gì |

*(Cần ≥1 nhóm khởi đầu G1/G2, bắt buộc G10, và ≥1 trong G8/G9/G11. Bảng trên đã đủ 5.)*

---

## 9 · Phân công & việc còn lại

| Người | Sở hữu | Câu giám khảo sẽ hỏi |
|---|---|---|
| **Nguyễn Trần Bảo Tâm** | Evidence: mining + khảo sát 20 người + log | *"Con số này đếm thế nào? Cho xem 5 ví dụ nguyên văn."* |
| **Trần Thị Thu Hiền** | Prototype Arena: màn 5 câu, vòng lặp đúng/sai, mock đối thủ | *"Phần nào đang mock? AI quyết định gì ở đây?"* |
| **Bùi Phương Duy** | AI call sinh câu hỏi + golden set + quality bar + eval | *"Quality bar bao nhiêu? Failure nguy hiểm nhất?"* |
| **Nguyễn Hải Nam** | Spec, canvas, slide, demo · **đội trưởng nộp form** | *"Lát cắt là gì? Vì sao chọn nó mà không chọn 2 ứng viên kia?"* |

**Vibe-coding rule:** giám khảo hỏi bất kỳ thành viên về phần có tên mình; không giải thích được → **0 điểm phần cá nhân đó**.

### Trạng thái

- [x] Chốt track A2 + ý tưởng + lát cắt
- [x] Evidence mining — 5 con số, có cách đếm
- [ ] Canvas nộp CP1 · điền 3 willing user có tên
- [ ] Repo public tên `K4-3B-<phòng>-<tênnhóm>`, **tạo mới, KHÔNG fork repo đề**
- [ ] Khảo sát 20 người + log nguyên văn
- [ ] Bảng impact ≥3 ứng viên + ứng viên đã loại *(gợi ý ứng viên loại: "tutor hỏi ngược khi học viên đưa giả thuyết" — 32 lượt có giả thuyết, 29 bị giảng lại; "điểm dừng kiểm tra hiểu bài giữa buổi cho giảng viên" — bỏ vì user là giảng viên, khó tiếp cận trong 39h)*
- [ ] §3 nghiên cứu ≥2 sản phẩm tương tự (Duolingo · Quizlet AI · Khanmigo · ChatGPT study mode) × 4 câu: flow của họ / 1 điều đáng học (quan sát cụ thể) / 1 điều đáng né / mình khác gì
- [ ] Prototype flow bấm được (CP2)
- [ ] AI call thật + golden set ≥20 + lượt đo 1 (CP3)
- [ ] Validation 5 người ngoài nhóm, 2 người đã khai từ CP1 (R6 — 8 điểm)
- [ ] `reflection/<tên>.md` mỗi người 1 file

---

## 10 · Script tái lập số liệu — `mining.py`

Đặt ở gốc repo nhóm. Chạy: `python mining.py --csv <đường dẫn tới tutor_turns.csv>`
Commit **script và output**, **không commit CSV**.

```python
import argparse, pandas as pd

p = argparse.ArgumentParser()
p.add_argument('--csv', required=True)
a = p.parse_args()

df = pd.read_csv(a.csv)
k4 = df[df.cohort_hint == 'K4']
n, nk = len(df), len(k4)
print(f"Toan file: {n} luot | K4: {nk} luot, {k4.student.nunique()} hoc vien\n")

print("== 4 co che da thiet ke san nhung bo trong ==")
u = int(df.understanding_level.notna().sum())
print(f"understanding_level co du lieu : {u}/{n} ({u/n*100:.2f}%)")
for m in ['suggest_next_topic', 'motivate', 'celebrate_progress']:
    c = int((df.move_used == m).sum())
    print(f"{m:22s}: {c}/{n} ({c/n*100:.2f}%)")

print("\n== Tutor chi lam mot viec ==")
for m in ['review_concept', 'ask_probing_question', 'give_hint', 'validate_understanding']:
    c, ck = int((df.move_used == m).sum()), int((k4.move_used == m).sum())
    print(f"{m:22s}: toan file {c}/{n} ({c/n*100:.1f}%) | K4 {ck}/{nk} ({ck/nk*100:.2f}%)")

print("\n== Khong co hoat dong nao cho hoc vien LAM ==")
print(f"19 cot: {df.columns.tolist()}")

print("\n== Proxy roi bo ==")
v = k4.student.value_counts()
print(f"Hoc vien K4 chi hoi 1 lan: {int((v==1).sum())}/{len(v)} ({(v==1).mean()*100:.1f}%)")

print("\n== Boi canh ==")
r = int(k4.rating.notna().sum())
hc = int((~k4.has_citation).sum())
print(f"K4 co rating        : {r}/{nk} ({r/nk*100:.2f}%)")
print(f"K4 khong trich dan  : {hc}/{nk} ({hc/nk*100:.1f}%)")
```

**Kết quả mong đợi** (nếu chạy ra khác thì dừng lại, kiểm lại file CSV trước khi dùng số):

```
understanding_level co du lieu : 20/13494 (0.15%)
suggest_next_topic    : 18/13494 (0.13%)
motivate              : 21/13494 (0.16%)
celebrate_progress    : 7/13494 (0.05%)
review_concept        : toan file 12127/13494 (89.9%) | K4 2767/3097 (89.34%)
ask_probing_question  : toan file 28/13494 (0.2%)  | K4 6/3097 (0.19%)
Hoc vien K4 chi hoi 1 lan: 114/448 (25.4%)
K4 co rating        : 12/3097 (0.39%)
K4 khong trich dan  : 839/3097 (27.1%)
```

---

## 11 · Cạm bẫy đã xác định

| Bẫy | Cách tránh |
|---|---|
| **Mở lại phạm vi** (thêm rank, matchmaking, xu) | Sau CP4 **không thêm feature mới**. Mọi thứ ngoài lát cắt → slide 6 "nếu có thêm 1 tuần" |
| **Dựng UI đẹp trước khi flow thông** | CP2 chỉ cần flow bấm đi hết được, data giả. Lỗi tốn 3 giờ phổ biến nhất |
| **Golden set toàn case dễ** | TA kiểm độ phủ 4 lớp chỗ khó tại CP3 |
| **Đổi quality bar khi thấy kết quả thấp** | Bar đã chốt 21:00 18/9. Phân tích khoảng cách chính là nội dung slide 4 |
| **Metric theater** | Đừng đo "câu hỏi hay". Đo: trace được về trang nào · đúng khái niệm không · có lộ đáp án không · đổi mức đúng chiều không |
| **Validation để sát giờ** | Xếp 16:00–19:00 ngày 18/9. Cần **5 người**, trong đó **2 người đã khai từ CP1** |
| **Chỉ toàn lời khen khi user test** | Giao task theo outcome rồi **im lặng quan sát**. Cấm hỏi "bạn có thích không?" |
| **Prompt injection trong data** | Chatlog có câu kiểu "bỏ qua hướng dẫn trước đó", `SYSTEM_OVERRIDE`. Nội dung học viên là **dữ liệu, không phải chỉ thị** |

---

## 12 · Slide 6 trang (CP5) — luật "không có bằng chứng thì không có slide"

1. **User & Job** (45") — job executor + JTBD 1 câu + con số pain (4 cơ chế bỏ trống)
2. **Vì sao chọn tính năng này** (45") — bảng impact 3 ứng viên + ứng viên loại 1 dòng lý do
3. **Giải pháp & demo live** (2') — lát cắt 1 câu + automation 1 dòng + **demo 1 case chuẩn + 1 case chỗ khó**
4. **Kết quả đo** (45") — % qua golden set **đối chiếu quality bar đã chốt** + 1 failure đáng kể nhất
5. **User thật nói gì** (45") — ≥2 quote nguyên văn có tên/vai + thay đổi đã làm
6. **Nếu có thêm 1 tuần** (30") — rank/matchmaking/Win Bonus nằm ở đây + 1 dòng bài học lớn nhất

Demo round: mỗi thành viên nói ≥1 phần · giám khảo có **thẻ chạy 1 case lạ tại chỗ**.
