# Kết quả eval — run-2

Tính lại từ `run-2.csv` lúc 14:54 18/09 (đã gồm cột chấm tay).

> Quality bar ở cột 3 là bản **dự kiến** (canvas). Bar chính thức chốt trong `spec.md` §7 lúc 21:00 18/9, sau đó không sửa.
> Ghi đủ mọi case, kể cả case fail. Không sửa số tay.

## Theo chiều chất lượng

| Chiều | Kết quả | Bar dự kiến | Cách chấm |
|---|---|---|---|
| Ra câu hợp lệ (trích dẫn khớp trang, qua validator) — case cần ra câu | 21/24 (88%) | ≥ 80% | tự động |
| Qua validator ngay lần đầu | 18/21 (86%) | (theo dõi) | tự động |
| Không lộ đáp án (đề không chứa nguyên văn đáp án đúng) | 20/21 (95%) | ≥ 90% (lộ ≤ 10%) | tự động |
| Không chép cụm câu trích vào đề (gợi ý quá mạnh) | 18/21 (86%) | (Nam + Duy chốt) | tự động |
| Không lặp câu đã hỏi | 21/21 (100%) | (theo dõi) | tự động |
| Case ① và ③ xử lý đúng | 6/6 (100%) | 100% | tự động |
| Case ② (chưa đủ dữ liệu) xử lý đúng | 3/3 (100%) | 100% | tự động |
| Answer key đúng | 21/21 (100%) | ≥ 90% | chấm tay |
| Đúng khái niệm đã chọn | 21/21 (100%) | ≥ 80% | chấm tay |
| Đúng mức khó yêu cầu | 17/21 (81%) | ≥ 70% | chấm tay |

## Từng case

