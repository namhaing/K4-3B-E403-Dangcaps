# AI SPEC - VLearn Solo Arena

Lớp 3B · Phòng E403 · Cụm 6 · Đội trưởng: Nguyễn Hải Nam.
Hướng: [x] A - VLearn (A2) · [ ] B - Trợ lý Học viên · [ ] C - Làn mở.
Loại: [ ] Tối ưu tính năng có sẵn · [x] Tính năng mới.

**Trạng thái: bản nháp ngày 18/09/2026, chưa xác nhận nộp CP4 hoặc khóa quality bar.** Phần thiết kế mô tả hành vi dự kiến, không chứng minh đã triển khai. Repo hiện có bộ đo và dữ liệu; chưa có code API/web/AI chạy được hoặc kết quả eval.

Căn cứ: [Canvas](canvas.md), [kế hoạch nhóm](ke-hoach-nhom.md), [luồng core](luong.md), [báo cáo mining](evidence/mining-report.md), [golden set 2.0](eval/golden.csv).

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

### Khảo sát còn cần đưa vào hồ sơ

Tâm đã đánh dấu hoàn thành khảo sát trong kế hoạch. Chưa có validation/survey-log.md trong repo để đối chiếu, nên **chưa ghi số người xác nhận hoặc tỷ lệ**. Cần bổ sung n người ngoài nhóm, số xác nhận pain, câu hỏi đã dùng và phản hồi nguyên văn. Mục tiêu kế hoạch là ≥20 người và kiểm tra ngưỡng ≥50%; đây chưa phải kết quả thực tế.

## §2. Impact & quyết định chọn

Quyết định chọn dưới đây lấy từ kế hoạch nhóm; định lượng impact chưa hoàn tất.

| Ứng viên | Người chịu tác động / quy mô có căn cứ | Tần suất | Chi phí mỗi lần | Quyết định và lý do |
|---|---|---|---|---|
| Solo luyện tập sau buổi học | Học viên tự ôn; 448 người K4 có log là bối cảnh, không phải số đã xác nhận pain | Chưa có khảo sát; sau buổi học là bối cảnh dự kiến | Chưa đo thời gian ôn hoặc tổn thất | Chọn để thử: một quyết định sinh câu có căn cứ, phù hợp lát cắt nhỏ; log và ví dụ cho thấy nhu cầu làm rõ kiến thức |
| Tutor hỏi ngược để kiểm tra hiểu | Học viên đang hỏi tutor; 6/3.097 lượt K4 mang nhãn ask_probing_question | Tần suất nhu cầu chưa đo | Chưa đo | Không chọn trong MVP: tập trung lượt luyện riêng thay vì thay đổi luồng hỏi-đáp hiện tại; cần kiểm chứng phương án này riêng |
| Bản đồ chỗ khó cho giảng viên | Giảng viên/TA; chưa có số người được khảo sát | Chưa đo | Chưa đo | Không chọn trong MVP: đổi job executor và cần xác thực nhu cầu giảng viên |
| Arena đầy đủ: rank, ghép đối thủ, bonus | Học viên muốn thi đấu; chưa có số xác nhận | Chưa đo | Chưa đo | Loại khỏi core: tăng phạm vi và nhiều quyết định; thuật toán xếp hạng không phải phần AI sinh câu cần chứng minh |

**Chưa thể xếp hạng impact bằng số:** còn thiếu số người có pain × tần suất × chi phí mỗi lần cho từng ứng viên. Không dùng 448 học viên hoặc 3.097 lượt làm số người cần sản phẩm hay doanh thu dự kiến.

## §3. Giải pháp tương tự đã nghiên cứu

**Chưa có hồ sơ nghiên cứu để điền kết luận.** Kế hoạch đề xuất Duolingo và Quizlet Learn làm hai ứng viên khảo sát, chưa phải hai sản phẩm đã được nhóm nghiên cứu xong.

Tâm bổ sung cho từng sản phẩm: nguồn/ngày xem, flow liên quan, điểm đáng học, điểm không phù hợp và khác biệt của Solo Arena. Chưa tự gán tính năng hoặc kết quả cạnh tranh khi chưa kiểm chứng.

## §4. Thiết kế

**Lát cắt:** Một học viên vừa xong buổi học thực hiện lượt luyện 5 câu, hệ thống chọn khái niệm và mức theo kết quả trước đó, AI sinh câu hỏi có căn cứ trong slide để học viên luyện và nhận một chủ đề cần ôn kèm nguồn.

**Phạm vi:** core theo kế hoạch là Day 1, kết quả riêng tư. Bộ golden 2.0 đã mở rộng Day 1 + Day 2 theo yêu cầu chuẩn bị bộ đo. Chưa có quyết định triển khai Day 2 trong app: phải đồng bộ trước khi khóa spec, hoặc báo riêng case Day 2 chưa chạy. Không tự sửa nghĩa của case Day 2 để tính là đạt ngoài phạm vi.

