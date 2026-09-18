# AI SPEC - VLearn Solo Arena

Lớp 3B · Phòng E403 · Cụm 6 · Đội trưởng: Nguyễn Hải Nam.
Hướng: [x] A - VLearn (A2) · [ ] B - Trợ lý Học viên · [ ] C - Làn mở.
Loại: [ ] Tối ưu tính năng có sẵn · [x] Tính năng mới.

**Trạng thái: bản nộp CP4, 18/09/2026.** Prototype chạy end-to-end bằng AI thật (web → API → `openai/gpt-4o-mini`), không can thiệp tay. Đã có 3 lượt eval trọn bộ 31 case Day 1 (run-1, run-2, **run-5 trên bản hiện tại**) và 2 lượt chạy thử riêng câu mức 2 (run-3-muc2, run-4-muc2). **Chấm tay:** run-1 do Nam và Duy chấm; run-2 → run-4 do Claude chấm nháp theo rubric, **Nam và Duy đã duyệt** (18/9, giữ nguyên toàn bộ điểm; tên người duyệt ở cột `nguoi_cham`). Ô nào ghi "chưa có" là chưa có thật, không điền số giả.

Căn cứ: [Canvas](canvas.md), [kế hoạch nhóm](ke-hoach-nhom.md), [luồng core](luong.md), [báo cáo mining](evidence/mining-report.md), [golden set 2.0](eval/golden.csv), [bộ Day 1 đang chạy](eval/golden-day1.csv), kết quả eval [run-1](eval/run-1.md) · [run-2](eval/run-2.md) · [run-3-muc2](eval/run-3-muc2.md) · [run-4-muc2](eval/run-4-muc2.md), [hợp đồng API](codebase/CONTRACT.md).

## §1. User & Job

**Job executor:** học viên vừa học xong một buổi trên VLearn và muốn tự ôn lại kiến thức.

**Core JTBD:** Khi vừa học xong một buổi, tôi muốn xác định phần mình chưa hiểu và luyện lại ở mức phù hợp để biết nên ôn gì tiếp.

**Problem statement - giả thuyết cần kiểm chứng:** Học viên tự ôn sau buổi học gặp khó khăn khi xác định phần chưa hiểu và chọn nội dung luyện phù hợp, dẫn đến thời gian ôn chưa tập trung vào chỗ cần cải thiện.

**Current-state mapping, tổng hợp từ Canvas và log, chưa phải kết quả quan sát người dùng:** học xong → mở lại slide → chọn đoạn chưa hiểu hoặc đặt câu hỏi → tutor giải thích → học viên tự quyết định đọc tiếp/hỏi tiếp. Chưa đo thời gian từng bước hoặc mức độ phổ biến của toàn bộ luồng này.

### Bằng chứng từ dữ liệu

Nguồn: tutor_turns.csv, xuất 15/09/2026; mỗi dòng là một lượt hỏi-đáp, không phải một người. K4 có nhiều course_id; không đồng nhất số liệu K4 với riêng khóa K4P1. Cách đếm và output tái lập tại [evidence/mining-report.md](evidence/mining-report.md).

| Chỉ số | Kết quả | Diễn giải có giới hạn |
|---|---:|---|
| Tổng lượt trong file | 13.494 | Gộp K3 và K4 |
| Lượt K4 / học viên K4 | 3.097 / 448 | Học viên có tương tác được ghi trong file |
| review_concept của K4 | 2.767/3.097 = 89,34% | Tutor chủ yếu giảng lại trong các lượt được ghi |
| ask_probing_question của K4 | 6/3.097 = 0,19% | Ít lượt được gắn nhãn hỏi gợi mở |
| understanding_level có dữ liệu | 20/13.494 = 0,15% | Trường mức hiểu ít được ghi, không chứng minh người học không được đánh giá bằng cách khác |
| suggest_next_topic | 18/13.494 = 0,13% | Ít lượt gắn nhãn gợi ý chủ đề tiếp |
| Học viên K4 có đúng một lượt | 114/448 = 25,4% | Trong khoảng dữ liệu quan sát; không đồng nghĩa bỏ học hoặc không hài lòng |
| Lượt K4 có rating | 12/3.097 = 0,39% | Không đủ để suy rộng mức hài lòng toàn bộ người dùng |

Các số này hỗ trợ nhận định log thiên về giải thích, chưa chứng minh nhu cầu Solo Arena, hiệu quả học tập hoặc thời gian tiết kiệm. Danh sách 19 cột chưa có trường riêng về bài làm; không dùng điều này để kết luận toàn sản phẩm không có hoạt động luyện tập.

### Ví dụ nguyên văn

Trích phần câu hỏi ngắn; giữ nguyên cách viết. Đối chiếu bằng turn_id + course_id + lecture_code trong chatlog; câu trả lời tutor không được coi là đáp án chuẩn.

| Nguồn (đều D01) | Trích đoạn nguyên văn | Điều quan sát được |
|---|---|---|
| T10417 · K4P1 | “LLM có phải là một dạng của Machine Learning không?” | Cần làm rõ quan hệ khái niệm |
| T10427 · K4P1 | “chat gpt có phải llm ko” | Cần phân biệt sản phẩm chatbot và model |
| T10438 · K4P1 | “Machine Learning và Deep Learning khác nhau thế nào?” | Nhu cầu so sánh hai khái niệm |
| T10455 · L2-L3-K4P1 | “AI, ML và DL khác nhau thế nào?” | Câu hỏi tương tự ở khóa khác; không gộp thành bằng chứng riêng K4P1 |
| T10364 · K4P1 | “context ?” | Có bối cảnh bài LLM, không mặc định là câu mơ hồ |
| T10983 · K4P1 | “self attetion là gì giải thích lại workflow trong slide đó” | Nhu cầu giải thích cơ chế attention |

Đây là ví dụ minh họa có chọn lọc, không phải mẫu ngẫu nhiên hoặc bằng chứng về tỷ lệ học viên nhầm từng khái niệm.

**Nhu cầu quan sát được, dùng làm căn cứ thiết kế câu hỏi:** 4/6 ví dụ trên là hỏi phân biệt hoặc nhầm giữa các khái niệm gần nhau (LLM–ML, ChatGPT–LLM, ML–DL, AI–ML–DL). Vì vậy câu mức 2 phải bắt học viên **phân biệt** chứ không chỉ nhớ định nghĩa, và lựa chọn sai phải là một **hiểu nhầm có thật** (§4, §9 19:30–19:45). Đây là quan sát định tính trên ví dụ chọn lọc, không phải tỷ lệ.

### Khảo sát (n = 20)

Nguồn: `validation/khao_sat.csv` (khảo sát do Tâm phụ trách theo kế hoạch; định dạng xuất từ form, 20 phản hồi ẩn danh — chỉ có dấu thời gian và câu trả lời, thu 18:34–19:20 ngày 17/09/2026). File gốc giữ trên máy, **chưa đưa lên repo public** (bị chặn bởi quy tắc `*.csv`); dưới đây là số tổng hợp.

