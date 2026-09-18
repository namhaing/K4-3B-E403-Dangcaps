# Kết quả eval — run-5

Tính lại từ `run-5.csv` lúc 20:56 18/09 (đã gồm cột chấm tay).

> Quality bar ở cột 3 là bản **dự kiến** (canvas). Bar chính thức chốt trong `spec.md` §7 lúc 21:00 18/9, sau đó không sửa.
> Ghi đủ mọi case, kể cả case fail. Không sửa số tay.

## Theo chiều chất lượng

| Chiều | Kết quả | Bar dự kiến | Cách chấm |
|---|---|---|---|
| Ra câu hợp lệ (trích dẫn khớp trang, qua validator) — case cần ra câu | 22/24 (92%) | ≥ 80% | tự động |
| Qua validator ngay lần đầu | 21/22 (95%) | (theo dõi) | tự động |
| Không lộ đáp án (đề không chứa nguyên văn đáp án đúng) | 21/22 (95%) | ≥ 90% (lộ ≤ 10%) | tự động |
| Không chép cụm câu trích vào đề (gợi ý quá mạnh) | 17/22 (77%) | (Nam + Duy chốt) | tự động |
| Không lặp câu đã hỏi | 22/22 (100%) | (theo dõi) | tự động |
| Case ① và ③ xử lý đúng | 6/6 (100%) | 100% | tự động |
| Case ② (chưa đủ dữ liệu) xử lý đúng | 3/3 (100%) | 100% | tự động |
| Answer key đúng | 21/22 (95%) | ≥ 90% | chấm tay |
| Đúng khái niệm đã chọn | 22/22 (100%) | ≥ 80% | chấm tay |
| Đúng mức khó yêu cầu | 22/22 (100%) | ≥ 70% | chấm tay |

## Từng case

