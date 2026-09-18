# Kết quả eval — run-4-muc2

Tính lại từ `run-4-muc2.csv` lúc 19:37 18/09 (đã gồm cột chấm tay).

> Quality bar ở cột 3 là bản **dự kiến** (canvas). Bar chính thức chốt trong `spec.md` §7 lúc 21:00 18/9, sau đó không sửa.
> Ghi đủ mọi case, kể cả case fail. Không sửa số tay.

## Theo chiều chất lượng

| Chiều | Kết quả | Bar dự kiến | Cách chấm |
|---|---|---|---|
| Ra câu hợp lệ (trích dẫn khớp trang, qua validator) — case cần ra câu | 12/13 (92%) | ≥ 80% | tự động |
| Qua validator ngay lần đầu | 7/12 (58%) | (theo dõi) | tự động |
| Không lộ đáp án (đề không chứa nguyên văn đáp án đúng) | 12/12 (100%) | ≥ 90% (lộ ≤ 10%) | tự động |
| Không chép cụm câu trích vào đề (gợi ý quá mạnh) | 12/12 (100%) | (Nam + Duy chốt) | tự động |
| Không lặp câu đã hỏi | 12/12 (100%) | (theo dõi) | tự động |
| Case ① và ③ xử lý đúng | 2/2 (100%) | 100% | tự động |
| Case ② (chưa đủ dữ liệu) xử lý đúng | chưa có số liệu | 100% | tự động |
| Answer key đúng | 11/12 (92%) | ≥ 90% | chấm tay |
| Đúng khái niệm đã chọn | 12/12 (100%) | ≥ 80% | chấm tay |
| Đúng mức khó yêu cầu | 12/12 (100%) | ≥ 70% | chấm tay |

## Từng case

| Case | Nhóm | Nguồn | Mong đợi | Thực tế | Hành vi đúng | Lần thử | Trang | Cờ tự động | Câu hỏi |
|---|---|---|---|---|---|---|---|---|---|
| G02 | thuong | chatlog T10438 | ok | ok | ✅ | 1 | 3 | — | Một nhóm nghiên cứu đang tìm hiểu về các khái niệm trong AI. Họ muốn biết sự khá |
| G04 | thuong | tự viết | ok | ok | ✅ | 1 | 4 | — | Một nhóm nghiên cứu đang tìm hiểu về các loại AI. Họ cần phân biệt giữa AI phân  |
| G05 | thuong | chatlog T10672 | ok | ok | ✅ | 2 | 18 | — | Trong quy trình tạo LLM, phát biểu nào đúng giữa pre-training và SFT? |
| G06 | thuong | chatlog T10975 | ok | ok | ✅ | 2 | 20 | — | Khi so sánh knowledge cutoff và hallucination, điểm khác biệt nào dưới đây là ch |
| G07 | thuong | chatlog T10472 | ok | ok | ✅ | 2 | 29 | — | Khi muốn tạo ra nội dung đa dạng hơn trong một prompt, người dùng nên điều chỉnh |
| G08 | thuong | chatlog T10511 | ok | ok | ✅ | 1 | 23 | — | Một nhóm nghiên cứu đang tìm hiểu sự khác biệt giữa LLM và agent trong ứng dụng  |
| G10 | thuong | chatlog T10355 | ok | no_evidence / validation_failed | ❌ | 2 |  | — |  |
| L1-01 | lop1 | tự viết (khái niệm Day 2) | no_evidence / concept_not_in_lecture | no_evidence / concept_not_in_lecture | ✅ | 0 |  | — |  |
| L3-01 | lop3 | chatlog T00273 (prompt injection) | ok | ok | ✅ | 1 | 3 | — | Một nhóm nghiên cứu đang tìm hiểu về các khái niệm trong AI. Họ muốn phân biệt g |
| L4-01 | lop4 | chatlog T10455 | ok | ok | ✅ | 1 | 3 | — | Một nhóm nghiên cứu đang tìm hiểu về các công nghệ AI. Họ muốn phân biệt giữa Ge |
| L4-02 | lop4 | chatlog T10427 | ok | ok | ✅ | 1 | 10 | — | Một nhóm nghiên cứu đang tìm hiểu về các mô hình ngôn ngữ. Họ muốn phân biệt giữ |
| T-G25 | thuong | bộ 60 của Tâm (G25) | ok | ok | ✅ | 2 | 4 | — | Khi so sánh Discriminative AI và Generative AI, phát biểu nào sau đây là đúng? |
| T-G50 | thuong | bộ 60 của Tâm (G50) | ok | ok | ✅ | 2 | 14 | — | Một nhóm đang phát triển một ứng dụng AI và cần đảm bảo rằng thông tin quan trọn |
| T-G53 | thuong | bộ 60 của Tâm (G53) | ok | ok | ✅ | 1 | 20 | — | Trong bối cảnh của LLM, phát biểu nào sau đây đúng về sự khác nhau giữa knowledg |