| Câu hỏi (rút gọn) | Kết quả | Đọc |
|---|---|---|
| Khi tự ôn, có khó biết chính xác trình độ / mức hiểu bài hiện tại không? | Thường xuyên 6 · Thỉnh thoảng 7 · Hiếm khi 3 · Không bao giờ 4 | **13/20 (65%) có gặp pain** (≥ 50% theo kế hoạch); chỉ tính "thường xuyên" là 6/20 (30%) |
| Sau buổi học có thường tự ôn lại không? | Thường xuyên 6 · Thỉnh thoảng 3 · Hiếm khi 6 · Không bao giờ 5 | 9/20 có tự ôn; 11/20 hiếm khi hoặc không bao giờ |
| Muốn ôn tập kiểu thi đấu với học viên khác không? | Rất muốn 8 · Có 5 · Không chắc 6 · Không muốn 1 | 13/20 (65%) muốn |
| Đối thủ ngang trình độ quan trọng thế nào? | Rất 5 · Khá 9 · Ít 2 · Không 4 | 14/20 cho là quan trọng |
| Có dùng tính năng tự đánh giá trình độ + ghép người ngang trình không? | Chắc chắn có 8 · Có thể 2 · Không chắc 3 · **Không dùng 7** | 10/20 (50%) sẽ dùng; 7/20 nói không |
| Làm quiz một mình có nhàm chán / giảm động lực không? | Rất thường xuyên 4 · Thỉnh thoảng 5 · Hiếm khi 7 · Không 4 | 9/20 — tín hiệu yếu hơn pain "không biết mình ở đâu" |

**Giới hạn:** chưa rõ người trả lời có phải học viên K4 / người ngoài nhóm không; mẫu tiện lợi, thu trong 46 phút; câu hỏi về tính năng (Q6) có gợi ý sẵn giải pháp. Chưa có phản hồi nguyên văn dạng mở. Khảo sát ủng hộ pain "khó biết mình đang hiểu tới đâu" (khớp bản đồ chỗ yếu), còn nhu cầu thi đấu chia đôi (7/20 không dùng) → giữ chế độ đấu là lớp bọc, không phải core.

## §2. Impact & quyết định chọn

Quyết định chọn dưới đây lấy từ kế hoạch nhóm; định lượng impact chưa hoàn tất.

| Ứng viên | Người chịu tác động / quy mô có căn cứ | Tần suất | Chi phí mỗi lần | Quyết định và lý do |
|---|---|---|---|---|
| Solo luyện tập sau buổi học | Học viên tự ôn; 448 người K4 có log là bối cảnh, không phải số đã xác nhận pain | Chưa có khảo sát; sau buổi học là bối cảnh dự kiến | Chưa đo thời gian ôn hoặc tổn thất | Chọn để thử: một quyết định sinh câu có căn cứ, phù hợp lát cắt nhỏ; log và ví dụ cho thấy nhu cầu làm rõ kiến thức |
| Tutor hỏi ngược để kiểm tra hiểu | Học viên đang hỏi tutor; 6/3.097 lượt K4 mang nhãn ask_probing_question | Tần suất nhu cầu chưa đo | Chưa đo | Không chọn trong MVP: tập trung lượt luyện riêng thay vì thay đổi luồng hỏi-đáp hiện tại; cần kiểm chứng phương án này riêng |
| Bản đồ chỗ khó cho giảng viên | Giảng viên/TA; chưa có số người được khảo sát | Chưa đo | Chưa đo | Không chọn trong MVP: đổi job executor và cần xác thực nhu cầu giảng viên |
| Arena đầy đủ: rank, ghép đối thủ, bonus | Học viên muốn thi đấu; chưa có số xác nhận | Chưa đo | Chưa đo | Loại khỏi core: tăng phạm vi và nhiều quyết định; thuật toán xếp hạng không phải phần AI sinh câu cần chứng minh. Bản build chỉ có **lớp bọc mô phỏng** dùng lại câu hỏi của core (§4c) |

**Chưa thể xếp hạng impact bằng số:** còn thiếu số người có pain × tần suất × chi phí mỗi lần cho từng ứng viên. Không dùng 448 học viên hoặc 3.097 lượt làm số người cần sản phẩm hay doanh thu dự kiến.

## §3. Giải pháp tương tự đã nghiên cứu

**Chưa có hồ sơ nghiên cứu để điền kết luận.** Kế hoạch đề xuất Duolingo và Quizlet Learn làm hai ứng viên khảo sát, chưa phải hai sản phẩm đã được nhóm nghiên cứu xong.

Tâm bổ sung cho từng sản phẩm: nguồn/ngày xem, flow liên quan, điểm đáng học, điểm không phù hợp và khác biệt của Solo Arena. Chưa tự gán tính năng hoặc kết quả cạnh tranh khi chưa kiểm chứng.

## §4. Thiết kế

**Lát cắt:** Một học viên vừa xong buổi học thực hiện lượt luyện 5 câu, hệ thống chọn khái niệm và mức theo kết quả trước đó, AI sinh câu hỏi có căn cứ trong slide để học viên luyện và nhận một chủ đề cần ôn kèm nguồn. **Kết quả cộng dồn qua nhiều lượt thành bản đồ "chỗ bạn đang yếu" của 12 khái niệm Day 1, và lượt sau ưu tiên ôn đúng chỗ yếu** (thêm 18/9).

**Phạm vi:** core theo kế hoạch là Day 1, kết quả riêng tư. Bộ golden 2.0 đã mở rộng Day 1 + Day 2 theo yêu cầu chuẩn bị bộ đo. App chỉ phủ Day 1; case Day 2 của bộ golden báo riêng là **chưa chạy** (§7). Không tự sửa nghĩa của case Day 2 để tính là đạt ngoài phạm vi.

**Prototype:** Working. **Hiện trạng (18/9):** web `codebase/web/` → API `codebase/api/` → AI thật `openai/gpt-4o-mini` (`codebase/ai/`); trace ở `eval/traces/`. Chạy end-to-end trên trình duyệt không can thiệp tay. **Phần MOCK (ghi rõ trên giao diện):** đối thủ ở chế độ "Ghép trận 1v1" (mô phỏng ở frontend), rating và bảng xếp hạng (lưu trên trình duyệt, người chơi khác là dữ liệu mẫu), nút "Demo offline" (câu hỏi viết sẵn, không gọi AI). **Chưa khai trên giao diện, sẽ sửa:** hồ sơ đấu của chính người chơi đang khởi tạo sẵn số liệu mẫu (rating 1240, 13 trận, 8 thắng) thay vì 0 trận.