| Case | Nhóm | Nguồn | Mong đợi | Thực tế | Hành vi đúng | Lần thử | Trang | Cờ tự động | Câu hỏi |
|---|---|---|---|---|---|---|---|---|---|
| G01 | thuong | chatlog T10417 | ok | ok | ✅ | 1 | 3 | chép cụm câu trích | Khái niệm nào được mô tả là 'chiếc ô lớn nhất' trong hệ thống có yếu tố thông mi |
| G02 | thuong | chatlog T10438 | ok | ok | ✅ | 1 | 3 | — | Trong các khái niệm AI, phát biểu nào đúng về mối quan hệ giữa Machine Learning  |
| G03 | thuong | chatlog T10414 | ok | ok | ✅ | 1 | 10 | — | LLM là gì trong lĩnh vực trí tuệ nhân tạo? |
| G04 | thuong | tự viết | ok | ok | ✅ | 2 | 4 | chép cụm câu trích | Trong ba nhóm AI chính, sự khác biệt nào giữa Discriminative AI và Generative AI |
| G05 | thuong | chatlog T10672 | ok | ok | ✅ | 1 | 18 | — | Một nhóm nghiên cứu đang tìm hiểu về quy trình huấn luyện LLM. Họ muốn biết lý d |
| G06 | thuong | chatlog T10975 | ok | ok | ✅ | 1 | 20 | — | Trong bối cảnh làm việc với LLM, phát biểu nào sau đây về các giới hạn của mô hì |
| G07 | thuong | chatlog T10472 | ok | no_evidence / validation_failed | ❌ | 2 |  | — |  |
| G08 | thuong | chatlog T10511 | ok | ok | ✅ | 1 | 23 | — | Một nhóm nghiên cứu đang tìm hiểu về sự khác biệt giữa agent và LLM. Họ phát hiệ |
| G09 | thuong | chatlog T10781 | ok | no_evidence / validation_failed | ❌ | 2 |  | — |  |
| G10 | thuong | chatlog T10355 | ok | ok | ✅ | 1 | 26 | — | Khi lựa chọn model cho một nhiệm vụ, phát biểu nào sau đây là đúng? |
| H01 | hiem | chatlog T10474 | ok | ok | ✅ | 1 | 8 | — | Một nhóm nghiên cứu đang phát triển một ứng dụng xử lý ngôn ngữ tự nhiên. Họ cần |
| H02 | hiem | tự viết | ok | ok | ✅ | 1 | 15 | — | Một nhóm nghiên cứu đang phát triển một mô hình ngôn ngữ mới. Họ muốn mô hình có |
| H03 | hiem | tự viết | ok | ok | ✅ | 1 | 14 | — | Một nhóm phát triển AI cần tối ưu hóa việc sử dụng thông tin trong câu hỏi để mo |
| L1-01 | lop1 | tự viết (khái niệm Day 2) | no_evidence / concept_not_in_lecture | no_evidence / concept_not_in_lecture | ✅ | 0 |  | — |  |
| L1-02 | lop1 | tự viết (khái niệm Day 3) | no_evidence / concept_not_in_lecture | no_evidence / concept_not_in_lecture | ✅ | 0 |  | — |  |
| L1-03 | lop1 | tự viết | ok | ok | ✅ | 1 | 26 | — | Một nhóm phát triển phần mềm đang tìm kiếm một mô hình AI để tự động hóa các tác |
| L2-01 | lop2 | tự viết | not_enough_data | not_enough_data | ✅ |  |  | — | 2 câu đã trả lời |
| L2-02 | lop2 | tự viết | not_enough_data | not_enough_data | ✅ |  |  | — | 5 câu đã trả lời |
| L2-03 | lop2 | tự viết | no_evidence / invalid_level | no_evidence / invalid_level | ✅ | 0 |  | — |  |
| L3-01 | lop3 | chatlog T00273 (prompt injection) | ok | ok | ✅ | 1 | 3 | — | Trong các phát biểu sau, phát biểu nào đúng về sự khác nhau giữa Generative AI v |
| L3-02 | lop3 | chatlog T10515 (đòi đáp án) | ok | ok | ✅ |  |  | — | Một nhóm đang tìm hiểu về các loại AI và đang phân vân giữa Discriminative AI và |
| L3-03 | lop3 | tự viết | http_404 | http_404 | ✅ |  |  | — |  |
| L4-01 | lop4 | chatlog T10455 | ok | ok | ✅ | 1 | 3 | — | Trong các khái niệm về AI, phát biểu nào sau đây mô tả đúng về Generative AI? |
| L4-02 | lop4 | chatlog T10427 | ok | ok | ✅ | 1 | 10 | chép cụm câu trích | Một nhóm nghiên cứu đang tìm hiểu về các mô hình ngôn ngữ. Họ thảo luận về sự kh |
| L4-03 | lop4 | run thử 18/9 (đề chép cụm 'chiếc ô lớn nhất') | ok | ok | ❌ | 1 | 3 | lộ đáp án, chép cụm câu trích | Khái niệm nào được mô tả là 'chiếc ô lớn nhất' trong hệ thống AI? |
| T-G07 | thuong | bộ 60 của Tâm (G07) | ok | ok | ✅ | 1 | 14 | — | Một nhóm nghiên cứu đang phát triển một ứng dụng AI có khả năng trả lời câu hỏi  |
| T-G21 | thuong | bộ 60 của Tâm (G21) | ok | ok | ✅ | 1 | 14 | — | Một nhóm nghiên cứu đang phát triển một ứng dụng AI và muốn đảm bảo rằng các thô |
| T-G25 | thuong | bộ 60 của Tâm (G25) | ok | ok | ✅ | 1 | 4 | — | Khi so sánh Discriminative AI và Generative AI, phát biểu nào sau đây là đúng? |
| T-G38 | thuong | bộ 60 của Tâm (G38) | ok | ok | ✅ | 1 | 14 | — | Một nhóm nghiên cứu đang phát triển một ứng dụng AI và muốn đảm bảo rằng các thô |
| T-G50 | thuong | bộ 60 của Tâm (G50) | ok | ok | ✅ | 1 | 14 | — | Một nhóm nghiên cứu muốn tối ưu hóa việc sử dụng AI trong việc xử lý văn bản. Họ |
| T-G53 | thuong | bộ 60 của Tâm (G53) | ok | ok | ✅ | 1 | 20 | chép cụm câu trích | Khi nào LLM có thể tự tin đưa ra thông tin sai lệch? |

## Case fail — lỗi validator ghi lại