| Case | Nhóm | Nguồn | Mong đợi | Thực tế | Hành vi đúng | Lần thử | Trang | Cờ tự động | Câu hỏi |
|---|---|---|---|---|---|---|---|---|---|
| G01 | thuong | chatlog T10417 | ok | ok | ✅ | 1 | 3 | — | AI được định nghĩa là gì trong hệ thống các tầng AI? |
| G02 | thuong | chatlog T10438 | ok | ok | ✅ | 1 | 3 | — | Trong các khái niệm AI, khái niệm nào được coi là tầng rộng nhất, bao trùm các t |
| G03 | thuong | chatlog T10414 | ok | ok | ✅ | 1 | 10 | chép cụm câu trích | Mô hình nào được định nghĩa là 'mô hình ngôn ngữ rất lớn' và có khả năng đoán mả |
| G04 | thuong | tự viết | ok | no_evidence / validation_failed | ❌ | 2 |  | — |  |
| G05 | thuong | chatlog T10672 | ok | ok | ✅ | 1 | 19 | — | Trong quy trình tạo LLM, bước nào giúp mô hình học từ phản hồi của con người để  |
| G06 | thuong | chatlog T10975 | ok | ok | ✅ | 1 | 20 | — | Khi một mô hình ngôn ngữ tạo ra thông tin không chính xác nhưng vẫn trình bày mộ |
| G07 | thuong | chatlog T10472 | ok | ok | ✅ | 1 | 29 | — | Khi điều chỉnh để thay đổi cách chọn từ trong mô hình, người dùng nên chọn điều  |
| G08 | thuong | chatlog T10511 | ok | ok | ✅ | 1 | 23 | chép cụm câu trích | Một LLM được sử dụng trong một vòng làm việc có mục tiêu và hành động thì được g |
| G09 | thuong | chatlog T10781 | ok | ok | ✅ | 1 | 22 | — | Khái niệm nào mô tả việc cho phép model sử dụng giấy nháp để cải thiện khả năng  |
| G10 | thuong | chatlog T10355 | ok | no_evidence / validation_failed | ❌ | 2 |  | — |  |
| H01 | hiem | chatlog T10474 | ok | ok | ✅ | 2 | 8 | — | Một nhóm nghiên cứu đang phát triển một mô hình ngôn ngữ mới. Họ muốn mô hình nà |
| H02 | hiem | tự viết | ok | ok | ✅ | 2 | 15 | — | Một nhóm nghiên cứu đang phát triển mô hình ngôn ngữ mới và cần đảm bảo rằng mỗi |
| H03 | hiem | tự viết | ok | ok | ✅ | 1 | 14 | — | Một nhóm nghiên cứu đang phát triển một mô hình AI để trả lời câu hỏi từ người d |
| L1-01 | lop1 | tự viết (khái niệm Day 2) | no_evidence / concept_not_in_lecture | no_evidence / concept_not_in_lecture | ✅ | 0 |  | — |  |
| L1-02 | lop1 | tự viết (khái niệm Day 3) | no_evidence / concept_not_in_lecture | no_evidence / concept_not_in_lecture | ✅ | 0 |  | — |  |
| L1-03 | lop1 | tự viết | ok | ok | ✅ | 2 | 26 | — | Một nhóm phát triển phần mềm cần chọn một mô hình AI để tự động hóa các tác vụ h |
| L2-01 | lop2 | tự viết | not_enough_data | not_enough_data | ✅ |  |  | — | 2 câu đã trả lời |
| L2-02 | lop2 | tự viết | not_enough_data | not_enough_data | ✅ |  |  | — | 5 câu đã trả lời |
| L2-03 | lop2 | tự viết | no_evidence / invalid_level | no_evidence / invalid_level | ✅ | 0 |  | — |  |
| L3-01 | lop3 | chatlog T00273 (prompt injection) | ok | ok | ✅ | 1 | 3 | — | Một nhóm nghiên cứu đang tìm hiểu về các công nghệ AI. Họ nhận thấy rằng một tro |
| L3-02 | lop3 | chatlog T10515 (đòi đáp án) | ok | ok | ✅ |  |  | — | Trong các khái niệm AI, phát biểu nào đúng về Generative AI? |
| L3-03 | lop3 | tự viết | http_404 | http_404 | ✅ |  |  | — |  |
| L4-01 | lop4 | chatlog T10455 | ok | ok | ✅ | 1 | 3 | — | Một nhóm nghiên cứu đang tìm hiểu về các tầng của AI và muốn biết LLM có phải là |
| L4-02 | lop4 | chatlog T10427 | ok | ok | ✅ | 1 | 10 | — | Một mô hình ngôn ngữ lớn có thể được sử dụng cho nhiều ứng dụng khác nhau. Tuy n |
| L4-03 | lop4 | run thử 18/9 (đề chép cụm 'chiếc ô lớn nhất') | ok | ok | ❌ | 1 | 3 | lộ đáp án, chép cụm câu trích | Khái niệm nào được mô tả là 'chiếc ô lớn nhất' trong hệ thống AI? |
| T-G07 | thuong | bộ 60 của Tâm (G07) | ok | no_evidence / validation_failed | ❌ | 2 |  | — |  |
| T-G21 | thuong | bộ 60 của Tâm (G21) | ok | ok | ✅ | 1 | 14 | — | Một nhóm nghiên cứu đang phát triển một mô hình AI để trả lời câu hỏi từ người d |
| T-G25 | thuong | bộ 60 của Tâm (G25) | ok | ok | ✅ | 1 | 4 | — | Một hệ thống AI có khả năng tạo ra văn bản mới dựa trên các yêu cầu của người dù |
| T-G38 | thuong | bộ 60 của Tâm (G38) | ok | ok | ✅ | 1 | 14 | — | Một nhóm phát triển AI đang làm việc với một mô hình ngôn ngữ. Họ nhận thấy rằng |
| T-G50 | thuong | bộ 60 của Tâm (G50) | ok | ok | ✅ | 1 | 14 | — | Khi so sánh token và context trong mô hình AI, phát biểu nào sau đây là đúng? |
| T-G53 | thuong | bộ 60 của Tâm (G53) | ok | ok | ✅ | 1 | 20 | — | Khi một mô hình AI đưa ra câu trả lời tự tin nhưng không chính xác, hiện tượng n |

## Case fail — lỗi validator ghi lại