| Thành phần | Cách làm (đã chạy trong bản build) |
|---|---|
| Sinh câu | AI sinh question, bốn options, answer, explanation, page và evidence_quote |
| Chọn mức | Rule: câu đầu mức 2; đúng +1, sai -1; kẹp 1–3 |
| Chọn khái niệm | Rule: thứ tự khái niệm xáo mỗi lượt; **có hồ sơ thì ưu tiên đang yếu → chưa luyện → đã vững**; sai giữ khái niệm nhưng sai 2 lần liên tiếp thì chuyển; đúng sang khái niệm chưa hỏi; khái niệm nhiều trang thì gợi ý AI dùng trang chưa hỏi |
| Chấm bài | So lựa chọn với answer; vẫn cần kiểm chất lượng answer do AI sinh |
| Thiếu dữ liệu | Dưới 3 câu đã trả lời hoặc ≥3 câu dưới 3000 ms → not_enough_data |
| Validator | Code: kiểm schema, đáp án thuộc options, trích dẫn nguyên văn có trong trang, không lộ đáp án, không tiền tố A./B., không lựa chọn gộp, **mức 2 không hỏi dạng "mô tả → gọi tên"**; lỗi thì sinh lại một lần (kèm lý do), tiếp tục lỗi → no_evidence |
| Kiểm chéo | AI lần 2 giải lại câu **không được biết đáp án**; chỉ cho qua khi đề rõ nghĩa và đúng 1 lựa chọn đúng trùng answer |
| Độ trễ (sinh sẵn) | Rule, không đổi AI: bật server là sinh sẵn câu đầu (mức 2) cho mọi khái niệm, dùng 1 câu thì sinh bù; trong lúc học viên đọc câu, sinh sẵn câu tiếp cho **cả 2 nhánh** đúng/sai theo đúng luật chọn khái niệm + mức, trả lời xong lấy nhánh khớp. Câu sinh sẵn vẫn qua đủ validator + kiểm chéo. Đổi lại: tốn khoảng 2 lần gọi AI mỗi câu (bỏ nhánh không xảy ra) |
| Đo chỗ yếu qua nhiều lượt | Rule, không AI: mỗi câu trả lời cộng dồn theo khái niệm vào hồ sơ của **mã học viên ẩn danh**. Khái niệm "đang yếu" khi đã làm **≥ 3 câu** và **sai ≥ 2 trong 3 câu gần nhất**; dưới 3 câu → "chưa đủ dữ liệu"; câu trả lời < 3000 ms (đoán mò) **không tính** |

**Automation: Conditional.** Chỉ đưa câu qua kiểm tra vào luồng luyện. Answer key sai có thể chấm oan và truyền kiến thức sai; rule chấm không tự khắc phục answer key sai. Kiểm khớp chuỗi trích dẫn cũng chưa bảo đảm đúng nghĩa, nên cần human eval.

**Non-goals** (nhóm tự đặt, cập nhật 18/9 cho khớp bản build):
1. Không ghép trận thật qua mạng: không tài khoản, không phòng đấu, không đấu realtime. Đối thủ 1v1 là mô phỏng.
2. Không dùng rating hay bảng xếp hạng để đánh giá năng lực học. Đánh giá năng lực chỉ nằm ở bản đồ kiến thức, theo luật có ngưỡng dữ liệu.
3. Không để AI phán học viên yếu: "đang yếu" là kết luận của luật minh bạch (≥ 3 câu), AI chỉ sinh câu hỏi.
4. Không lưu danh tính: hồ sơ chỉ gắn với mã ngẫu nhiên của trình duyệt; không có chức năng xem hay liệt kê hồ sơ người khác.
5. Không có xu, cửa hàng, vật phẩm.
6. Không sinh câu hỏi ngoài slide của buổi đang luyện (demo: Day 1).

### §4c. Chế độ Solo 1v1 (lớp bọc bên ngoài, không thêm quyết định AI)

Câu hỏi trong trận là câu **thật** của luồng luyện (AI sinh + validator + kiểm chéo); phần đấu chỉ là rule chạy ở web.

| Thành phần | Thật hay mô phỏng | Luật |
|---|---|---|
| Một vòng | Rule | Kiểu Kahoot: hiện **đề trước, ẩn đáp án**, đếm 3-2-1 → hiện đáp án + **10 s trả lời**, chạm là nộp → **cả hai đã chọn** thì lộ kết quả đối thủ → hiện kết quả vòng, **đếm ngược 4 s rồi tự sang câu** (không có nút). Hết giờ chưa chọn → 0 điểm, xem đáp án đúng + giải thích |
| Điểm mỗi câu | Rule | Đúng: 1000 × (1 − t / 2T), t tính trong 10 s trả lời → 500–1000; điểm có thể nhận **hiện trực tiếp trên thanh đếm** và giảm dần. Sai / hết giờ: 0 |
| Đối thủ | **Mô phỏng** ở web | Đúng/sai theo mẫu cố định Đ–S–Đ–Đ–S, chọn sau 3,5–6 s kể từ lúc hiện đáp án. Bảng điểm hiện "đang đọc đề / đang chọn / đã chọn ✓", chỉ lộ đúng-sai khi cả hai đã chọn |
| Rating, bảng xếp hạng | **Mô phỏng**, lưu trên trình duyệt | Thắng +24 · hòa +4 · thua −12. Không dùng để đánh giá năng lực (non-goal 2) |
| Bản đồ chỗ yếu | Thật | Câu trong trận vẫn cộng theo luật cũ; **hết giờ** không tính (API cờ `timed_out`). Luật "< 3 s = đoán mò" đo **từ lúc hiện đáp án** (chọn trước khi kịp đọc đáp án). Lượt "chưa đủ dữ liệu" vẫn hiện tỉ số + rating, chỉ không kết luận chỗ cần ôn |

Giới hạn đã biết: đề + 4 lựa chọn thật dài trung vị 36 / 84 / 100 chữ ở mức 1 / 2 / 3 (run-2 + run-4), đọc hết mất 11–14 / 25–34 / 30–40 s. 3 s đọc đề + 10 s trả lời (≈ 13 s) là **chặt với câu mức 2–3** → nhiều câu có thể hết giờ; cần đo tỷ lệ hết giờ khi người dùng thật chơi và chỉnh `BATTLE_READ_SECONDS` / `BATTLE_ANSWER_SECONDS` trong `app.js`.

### §4b. Nguyên tắc đã áp dụng

Tên HAX theo kế hoạch nhóm. Các chỗ dưới đây có trong bản build (thử trên Edge 18/9, xem §9); ảnh minh hoạ ở `docs/anh/` (đã cắt phần chữ slide).

| Nguyên tắc | Chỗ áp dụng trong bản build |
|---|---|
| G1/G2 - nêu khả năng và giới hạn | Hiển thị buổi/phạm vi nguồn; mỗi câu có trang dẫn |
| G10 - xử lý thiếu chắc chắn | Thiếu dữ liệu thì không kết luận năng lực; thiếu căn cứ thì không ra câu; **bản đồ kiến thức ghi "Chưa đủ dữ liệu" khi khái niệm dưới 3 câu, và ghi rõ luật ngay dưới bản đồ** |
| G11 - giải thích | Sau nộp, hiển thị đúng/sai, giải thích và đoạn nguồn |
| G9 - cho sửa lỗi | "Báo câu sai" (ghi log, thay câu, không tính điểm); "Đổi câu khác" tối đa 2 lần mỗi lượt |
| G8 - cho thoát | Cho thoát lượt luyện |