- **G07**: no_evidence validation_failed — `[["không dùng lựa chọn gộp kiểu 'Cả A và B', 'Tất cả đều đúng', 'Không có đáp án nào': ['Cả hai đều có tác dụng giống nhau trong việc cải thiện chất lượng đầu ra của mô hình.']"], ["kiểm chéo: theo slide các lựa chọn đúng là [0, 1], không khớp đáp án 1 (Slide nêu rõ rằng temperature được điều chỉnh `
- **G09**: no_evidence validation_failed — `[["câu trích không có nguyên văn trong trang 22"], ["câu trích không có nguyên văn trong trang 22"]]`
- **L4-03**: ok  — `[]`

## Phân tích nguyên nhân (Nam viết sau khi đọc từng case fail)

> Lượt đo **trọn bộ 31 case trên bản hiện tại** (prompt luật 11 + validator chặn mức 2 dạng gọi tên + kiểm chéo), chạy 20:46 18/9. Chấm tay: Claude chấm nháp theo rubric, **chờ Nam/Duy duyệt** (cột `nguoi_cham`).

**Đạt toàn bộ: 27/31 case (87%).** Mọi chiều đạt quality bar đã khoá (spec §7): ra câu 22/24 (92%) · khái niệm 22/22 · answer key 21/22 (95%) · lộ đáp án 1/22 (5%) · mức khó 22/22 · ①③ 6/6 · ② 3/3.

**So với run-2 (cùng 31 case, trước khi sửa mức 2):** mức khó 17/21 (chấm chặt 14/21, 67% — dưới bar) → **22/22**; ra câu 21/24 → 22/24; answer key 21/21 → 21/22; chép cụm câu trích 3/21 → 5/22.

**4 case chưa đạt:**
1. **G05 — sai đáp án (lỗi nặng nhất).** Đáp án đánh dấu: "RLHF giúp model tạo ra nhiều câu trả lời khác nhau cho cùng một câu hỏi". Slide 18: RLHF là "được uốn nắn: học theo phản hồi con người"; việc model viết nhiều câu trả lời chỉ là bước ① trong quy trình. Không lựa chọn nào đúng. **Kiểm chéo (cùng model) cũng hiểu sai → cho qua.** Nếu ra cho học viên, người hiểu đúng sẽ bị chấm sai.
2. **G07 — không ra câu.** Lần 1 bị validator chặn vì lựa chọn "Cả hai đều có tác dụng giống nhau…" — đây là **chặn nhầm**: "cả hai" chỉ temperature và top_p trong đề, là một hiểu nhầm có nội dung, không phải lựa chọn gộp kiểu "Cả A và B". Lần 2 bị kiểm chéo chặn vì 2 đáp án cùng đúng — chặn đúng.
3. **G09 — không ra câu.** Cả 2 lần AI không chép được câu trích nguyên văn ở trang 22 (chain-of-thought). Chưa xem nguyên nhân (có thể do chữ trang 22 trích từ PDF bị ngắt dòng / ký tự đặc biệt).
4. **L4-03 — lộ đáp án.** Đề "Khái niệm nào được mô tả là 'chiếc ô lớn nhất' trong hệ thống AI?" — đáp án ngắn "AI" nằm ngay trong đề, và đề chép cụm câu trích. Lỗi đã biết từ run-1; khái niệm `ai_layers` trang 3 chỉ có một câu đặc trưng cho AI.

**Theo dõi thêm:**
- Chép cụm câu trích tăng 3/21 → 5/22 (G01, G04, L4-02, L4-03, T-G53) — prompt luật 9 chỉ đỡ một phần.
- 3 case token_context mức 3 (H03, T-G21, T-G38) ra câu gần giống nhau ("giữ context sạch") — đúng nhưng ít đa dạng.
- 2 câu mức 2 sát ranh giới nhận biết (L4-01, T-G53) — chấm Y theo chữ của rubric ("chọn phát biểu đúng, lựa chọn sai là hiểu nhầm hay gặp"), người duyệt quyết.

**Việc nên làm tiếp:** (a) kiểm chéo bằng model khác hoặc bắt kiểm chéo tự giải thích đáp án theo câu trích — để bắt kiểu lỗi G05; (b) thu hẹp luật "lựa chọn gộp" để không chặn "Cả hai đều …" có nội dung (G07); (c) xem chữ trang 22 (G09).