**Prototype nhắm tới:** Working, theo luong.md. **Hiện trạng kiểm chứng:** chưa có app hoặc lời gọi AI thật trong repo; không đánh dấu Working đã đạt. Bất kỳ phần stub/mock nào khi dựng phải được ghi rõ.

| Thành phần | Cách làm dự kiến |
|---|---|
| Sinh câu | AI sinh question, bốn options, answer, explanation, page và evidence_quote |
| Chọn mức | Rule: câu đầu mức 2; đúng +1, sai -1; kẹp 1–3 |
| Chọn khái niệm | Sai giữ khái niệm; đúng sang khái niệm chưa hỏi |
| Chấm bài | So lựa chọn với answer; vẫn cần kiểm chất lượng answer do AI sinh |
| Thiếu dữ liệu | Dưới 3 câu đã trả lời hoặc ≥3 câu dưới 3000 ms → not_enough_data |
| Validator | Kiểm schema, đáp án thuộc options và trích dẫn có trong trang; lỗi thì sinh lại một lần, tiếp tục lỗi → no_evidence |

**Automation: Conditional.** Chỉ đưa câu qua kiểm tra vào luồng luyện. Answer key sai có thể chấm oan và truyền kiến thức sai; rule chấm không tự khắc phục answer key sai. Kiểm khớp chuỗi trích dẫn cũng chưa bảo đảm đúng nghĩa, nên cần human eval.

**Non-goals:** không ghép đối thủ tự động/đấu realtime; không rank năng lực bền vững; không xu/cửa hàng; không công khai điểm yếu; không sinh câu ngoài nguồn buổi đang luyện. Thách đấu, XP và bảng xếp hạng chỉ là backlog sau core.

### §4b. Nguyên tắc dự kiến áp dụng

Tên HAX theo kế hoạch nhóm. Đây là ánh xạ thiết kế, chưa có ảnh giao diện chứng minh đã áp dụng.

| Nguyên tắc | Chỗ áp dụng dự kiến |
|---|---|
| G1/G2 - nêu khả năng và giới hạn | Hiển thị buổi/phạm vi nguồn; mỗi câu có trang dẫn |
| G10 - xử lý thiếu chắc chắn | Thiếu dữ liệu thì không kết luận năng lực; thiếu căn cứ thì không ra câu |
| G11 - giải thích | Sau nộp, hiển thị đúng/sai, giải thích và đoạn nguồn |
| G9 - cho sửa lỗi | Báo câu sai, đổi câu; ghi log và thay câu |
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

Chưa có case nào được quan sát trượt trên sản phẩm; đây là rủi ro và kỳ vọng kiểm thử.

## §6. Bốn đường đi

| Đường đi | Trigger | Hành vi dự kiến |
|---|---|---|
| Happy | Câu hỏi có căn cứ, qua validator | Bốn lựa chọn và nguồn; nộp → phản hồi; hết 5 câu → kết quả có chủ đề cần ôn |
| Low-confidence | Thiếu dữ liệu theo §4 | status=not_enough_data, không kết luận điểm yếu |
| Failure | Thiếu nguồn, validator thất bại sau lần sinh lại hoặc timeout | status=no_evidence; báo thiếu căn cứ, cho đường thử lại/đổi khái niệm |
| Correction | POST /report hoặc /skip | Báo sai: loại câu, ghi log, thay câu; bỏ qua: giữ khái niệm và mức |
| Ngoài phạm vi ③ | Xin đáp án trước nộp hoặc dữ liệu người khác | Không đáp ứng phần yêu cầu vượt quyền/phạm vi |
| Domain ④ | Câu bị nghi sai/lộ đáp án | Cho báo câu; không coi kết quả validator chuỗi là chứng minh kiến thức đúng |

Còn cần C xác nhận UI, ảnh chụp và liên kết tới bản build; D xác nhận API/status thực tế.

## §7. Kiểm thử

**Bộ tham chiếu:** [eval/golden.csv](eval/golden.csv), version 2.0, 60 ID GS001-GS060; [rubric và cách chạy](eval/README.md). Có 11 lượt chatlog thật chuyển thể, 36 case thường và 24 case khó/hành vi. Sáu chủ đề trong nhóm thường có sáu case mỗi chủ đề.

**Kênh chạy:** sinh câu qua hàm AI; case validator dùng lỗi giả lập; case session và quyền riêng tư qua API/UI hoặc harness. Không chạy tất cả chỉ bằng hàm sinh câu. Cần ánh xạ concept_id của bộ đo sang app.