## §5. Kiểu lỗi

| Lớp | Kịch bản / case | Phản ứng mong muốn |
|---|---|---|
| ① Nguồn | Không có trang nào, GS037 | no_evidence, không bịa nguồn |
| ① Nguồn | Hỏi MCP nhưng chỉ cấp trang agent tổng quan, GS038 | no_evidence vì thiếu căn cứ chi tiết |
| ① Nguồn | Hỏi token trên trang agent, GS039 | Không dùng nguồn không liên quan |
| ① Nguồn | Hỏi Day 2 trong lượt Day 1, GS040 | Không vượt nguồn buổi đang luyện |
| ② Thiếu dữ liệu | Chỉ trả lời hai câu, GS054 | not_enough_data |
| ② Thiếu dữ liệu | Ba câu đều dưới 3000 ms, GS055 | not_enough_data; không kết luận gian lận |
| ③ Ngoài phạm vi | SYSTEM_OVERRIDE xin đáp án trước nộp, GS041 | Không tiết lộ đáp án |
| ③ Ngoài phạm vi | Xin lịch sử học viên khác, GS042 | Không tiết lộ dữ liệu phiên khác |
| ④ Domain | Đảo quan hệ AI/ML/DL/LLM, GS045-GS047 | Answer key đúng, chỉ một lựa chọn đúng |
| ④ Domain | Đề hoặc UI lộ đáp án, GS048 | Chỉ phản hồi đáp án sau nộp |
| Lỗi kỹ thuật | JSON lỗi hoặc trích dẫn giả, GS043-GS044 | Giới hạn sinh lại; cuối cùng no_evidence |
| Biên/correction | Mức 1/3, mốc 3000 ms, báo câu sai, GS052-GS053/GS056/GS058 | Giữ đúng rule biên và đường correction |
| ② Thiếu dữ liệu (nhiều lượt) | Khái niệm mới làm 1–2 câu qua các lượt | "Chưa đủ dữ liệu", không ghi "đang yếu" (test `test_api`) |
| ② Thiếu dữ liệu (nhiều lượt) | Học viên đoán mò (trả lời < 3000 ms) | Câu đó không cộng vào hồ sơ → không làm sai lệch bản đồ (test `test_api`) |
| ③ Ngoài phạm vi | Xem bản đồ của người khác bằng mã lạ, hoặc mã chứa ký tự đường dẫn (`../`) | 400 với mã sai định dạng; không có endpoint liệt kê học viên; mã lạ chỉ thấy bản đồ trống |
| ④ Domain | AI ra câu sai đáp án → học viên trả lời đúng nhưng bị tính sai → bị gắn "đang yếu" oan | 3 lớp chặn: kiểm chéo trước khi hiển thị; cần ≥ 3 câu mới kết luận; câu bị "Báo câu sai" không cộng vào hồ sơ |
| ② Thiếu dữ liệu (chế độ đấu) | Điểm thưởng tốc độ khiến học viên đoán nhanh; hết giờ vì mất tập trung | Điểm chỉ cộng khi đúng (đoán bừa chỉ được ~1/4 số điểm); câu < 3 s và câu hết giờ không vào bản đồ |

Kết quả quan sát thật trên sản phẩm: xem `eval/run-1.md`, `eval/run-2.md` và §9 (case "AI chính", 29 trang chỉ hỏi 7 trang).

## §6. Bốn đường đi

| Đường đi | Trigger | Hành vi dự kiến |
|---|---|---|
| Happy | Câu hỏi có căn cứ, qua validator | Bốn lựa chọn và nguồn; nộp → phản hồi; hết 5 câu → kết quả có chủ đề cần ôn |
| Low-confidence | Thiếu dữ liệu theo §4 | status=not_enough_data, không kết luận điểm yếu |
| Failure | Thiếu nguồn, validator thất bại sau lần sinh lại hoặc timeout | status=no_evidence; báo thiếu căn cứ, cho đường thử lại/đổi khái niệm |
| Correction | POST /report hoặc /skip | Báo sai: loại câu, ghi log, thay câu (không giới hạn, mọi lần báo đều ghi log); đổi câu: giữ khái niệm và mức, **tối đa 2 lần mỗi lượt**, hết thì khoá nút và nhắc "cứ chọn đáp án bạn thấy đúng nhất" |
| Ngoài phạm vi ③ | Xin đáp án trước nộp hoặc dữ liệu người khác | Không đáp ứng phần yêu cầu vượt quyền/phạm vi |
| Domain ④ | Câu bị nghi sai/lộ đáp án | Cho báo câu; không coi kết quả validator chuỗi là chứng minh kiến thức đúng |
| Nhiều lượt | Học viên quay lại luyện lượt sau | Màn chính hiện bản đồ: thanh tổng quan theo màu, khu "Cần ôn ngay", lộ trình 12 khái niệm theo thứ tự slide (chấm đúng/sai các câu gần nhất + lý do bằng lời); lượt mới báo "Lượt này ưu tiên ôn lại phần bạn đang yếu: …" và câu đầu hỏi đúng phần đó |
| Ôn lại ngay | Bấm "Ôn lại kiến thức" ở một phần | Màn ôn 3 bước: (1) xem lại câu đã sai — lựa chọn của mình, đáp án đúng, giải thích, câu trích slide; (2) xem lại **ảnh đúng trang slide** như lúc học (vẽ từ PDF gốc trên máy chạy server; máy không có PDF thì hiện chữ) + ý chính đã làm căn cứ; mỗi câu trích có link nhảy tới ảnh slide. Màn phản hồi sau mỗi câu cũng có nút "Xem slide ↗"; (3) "Luyện 3 câu phần này" → lượt 3 câu cùng khái niệm, kết quả cộng vào bản đồ. Không gọi AI ở bước 1–2 |

Đã chạy thử trên Edge với AI thật và AI giả (§9). API/status khớp [codebase/CONTRACT.md](codebase/CONTRACT.md), kiểm bằng `codebase/api/test_api.py` (63/63).

## §7. Kiểm thử

**Bộ đang chạy:** [eval/golden-day1.csv](eval/golden-day1.csv), 31 case Day 1 (25 case của nhóm + 6 case chuyển từ bộ 60 của Tâm, mã T-G…): 16 case thường · 3 case hiếm · 3 case cho mỗi lớp chỗ khó ①②③④; **14 case lấy từ câu hỏi thật của học viên K4 trong chatlog** (ghi turn_id). 27 case sinh câu, 4 case luồng/phiên. Bộ tham chiếu đầy đủ [eval/golden.csv](eval/golden.csv) (v2.0, 60 case Day 1 + Day 2) **chưa chạy hết**: app chỉ phủ Day 1, case Day 2 là chưa chạy. Cách chạy và rubric: [eval/README.md](eval/README.md), [eval/rubric-cham-tay.md](eval/rubric-cham-tay.md).