- **G04**: no_evidence validation_failed — `[["không dùng lựa chọn gộp kiểu 'Cả A và B', 'Tất cả đều đúng', 'Không có đáp án nào': ['Cả ba loại đều tạo ra nội dung mới']"], ["không dùng lựa chọn gộp kiểu 'Cả A và B', 'Tất cả đều đúng', 'Không có đáp án nào': ['Cả ba loại đều sinh ra nội dung mới']"]]`
- **G10**: no_evidence validation_failed — `[["câu trích không có nguyên văn trong trang 26"], ["kiểm chéo: theo slide các lựa chọn đúng là [0, 2], không khớp đáp án 0 (Lựa chọn model nên dựa vào tầng phù hợp, không phải tên gọi, và việc đơn giản không nên dùng model rẻ.)"]]`
- **L4-03**: ok  — `[]`
- **T-G07**: no_evidence validation_failed — `[["kiểm chéo: theo slide các lựa chọn đúng là [2, 3], không khớp đáp án 2 (Đặt điều quan trọng ở đầu và cuối văn bản là một cách tối ưu hóa để model không bỏ sót thông tin quan trọng.)"], ["kiểm chéo: theo slide các lựa chọn đúng là [0, 2], không khớp đáp án 2 (Đặt điều quan trọng ở đầu và cuối giúp`

## Phân tích nguyên nhân (Nam viết sau khi đọc từng case fail)

> ⚠️ **NHÁP do Claude viết — Nam đọc lại, viết bằng lời của mình, rồi xoá dòng này.** Chấm tay trong CSV: Claude chấm nháp theo rubric, **Nam và Duy đã duyệt** (18/9, giữ nguyên toàn bộ điểm; tên người duyệt ở cột `nguoi_cham`).

**Thay đổi so với run-1 (ghi vào spec §9 Changelog):**
1. **Thêm bước kiểm chéo bằng AI** (`generator.cross_check`): sau validator, gọi AI lần 2 với vai người kiểm đề, KHÔNG cho biết đáp án, bắt giải lại. Chỉ cho qua khi đề rõ nghĩa VÀ đúng 1 lựa chọn đúng trùng đáp án. Lý do: run-1 G02 (4 đáp án đúng), G04, và case demo "AI chính" (AI hiểu tiêu đề slide "Ba nhóm AI chính" thành tên một nhóm → chấm oan học viên). Đã thử trực tiếp: chặn được cả "AI chính" và G02, cho qua câu đúng.
2. **Prompt luật 11–12:** định nghĩa từng mức kèm ví dụ, mức 3 bắt buộc mở đầu bằng tình huống; cấm lấy mảnh tiêu đề slide làm đáp án. Lý do: run-1 3/4 câu mức 3 chỉ là câu hỏi định nghĩa.
3. `temperature` 0.7 → 0.5.
4. Golden thêm 6 case từ bộ 60 của Tâm (T-G07…T-G53) → 31 case. **Mẫu số khác run-1, so sánh cần ghi rõ.**

**So với run-1 (chấm tay là NHÁP):**

| Chiều | run-1 | run-2 |
|---|---|---|
| Answer key đúng (trên các câu đã hiển thị) | 16/18 (89%) | 21/21 (100%) |
| Đúng mức khó | 13/18 (72%) | 17/21 (81%) |
| Mức 3 có tình huống | 1/4 | 6/6 |
| Chép cụm câu trích | 5/18 | 3/21 |
| Ra câu (case cần ra câu) | 18/18 (100%) | 21/24 (88%) |

**Đánh đổi chính:** tỷ lệ ra câu giảm 100% → 88% vì kiểm chéo chặn 3 case (G04, G10, T-G07). Đã đọc từng case: **cả 3 bị chặn đúng** (lựa chọn gộp; 2 đáp án đúng ở G10 và T-G07), không có chặn oan. Nhóm chọn "không ra câu còn hơn ra câu chấm oan" (cost-of-error §4). Trong app, khi 1 khái niệm bị chặn, API tự chuyển khái niệm khác nên học viên vẫn có câu.

**Lỗi còn lại:**
- Mức 2 vẫn hay thành câu nhận biết (G02, G08, L3-01, T-G25): model khoác tình huống nhưng thực chất hỏi định nghĩa.
- L4-03 vẫn chép cụm "chiếc ô lớn nhất" và để lộ đáp án ngắn "AI" — khái niệm `ai_layers` trang 3 chỉ có một câu đặc trưng.
- Kiểm chéo dùng cùng model (`gpt-4o-mini`) nên có thể cùng hiểu sai; chưa đo tỷ lệ chặn nhầm trên bộ lớn hơn.
- Độ trễ tăng (thêm 1 lần gọi AI mỗi câu) — cần đo `latency_ms` trong trace.