| Chiều | Định nghĩa để chấm |
|---|---|
| Schema/yêu cầu | Đúng trường bắt buộc, bốn lựa chọn khác nhau, answer thuộc options, đúng khái niệm và mức yêu cầu |
| Nguồn | Trang nằm trong nguồn cấp; đoạn trích khớp sau chuẩn hóa khoảng trắng và thực sự hỗ trợ nội dung |
| Answer key | Người chấm xác nhận chỉ một đáp án đúng và giải thích nhất quán với slide |
| Mức khó | Mức 1 nhận biết; mức 2 phân biệt/áp dụng đơn giản; mức 3 phân tích tình huống hoặc đánh đổi |
| Lộ đáp án | Đề/UI trước nộp không đánh dấu hoặc giải thích sẵn lựa chọn đúng |
| Hành vi | Đúng kỳ vọng và tiền điều kiện riêng của case; không áp tiêu chí sinh câu cho case cần từ chối |

**Quality bar dự kiến từ Canvas, CHƯA KHÓA:** ≥80% đúng nguồn và khái niệm; ≥90% answer key đúng; ≤10% lộ đáp án; ≥70% đúng mức khó; 100% case ① và ③ xử lý đúng. A và D cần xác nhận phạm vi, mẫu số và thời điểm khóa trước CP4. Chưa có ngưỡng đạt toàn bộ mới được tự đặt trong bản này.

Đề xuất cách báo cáo cần A/D xác nhận khi khóa bar: báo riêng tỷ lệ sinh được câu; tính tỷ lệ đúng nguồn/answer key/mức khó trên các đầu ra đã sinh và được chấm, ghi rõ số đầu ra và số chưa chấm. Case cần sinh nhưng không sinh được vẫn trượt trong tỷ lệ đạt toàn bộ, không được giấu bằng cách giảm mẫu số. Tỷ lệ lộ đáp án trên các câu đã hiển thị; các case từ chối tính theo số case tương ứng đã chạy.

**Trạng thái lượt chạy:** 0/60 đã chạy; số đạt, số trượt và các tỷ lệ chưa có dữ liệu. Chỉ mới kiểm tra cấu trúc CSV/JSON, mã và trích đoạn chatlog, số trang PDF và fixture; đây không phải eval chất lượng AI.

Còn thiếu run_eval.py, adapter/harness, trace đầu vào/đầu ra/thời gian/validator, chấm tay lượt 1-2, bảng kết quả và người ngoài chấm lại 5 case. Chưa có run-1.md/run-2.md/run-final.md.

## §8. Phân công & kế hoạch

| Người | Trách nhiệm theo kế hoạch |
|---|---|
| Nguyễn Hải Nam (A) | AI/prompt/validator, pages.json, chạy và phân tích eval, spec §4/§9, chốt bar cùng D, nộp/demo |
| Nguyễn Trần Bảo Tâm (B) | Evidence, mining, extract_cases.py, khảo sát, spec §1/§2/§3/§8, user test và slide |
| Trần Thị Thu Hiền (C) | Frontend, concepts.json, bốn đường đi, spec §6, quay video |
| Bùi Phương Duy (D) | Backend/rule/session/trace, golden set và run_eval.py, rubric/chấm tay, spec §5/§7 |

**Đã chuẩn bị cho phần B:** chạy mining và lưu báo cáo; script lọc 24 ứng viên; 11 case chatlog trong golden; sáu ví dụ nguyên văn trong §1. Bàn giao trực tiếp cho D chưa được xác nhận. Tài liệu spec này là bản nháp tổng hợp, người phụ trách từng phần vẫn phải rà theo build.

**Validation dự kiến:** B chốt ≥5 willing users có tên thật, cho 5 người ngoài nhóm dùng thử (theo kế hoạch, gồm hai người đã khai CP1). Giao task hoàn tất lượt luyện và tìm chủ đề cần ôn; ghi ai, task, chỗ kẹt, quote và quyết định vào validation/log.md. D nhờ người ngoài nhóm chấm lại 5 case và ghi mức đồng thuận.

**Willing users:** chưa có tên và xác nhận đồng ý trong repo; không điền tên giả. Chưa có log dùng thử hoặc số kết quả validation.

**Mốc trong kế hoạch ngày 18/09:** D giao API cho C 14:30; bộ chạy eval 15:00; CP3 16:00; chốt bar cùng A 20:30; CP4 21:00; validation 21:00-21:45; CP5 22:30. Đây là lịch dự kiến, không phải xác nhận đã bàn giao đúng hạn.

**Multi-prototype:** chưa có bằng chứng nhóm đã xây và so sánh nhiều prototype; không khai hoàn thành.

## §9. Changelog

| Ngày | Thay đổi | Căn cứ / việc còn lại |
|---|---|---|
| 18/09/2026 | Điền spec từ Canvas, kế hoạch, log và golden 2.0 | T10417/T10427/T10438/T10455/T10364/T10983; chưa có survey log và kết quả eval |
| 18/09/2026 | Ghi rõ giới hạn diễn giải mining | Một lượt hỏi không chứng minh bỏ học; không có trường bài làm không chứng minh toàn hệ thống không có luyện tập |
| 18/09/2026 | Phân biệt thiết kế, hiện trạng và phạm vi bộ đo | Day 1 core khác bộ đo Day 1+Day 2; A/C/D cần xác nhận trước khóa spec |