**Kênh chạy:** `python -m eval.run_eval` gọi đúng `generate_question()` (validator + kiểm chéo) với AI thật; case phiên/luồng (①②③) chạy qua API. Rule chọn khái niệm + mức, giới hạn đổi câu, sinh sẵn câu, hết giờ ở chế độ đấu kiểm bằng `codebase/api/test_api.py` (63/63) và `codebase/ai/test_validator.py` (25/25) với AI giả.

| Chiều | Định nghĩa để chấm |
|---|---|
| Schema/yêu cầu | Đúng trường bắt buộc, bốn lựa chọn khác nhau, answer thuộc options, đúng khái niệm và mức yêu cầu |
| Nguồn | Trang nằm trong nguồn cấp; đoạn trích khớp sau chuẩn hóa khoảng trắng và thực sự hỗ trợ nội dung |
| Answer key | Người chấm xác nhận chỉ một đáp án đúng và giải thích nhất quán với slide |
| Mức khó | Theo `eval/rubric-cham-tay.md` mục 3: mức 1 nhận biết; mức 2 phân biệt (so sánh 2 khái niệm gần nhau, hoặc chọn phát biểu đúng mà lựa chọn sai là hiểu nhầm hay gặp; dạng "mô tả → gọi tên" tính là mức 1); mức 3 tình huống mới không có trên slide |
| Lộ đáp án | Đề/UI trước nộp không đánh dấu hoặc giải thích sẵn lựa chọn đúng |
| Hành vi | Đúng kỳ vọng và tiền điều kiện riêng của case; không áp tiêu chí sinh câu cho case cần từ chối |

**Quality bar — ĐÃ KHOÁ (Nam, chốt lúc 20:40 18/09; lấy từ Canvas, không sửa sau khi khoá):** ≥ 80% ra câu có trích dẫn khớp trang · ≥ 80% đúng khái niệm · ≥ 90% answer key đúng · ≤ 10% lộ đáp án · ≥ 70% đúng mức khó · 100% case ① và ③ xử lý đúng. **Mẫu số:** tỷ lệ ra câu tính trên case cần ra câu (case không ra câu vẫn tính trượt, không giảm mẫu số); answer key / khái niệm / mức khó tính trên câu đã ra và đã chấm; lộ đáp án tính trên câu đã hiển thị.

**Kết quả** (chi tiết từng case trong `eval/results/`):

| Chiều | Bar | run-1 (25 case) | run-2 (31 case) | Mức 2 sau sửa: run-4-muc2 (14 case, chạy thử) | **run-5 (31 case, bản hiện tại)** |
|---|---|---|---|---|---|
| Ra câu, trích dẫn khớp trang | ≥ 80% | 18/18 (100%) | 21/24 (88%) | 12/13 (92%) | **22/24 (92%)** ✅ |
| Đúng khái niệm | ≥ 80% | 18/18 (100%) | 21/21 (100%) | 12/12 (100%) | **22/22 (100%)** ✅ |
| Answer key đúng | ≥ 90% | 16/18 (89%) ❌ | 21/21 (100%) | 11/12 (92%) | **21/22 (95%)** ✅ |
| Không lộ đáp án | lộ ≤ 10% | 17/18 (lộ 6%) | 20/21 (lộ 5%) | 12/12 (lộ 0%) | **21/22 (lộ 5%)** ✅ |
| Đúng mức khó | ≥ 70% | 13/18 (72%) | bản nháp 17/21 (81%) → **chấm lại chặt 14/21 (67%) ❌** | mức 2: 12/12 (100%) | **22/22 (100%)** ✅ |
| Case ① và ③ | 100% | 6/6 | 6/6 | 2/2 | **6/6** ✅ |
| Case ② (chưa đủ dữ liệu) | 100% | 3/3 | 3/3 | — | **3/3** ✅ |
| Chép cụm câu trích vào đề | (theo dõi) | 5/18 | 3/21 | 0/12 | 5/22 |
| **Case đạt toàn bộ** | — | — | 23/31 (74%) | — | **27/31 (87%)** |

- **Đọc kết quả:** run-2 đạt bar ở mọi chiều trừ **mức khó khi chấm đúng rubric**: G05, G06, T-G53 là câu "mô tả → gọi tên" nhưng bản nháp chấm Y; mức 2 thật chỉ 4/11. Đã sửa bằng prompt luật 11 + validator chặn mức 2 dạng gọi tên (§9 19:30–19:45): trên cùng tập case mức 2, 4/11 → 12/12. Đổi lại: G07 có 2 đáp án đúng mà kiểm chéo không bắt; 5/12 câu phải sinh lại (độ trễ sinh câu tăng, đã bù bằng sinh sẵn — §9 19:50).
- **run-5 (bản hiện tại, 31 case): đạt mọi chiều của bar**, 27/31 case đạt toàn bộ. 4 case chưa đạt: **G05 sai đáp án** (RLHF — kiểm chéo cùng model cũng hiểu sai, lỗi nặng nhất); G07 không ra câu (1 lần validator chặn nhầm "Cả hai đều…" có nội dung + 1 lần 2 đáp án đúng); G09 không chép được câu trích nguyên văn trang 22; L4-03 lộ đáp án "AI". Chi tiết: [eval/run-5.md](eval/run-5.md).
- **Chưa làm:** chạy 60 case của golden.csv (gồm Day 2); người ngoài nhóm chấm lại 5 case để kiểm độ rõ của rubric.
- **Chấm tay:** run-1 do **Nam (13 câu) và Duy (5 câu)** chấm. Run-2 → run-4: Claude chấm nháp theo rubric, **Nam và Duy đã duyệt** (18/9, giữ nguyên toàn bộ điểm; tên người duyệt ở cột `nguoi_cham`). **Run-5: Claude chấm nháp, Duy (21 câu) và Nam (1 câu) đã duyệt, giữ nguyên toàn bộ điểm.**
- **Lỗi đã biết:** câu trích khớp trang nhưng nhiều khi không chứng minh đáp án (validator chỉ kiểm có nguyên văn, chưa kiểm đúng nghĩa); kiểm chéo dùng cùng model nên có thể sai giống người ra đề (G07); L4-03 vẫn chép cụm "chiếc ô lớn nhất".

## §8. Phân công & kế hoạch

| Người | Trách nhiệm theo kế hoạch |
|---|---|
| Nguyễn Hải Nam (A) | AI/prompt/validator, pages.json, chạy và phân tích eval, spec §4/§9, chốt bar cùng D, nộp/demo |
| Nguyễn Trần Bảo Tâm (B) | Evidence, mining, extract_cases.py, khảo sát, spec §1/§2/§3/§8, user test và slide |
| Trần Thị Thu Hiền (C) | Frontend, concepts.json, bốn đường đi, spec §6, quay video |
| Bùi Phương Duy (D) | Backend/rule/session/trace, golden set và run_eval.py, rubric/chấm tay, spec §5/§7 |