## Case fail — lỗi validator ghi lại

- **G10**: no_evidence validation_failed — `[["mức 2 đang hỏi dạng mô tả → gọi tên ('tầng nào'); viết lại thành so sánh 2 khái niệm gần nhau ('X khác Y ở điểm nào?') hoặc 'phát biểu nào đúng' với 4 phát biểu đầy đủ, mỗi phát biểu sai là một hiểu nhầm"], ["câu trích không có nguyên văn trong trang 26"]]`

## Phân tích nguyên nhân (Nam viết sau khi đọc từng case fail)

> Lượt chạy thử bằng `--only`: 14 case mức 2 (cùng tập với run-2 và run-3-muc2), **không dùng làm số liệu nộp**. Chấm tay: Claude chấm nháp theo rubric, **Nam và Duy đã duyệt** (18/9, giữ nguyên toàn bộ điểm; tên người duyệt ở cột `nguoi_cham`).

**Thay đổi so với run-3-muc2:** validator (code) chặn mức 2 dạng "mô tả → gọi tên": đề hỏi "khái niệm / loại / công nghệ / hiện tượng / bước / tầng… nào (gì)", "được gọi là gì", hoặc cả 4 lựa chọn chỉ là tên (≤ 3 chữ). Lỗi ghi sẵn cách sửa và được gửi lại cho AI ở lần sinh lại. Chỉ áp dụng cho mức 2. Trước khi chạy đã thử offline trên 23 câu mức 2 đã chấm của run-2 và run-3: không chặn nhầm câu Y nào (0/11), bắt được 11/12 câu N.

| 13 case mức 2 cần ra câu | run-2 (chấm lại chặt) | run-3-muc2 (chỉ sửa prompt) | run-4-muc2 (+ validator) |
|---|---|---|---|
| Đúng mức 2 (phân biệt thật) | 4/11 (36%) | 7/12 (58%) | **12/12 (100%)** |
| Answer key đúng | 11/11 | 12/12 | 11/12 (92%) |
| Ra câu | 11/13 | 12/13 | 12/13 |
| Qua ngay lần đầu | — | 11/12 | 7/12 |
| Độ trễ trung vị (câu ra được) | 3.6 s | 5.5 s | **7.0 s** |

- **Luật mới có tác dụng:** 3 câu bị chặn lần đầu vì gọi tên (G05 "bước nào", G06 "khái niệm nào", T-G25 "loại nào"), cả 3 lần sinh lại đều thành câu so sánh đạt. Lựa chọn sai là hiểu nhầm có thật: G05 đảo vai pre-training/SFT; G08 "agent là một loại model khác"; T-G50 "context càng dài càng tốt" (cả 2 đều là điều slide cảnh báo).
- **G10 không ra câu:** lần 1 hỏi "tầng nào" (bị chặn), lần 2 bịa câu trích → `no_evidence`. Trong app, API tự chuyển sang khái niệm khác.
- **G07 answer key sai, kiểm chéo không bắt được:** "tăng temperature" và "tăng top_p" đều làm câu trả lời đa dạng hơn theo cơ chế ở slide 29. Kiểm chéo dùng cùng model nên có thể sai giống nhau (đã ghi ở run-2).
- **Cái giá phải trả là độ trễ:** 5/12 câu phải sinh lại → trung vị 7.0 s. Đánh đổi có chủ đích: câu mức 2 phải kiểm tra được phân biệt, nếu không bản đồ "chỗ yếu" sẽ báo "đã vững" quá tay.
- **Lỗi cũ vẫn còn, không do lần sửa này:** câu trích nhiều khi khớp trang nhưng không chứng minh đáp án (G02, G04, T-G25, T-G50 trích tiêu đề hoặc dòng định nghĩa). Validator chỉ kiểm câu trích có nguyên văn trong trang, chưa kiểm câu trích có đỡ cho đáp án không.
- **Giới hạn:** mới có 12 câu, chỉ ở mức 2. Cần chạy toàn bộ golden set để có số nộp.