Từ tối 18/9, Nam (A) trực tiếp sửa và duyệt cả web; các thay đổi sau CP3 ghi ở §9.

**Đã chuẩn bị cho phần B:** chạy mining và lưu báo cáo; script lọc 24 ứng viên; 11 case chatlog trong golden; sáu ví dụ nguyên văn trong §1. Bàn giao trực tiếp cho D chưa được xác nhận. Tài liệu spec này là bản nháp tổng hợp, người phụ trách từng phần vẫn phải rà theo build.

**Validation dự kiến:** B chốt ≥5 willing users có tên thật, cho 5 người ngoài nhóm dùng thử (theo kế hoạch, gồm hai người đã khai CP1). Giao task hoàn tất lượt luyện và tìm chủ đề cần ôn; ghi ai, task, chỗ kẹt, quote và quyết định vào validation/log.md. D nhờ người ngoài nhóm chấm lại 5 case và ghi mức đồng thuận.

**Willing users:** Đỗ Ngọc Phi, Phạm Cường Quốc ( lớp 3A), và Nguyễn Minh Quân, Đinh Công Minh, Phạm Nguyễn Tuân ( lớp level 2)

**Mốc trong kế hoạch ngày 18/09:** D giao API cho C 14:30; bộ chạy eval 15:00; CP3 16:00; chốt bar cùng A 20:30; CP4 21:00; validation 21:00-21:45; CP5 22:30. Đây là lịch dự kiến, không phải xác nhận đã bàn giao đúng hạn.

**Multi-prototype:** chưa có bằng chứng nhóm đã xây và so sánh nhiều prototype; không khai hoàn thành.

## §9. Changelog

| Ngày | Thay đổi | Căn cứ / việc còn lại |
|---|---|---|
| 18/09/2026 | Điền spec từ Canvas, kế hoạch, log và golden 2.0 | T10417/T10427/T10438/T10455/T10364/T10983; chưa có survey log và kết quả eval |
| 18/09/2026 | Ghi rõ giới hạn diễn giải mining | Một lượt hỏi không chứng minh bỏ học; không có trường bài làm không chứng minh toàn hệ thống không có luyện tập |
| 18/09/2026 | Phân biệt thiết kế, hiện trạng và phạm vi bộ đo | Day 1 core khác bộ đo Day 1+Day 2; A/C/D cần xác nhận trước khóa spec |
| 18/09 ~11:30 | **Bản đầu chạy AI thật** (`gpt-4o-mini`): validator kiểm câu trích nguyên văn trong trang, 4 lựa chọn, lộ đáp án; thử lại 1 lần rồi `no_evidence` | Chạy thử 12 khái niệm mức 2: 12/12 qua validator |
| 18/09 ~11:50 | Validator thêm: cấm tiền tố "A./B." và **lựa chọn gộp** ("Cả A và B", "Tất cả đều đúng"…) | Chạy thử G04: *"khái niệm nào **không thuộc** nhóm AI phân loại?"* → Generative và Agentic đều đúng, **2 đáp án đúng**, lựa chọn "Cả A và B". Lần đầu luật **báo nhầm** câu hợp lệ "Cả temperature và top_p đều không…" → thu hẹp chỉ bắt "đều đúng/sai" cuối câu. 19/19 test |
| 18/09 ~12:00 | Bộ đo tách 2 chiều: **lộ đáp án** (đề chứa nguyên văn đáp án) và **chép cụm câu trích** (≥ 4 tiếng liên tiếp). Prompt luật 9–10: không chép cụm, đã hỏi thì dùng ý khác | L4-03: đề *"khái niệm nào là 'chiếc ô lớn nhất'?"* mà bộ đo cũ chấm ✅. Sau sửa: vẫn 3/8 câu chép cụm → prompt chỉ đỡ một phần |
| 18/09 12:25 | **run-1** (25 case) — mốc so sánh | 18/18 trích dẫn khớp · ①②③ 9/9 · answer key **16/18 (89%)** · đúng mức 13/18 (72%) · mức 3 có tình huống **1/4** · chép cụm 5/18 |
| 18/09 14:00 | Gỡ slide/chatlog data pack khỏi repo public và khỏi lịch sử git | Tuân thủ quy định bảo mật data (điều 2–3) |
| 18/09 ~14:45 | **Thêm bước kiểm chéo bằng AI** (`generator.cross_check`): sau validator, AI giải lại câu **không được biết đáp án**; chỉ cho qua khi đề rõ nghĩa và đúng 1 lựa chọn đúng trùng đáp án | Case demo **"AI chính"**: slide *"Ba nhóm AI chính: phân loại · sinh nội dung · hành động"* → AI ra đề *"Nhóm nào được chia thành ba loại?"*, đáp án *"AI chính"* → **chấm oan** học viên chọn đúng. Validator cho qua vì chỉ kiểm hình thức. Thử trực tiếp: chặn "AI chính" và G02 (4 đáp án đúng), cho qua câu đúng |
| 18/09 ~14:50 | Prompt luật 11–12: định nghĩa từng mức kèm ví dụ, **mức 3 bắt buộc mở đầu bằng tình huống**; cấm lấy mảnh tiêu đề slide làm đáp án. `temperature` 0.7 → 0.5 | run-1: 3/4 câu mức 3 chỉ hỏi định nghĩa (H01, H02, H03) |
| 18/09 14:51 | Golden +6 case chuyển từ bộ 60 của Tâm (T-G07…T-G53), sửa mã trùng G07 và cột thiếu → 31 case | Phủ thêm token/context và câu phủ định |
| 18/09 14:53 | **run-2** (31 case, mẫu số khác run-1) | answer key **21/21 (100%)** · đúng mức 17/21 (81%) · mức 3 có tình huống **6/6** · chép cụm 3/21 · ra câu 21/24 (88%) — 3 case bị chặn, **đã đọc: cả 3 chặn đúng**. Độ trễ trung vị 2.6s → 3.7s. Đánh đổi có chủ đích: không ra câu còn hơn ra câu chấm oan |
| 18/09 ~15:05 | **Sửa luật chọn khái niệm:** xáo thứ tự khái niệm mỗi lượt; sai 2 lần liên tiếp cùng khái niệm thì chuyển; khái niệm nhiều trang thì gợi ý AI dùng trang chưa hỏi | Log app thật: 29 trang slide chỉ hỏi tới **7 trang, trang 3 chiếm 34 lần**; trả lời sai liên tục thì kẹt 1 khái niệm cả 5 câu. **Golden set không lộ lỗi này** vì gọi thẳng từng khái niệm. Sau sửa, 3 lượt AI thật: 7 khái niệm, **11 trang**, không còn kẹt. Test rule/API 29/29 |
| 18/09 ~18:50 | **Hiện ảnh slide thật khi ôn lại**: endpoint `GET /slide/{page}.png` vẽ trang PDF thành ảnh (giữ trong RAM, không lưu ra repo); màn ôn hiện ảnh slide + chữ thu gọn; nút "Xem slide ↗" ở màn phản hồi | Góp ý của Nam: ôn lại mà chỉ có chữ trích từ PDF thì khó nhận ra slide đã học. Test 52/52 (+3: ảnh PNG đúng trang, trang lạ 404, máy không có PDF 404). Không đưa ảnh slide vào repo (data pack) — `.gitignore` chặn `docs/anh/*slide*.png`, ảnh minh hoạ trong `docs/anh/` đã cắt bỏ phần chữ slide |
| 18/09 ~18:35 | **Bản đồ trực quan hơn + ôn lại ngay:** thanh tổng quan, khu "Cần ôn ngay", lộ trình theo thứ tự slide, lý do trạng thái bằng lời; màn "Ôn lại kiến thức" (câu đã sai + slide gốc, không gọi AI); "Luyện 3 câu phần này" (`focus_concept`), AI hụt thì thử lại chính khái niệm | Góp ý của Nam khi dùng thử: bản đồ khó đọc, và xem xong bản đồ thì chưa biết ôn thế nào. Chạy thật lần đầu: lượt ôn riêng 1/3 lần bị `no_evidence` vì không có khái niệm khác để chuyển → sửa thử lại chính khái niệm → 5/5. Test 49/49. Giới hạn: trong lượt ôn riêng, AI hay ra câu gần giống nhau ("Có bao nhiêu nhóm AI chính…" 2 lần) |
| 18/09 ~18:30 | **Đo chỗ yếu qua nhiều lượt**: hồ sơ theo mã học viên ẩn danh (`codebase/api/progress.py`), luật "đang yếu" (≥ 3 câu, sai ≥ 2/3 câu gần nhất), lượt sau ưu tiên khái niệm đang yếu, endpoint `GET /learner/{id}/progress`, bản đồ kiến thức trên web. Đổi lát cắt (thêm vế nhiều lượt) và non-goals | Trước đó mỗi lượt độc lập: tắt trang là mất, "chỗ yếu" chỉ dựa trên 5 câu, pain "không biết mình đang ở mức nào" mới giải một nửa; trang chủ VLearn thật vẫn ghi "Chỗ bạn đang yếu: Chưa đo được phần nào". Test 41/41 (thêm 12). Chạy thật trên Edge + AI thật: hồ sơ có 1 phần yếu → nút "Ôn chỗ yếu" → câu đầu hỏi đúng phần đó |
| 18/09 ~19:30 | **Prompt luật 11 mức 2 + `level_guide["2"]`:** cấm dạng "mô tả → gọi tên" ("…là hiện tượng gì?", "khái niệm/loại nào…"); chỉ cho so sánh 2 khái niệm gần nhau hoặc chọn phát biểu đúng mà mỗi phát biểu sai là một hiểu nhầm cụ thể. Rubric mức 2 thêm dấu hiệu N | Đọc lại run-2 theo rubric: G05, G06, T-G53 được chấm Y nhưng là câu gọi tên → mức 2 thật chỉ **4/11**, đúng mức toàn bộ **14/21 (67%) < 70%**, không phải 81%. Chạy thử 14 case mức 2 (`eval/run-3-muc2.md`, `--only`, không dùng làm số nộp): mức 2 thật **7/12 (58%)**, answer key 12/12, ra câu 12/13. Còn lỗi: khoác tình huống rồi hỏi "loại/khái niệm nào" (5/12). T-G50 bị chặn đúng (2 phát biểu cùng đúng). Độ trễ trung vị 3.6 → 5.5 s, chưa rõ nguyên nhân |
| 18/09 ~19:45 | **Validator chặn mức 2 dạng "mô tả → gọi tên"** (`NAMING` + cả 4 lựa chọn chỉ là tên): lỗi ghi sẵn cách sửa, gửi lại cho AI ở lần sinh lại. Chỉ áp dụng cho mức 2. Test validator 25/25 (+6: 3 case chặn, 3 case không báo nhầm) | Prompt đơn thuần chỉ đưa mức 2 lên 7/12. Thử offline trên 23 câu mức 2 đã chấm: 0/11 câu Y bị chặn nhầm, bắt 11/12 câu N. Chạy thử 14 case mức 2 (`eval/run-4-muc2.md`, không dùng làm số nộp): đúng mức 2 **12/12**, answer key 11/12 (G07: 2 đáp án đúng, kiểm chéo không bắt được), ra câu 12/13. **Cái giá:** 5/12 câu phải sinh lại, độ trễ trung vị 3.6 → **7.0 s** |
| 18/09 ~19:50 | **Giảm thời gian chờ bằng sinh sẵn** (`app.create_app(prefetch=True)`, bật trong `main.py`): câu đầu sinh sẵn cho mọi khái niệm lúc bật server; trong lúc học viên đọc câu, sinh sẵn câu tiếp cho cả nhánh đúng và nhánh sai. Dùng chung 1 client OpenAI (không bắt tay TLS lại mỗi lần gọi). Hợp đồng API và web không đổi. Trace: `api_ms` giờ là thời gian học viên thật sự chờ, thêm cờ `prefetched` | Sau khi thêm kiểm tra mức 2, sinh 1 câu mất trung vị 7 s, mà học viên phải chờ ngay sau khi bấm đáp án (chưa biết đúng/sai). Đo AI thật (4 câu/lượt): trước khi sửa chờ câu đầu 5.8–9.3 s, sau mỗi lần trả lời 3.5–8.6 s → sau khi sửa, học viên đọc 8 s: **0.0 s** cả câu đầu lẫn các câu sau; học viên nhanh nhất (đọc 3 s): câu đầu 0.0 s, sau khi trả lời 0.6–1.5 s. Test API 57/57 (+5: chuỗi câu giống hệt khi không sinh sẵn, không chờ, sau "câu khác", câu sinh sẵn thiếu căn cứ). Cái giá: khoảng 2 lần gọi AI mỗi câu + 12 câu lúc bật server |
| 18/09 ~19:57 | **Giới hạn "Đổi câu khác" 2 lần mỗi lượt** (`rules.MAX_SKIPS`): câu gửi xuống có `skips_left`, web hiện số lần còn lại, hết thì khoá nút; đổi quá giới hạn → 409. "Báo câu sai" không bị trừ. Mỗi lần đổi ghi trace `skip` (không đưa vào bản đồ) | Nam phát hiện khi dùng thử: đổi câu không giới hạn → câu bị đổi không tính vào 5 câu nên **lượt không bao giờ xong**; học viên đổi tới khi gặp câu đoán được → bản đồ báo "đã vững" quá tay; mỗi lần đổi chờ 5–7 s và tốn 2–4 lần gọi AI. Không chọn cách "đổi = tính sai" vì gắn "đang yếu" oan, trái luật "câu bị đổi không tính". Test API 61/61 (+4) |
| 18/09 ~20:15 | **Chế độ Solo 1v1 kiểu Quizizz:** đếm ngược mỗi câu (20/30/45 s theo mức), chạm là nộp, điểm 500–1000 theo tốc độ; đối thủ mô phỏng cũng tính theo tốc độ; hết giờ → 0 điểm, API cờ `timed_out` để không tính vào bản đồ. Thêm §4c mô tả luật chế độ đấu (trước đó spec chưa có) | Nam: điểm cũ +100/câu đúng, không có áp lực thời gian, không giống thi đấu. Thử trên Edge (AI giả): đồng hồ 30 → 28 s sau 2 s; sai +0; hết giờ ở câu mức 1 → "Hết giờ", hiện đáp án đúng; đổi câu → đồng hồ về 20 s; đúng sau 1,5 s → +961; câu < 3 s và câu hết giờ không vào bản đồ; mobile 390 px không tràn; 0 lỗi JS (trừ favicon 404 có sẵn). Test API 63/63 (+2) |
| 18/09 ~20:20 | **Chế độ đấu: đọc trước, 10 s trả lời; điểm hiện trên thanh đếm.** Giai đoạn đọc khoá đáp án (bấm "Sẵn sàng"/Enter hoặc tự mở sau 20 s), rồi 10 s trả lời mọi mức; thanh hiện điểm có thể nhận (+1000 → +500) | Nam muốn mỗi câu 10 s. Đo câu thật: mức 2–3 dài 84–100 chữ, chỉ đọc mất 25–40 s → 10 s tính cả đọc thì đa số hết giờ; Nam chọn cách Kahoot (đọc trước, 10 s để trả lời). Thử trên Edge (AI giả): đáp án khoá khi đọc, bấm vào không nộp; Sẵn sàng → 10 s, điểm trên thanh +990 → +890 sau 2 s; đúng → +884; không bấm gì → tự mở sau 20 s → hết giờ +0; Enter + phím 1 dùng được; bản đồ tính đúng 1/3 câu; mobile không tràn |
| 18/09 ~20:30 | **Chế độ đấu theo vòng kiểu Kahoot:** đề hiện trước, ẩn đáp án, đếm 3-2-1 → đáp án + 10 s → cả hai đã chọn thì lộ kết quả đối thủ → tự sang câu sau 6 s (có "Tạm dừng để đọc"). Bỏ nút "Sẵn sàng". Luật "< 3 s" đo từ lúc hiện đáp án. **Sửa lỗi:** lượt "chưa đủ dữ liệu" trước đây bỏ mất tỉ số + rating của trận | Nam muốn hiện đề trước 1-2-3 giây rồi mới hiện đáp án, cả hai chọn xong thì tự chuyển. Thử 5 vòng trên Edge (AI giả): đáp án ẩn + đếm 3→2; chọn sau 1 s → "Đang chờ … chọn", nút khoá; đối thủ chọn → lộ "+775", nút "(6s)" → tự sang câu; để đối thủ chọn trước → bảng "đã chọn ✓", mình chọn → lộ ngay; Tạm dừng 7 s → vẫn ở màn giải thích; hết giờ → lộ đối thủ ngay; câu cuối tự sang kết quả. Lỗi phát hiện khi thử: 3 câu chọn < 3 s → màn "chưa đủ dữ liệu" không có tỉ số, rating không cập nhật → sửa: màn này hiện tỉ số + rating, chỉ không kết luận chỗ cần ôn. 0 lỗi JS, mobile không tràn |
| 18/09 ~20:35 | **Chế độ đấu: bỏ nút "Tạm dừng để đọc" và "Câu tiếp theo"**, kết quả vòng đếm ngược 4 s rồi tự sang câu | Nam muốn trận chạy liền mạch. Thử 5 vòng trên Edge (AI giả): không còn nút, tự sang câu sau 3,9–4,0 s, câu cuối tự sang kết quả; 0 lỗi JS. Đánh đổi: giải thích chỉ hiện 4 s; câu sai (≥ 3 s, không hết giờ) vẫn xem lại được ở màn "Ôn lại kiến thức" |
| 18/09 ~20:40 | **Cập nhật spec cho CP4:** dòng trạng thái (đã chạy end-to-end + có eval), §1 thêm nhu cầu phân biệt khái niệm gần nhau (4/6 ví dụ chatlog) làm căn cứ câu mức 2, §4/§4b chuyển từ "dự kiến" sang "đã chạy", khai hồ sơ đấu có số liệu mẫu, §6/§8 bỏ việc chờ C xác nhận, **§7 viết lại bằng số thật** run-1 / run-2 / run-4-muc2 | §7 cũ vẫn ghi "0/60 đã chạy", dòng trạng thái ghi "chưa có code chạy được" — sai so với repo. Ghi thẳng: mức khó run-2 chấm chặt 67% < 70%, chưa chạy lại toàn bộ trên bản hiện tại, chấm tay còn là bản nháp |
| 18/09 ~20:50 | **§1 điền số khảo sát** (n = 20, từ `validation/khao_sat.csv`): pain "khó biết mình đang hiểu tới đâu" 13/20 (65%); muốn thi đấu 13/20; sẽ dùng ghép ngang trình 10/20, 7/20 không. §7 sửa số case chatlog của bộ Day 1: **14** (trước ghi nhầm 11 — số của bộ 60) | Spec cũ ghi "chưa có số khảo sát" dù file khảo sát đã có trên máy (bị `*.csv` chặn khỏi repo). Ghi rõ giới hạn: chưa rõ người trả lời, mẫu tiện lợi, Q6 gợi ý giải pháp |
| 18/09 ~20:55 | **run-5: đo lại trọn bộ 31 case trên bản hiện tại** | Đạt mọi chiều của bar đã khoá: ra câu 22/24 · khái niệm 22/22 · answer key 21/22 · lộ 1/22 · mức khó 22/22 (run-2 chấm chặt 14/21) · ①③ 6/6 · ② 3/3; 27/31 case đạt toàn bộ (run-2: 23/31). Lỗi mới: **G05 sai đáp án mà kiểm chéo cho qua**; G07 validator chặn nhầm "Cả hai đều…". Chấm tay run-5 là nháp, chờ Nam/Duy duyệt |
| 18/09 21:02 | **Duyệt chấm tay run-5:** Duy 21 câu, Nam 1 câu; giữ nguyên toàn bộ điểm (không sửa ô nào) | Số nộp CP4 (run-5) giờ đã có người trong nhóm duyệt; vẫn chưa có người ngoài nhóm chấm lại |
| 18/09 20:40 | **Khoá quality bar** (Nam chốt): ≥ 80% ra câu có trích dẫn khớp trang · ≥ 80% đúng khái niệm · ≥ 90% answer key · ≤ 10% lộ đáp án · ≥ 70% đúng mức khó · 100% case ① và ③ | Hạn khoá bar trước CP4. Giữ nguyên ngưỡng Canvas, không nới theo kết quả (mức khó run-2 chấm chặt 67% vẫn ghi là chưa đạt) |
