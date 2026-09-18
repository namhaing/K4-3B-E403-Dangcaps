# Kết quả eval — run-3-muc2

Tính lại từ `run-3-muc2.csv` lúc 19:31 18/09 (đã gồm cột chấm tay).

> Quality bar ở cột 3 là bản **dự kiến** (canvas). Bar chính thức chốt trong `spec.md` §7 lúc 21:00 18/9, sau đó không sửa.
> Ghi đủ mọi case, kể cả case fail. Không sửa số tay.

## Theo chiều chất lượng

| Chiều | Kết quả | Bar dự kiến | Cách chấm |
|---|---|---|---|
| Ra câu hợp lệ (trích dẫn khớp trang, qua validator) — case cần ra câu | 12/13 (92%) | ≥ 80% | tự động |
| Qua validator ngay lần đầu | 11/12 (92%) | (theo dõi) | tự động |
| Không lộ đáp án (đề không chứa nguyên văn đáp án đúng) | 12/12 (100%) | ≥ 90% (lộ ≤ 10%) | tự động |
| Không chép cụm câu trích vào đề (gợi ý quá mạnh) | 11/12 (92%) | (Nam + Duy chốt) | tự động |
| Không lặp câu đã hỏi | 12/12 (100%) | (theo dõi) | tự động |
| Case ① và ③ xử lý đúng | 2/2 (100%) | 100% | tự động |
| Case ② (chưa đủ dữ liệu) xử lý đúng | chưa có số liệu | 100% | tự động |
| Answer key đúng | 12/12 (100%) | ≥ 90% | chấm tay |
| Đúng khái niệm đã chọn | 12/12 (100%) | ≥ 80% | chấm tay |
| Đúng mức khó yêu cầu | 7/12 (58%) | ≥ 70% | chấm tay |

## Từng case

| Case | Nhóm | Nguồn | Mong đợi | Thực tế | Hành vi đúng | Lần thử | Trang | Cờ tự động | Câu hỏi |
|---|---|---|---|---|---|---|---|---|---|
| G02 | thuong | chatlog T10438 | ok | ok | ✅ | 1 | 3 | — | Khi so sánh Generative AI và LLM, phát biểu nào sau đây là đúng? |
| G04 | thuong | tự viết | ok | ok | ✅ | 2 | 4 | — | Một nhóm đang phát triển một hệ thống để phân loại email thành spam và không spa |
| G05 | thuong | chatlog T10672 | ok | ok | ✅ | 1 | 19 | — | Trong quy trình tạo LLM, phát biểu nào sau đây về RLHF là đúng? |
| G06 | thuong | chatlog T10975 | ok | ok | ✅ | 1 | 20 | — | Trong bối cảnh các mô hình ngôn ngữ, điểm khác biệt chính giữa 'hallucination' v |
| G07 | thuong | chatlog T10472 | ok | ok | ✅ | 1 | 29 | — | Khi điều chỉnh các tham số để tạo ra kết quả khác nhau từ mô hình, sự khác biệt  |
| G08 | thuong | chatlog T10511 | ok | ok | ✅ | 1 | 24 | — | Một nhóm đang phát triển một agent, họ cần xác định các thành phần nào là cần th |
| G10 | thuong | chatlog T10355 | ok | ok | ✅ | 1 | 26 | — | Một nhóm đang tìm cách chọn model AI cho dự án của mình. Họ cần biết điều gì qua |
| L1-01 | lop1 | tự viết (khái niệm Day 2) | no_evidence / concept_not_in_lecture | no_evidence / concept_not_in_lecture | ✅ | 0 |  | — |  |
| L3-01 | lop3 | chatlog T00273 (prompt injection) | ok | ok | ✅ | 1 | 3 | — | Một nhóm nghiên cứu đang tìm hiểu về các khái niệm AI. Họ muốn phân biệt giữa Ge |
| L4-01 | lop4 | chatlog T10455 | ok | ok | ✅ | 1 | 3 | — | Một nhóm nghiên cứu đang phát triển một hệ thống có khả năng tạo ra nội dung mới |
| L4-02 | lop4 | chatlog T10427 | ok | ok | ✅ | 1 | 10 | chép cụm câu trích | Một nhóm nghiên cứu đang tìm hiểu về các mô hình ngôn ngữ. Họ muốn phân biệt giữ |
| T-G25 | thuong | bộ 60 của Tâm (G25) | ok | ok | ✅ | 1 | 4 | — | Một nhóm nghiên cứu đang tìm hiểu sự khác biệt giữa hai loại AI. Họ muốn biết lo |
| T-G50 | thuong | bộ 60 của Tâm (G50) | ok | no_evidence / validation_failed | ❌ | 2 |  | — |  |
| T-G53 | thuong | bộ 60 của Tâm (G53) | ok | ok | ✅ | 1 | 20 | — | Một nhóm nghiên cứu đang tìm hiểu về cách mà các mô hình ngôn ngữ sinh ra thông  |

## Case fail — lỗi validator ghi lại

- **T-G50**: no_evidence validation_failed — `[["kiểm chéo: theo slide các lựa chọn đúng là [0, 2], không khớp đáp án 0 (Các phát biểu 0 và 2 đúng theo nội dung trong slide.)"], ["kiểm chéo: theo slide các lựa chọn đúng là [0, 1], không khớp đáp án 1 (Model có thể bỏ sót thông tin quan trọng khi context quá dài và không được sắp xếp hợp lý, hoặ`

## Phân tích nguyên nhân (Nam viết sau khi đọc từng case fail)

> Lượt chạy thử bằng `--only`: chỉ 14 case mức 2 (đúng tập case mức 2 của run-2), **không dùng làm số liệu nộp**. Chấm tay: Claude chấm nháp theo rubric, **Nam và Duy đã duyệt** (18/9, giữ nguyên toàn bộ điểm; tên người duyệt ở cột `nguoi_cham`).

**Thay đổi:** prompt luật 11 mức 2 + `level_guide["2"]`: cấm dạng "mô tả → gọi tên" ("…là hiện tượng gì?", "khái niệm/loại nào…"), chỉ cho 2 dạng: so sánh 2 khái niệm gần nhau, hoặc chọn phát biểu đúng mà mỗi phát biểu sai là một hiểu nhầm cụ thể.

**So với run-2 trên cùng 13 case mức 2 cần ra câu** (run-2 đọc lại theo rubric chặt: G05, G06, T-G53 được chấm Y nhưng thật ra là "mô tả → gọi tên"):

| | run-2 (chấm lại chặt) | run-3-muc2 |
|---|---|---|
| Mức 2 là câu phân biệt thật | 4/11 (36%) | **7/12 (58%)** |
| Answer key đúng | 11/11 | 12/12 (3 câu ghi "có thể bàn") |
| Ra câu | 11/13 | 12/13 |
| Độ trễ trung vị (câu ra được) | 3.6 s | 5.5 s |

- **Tốt lên:** G02, G05, G06, G10, L3-01 chuyển sang so sánh / phát biểu đúng. Lựa chọn sai bắt đúng hiểu nhầm slide cảnh báo (G07: "temperature làm model thông minh hơn"; L3-01: đảo quan hệ DL/GenAI; L4-02: nhầm LLM với chatbot).
- **Còn lỗi, 5/12:** cùng một dạng — **khoác tình huống rồi hỏi "loại / công nghệ / khái niệm nào"** (G04, L4-01, T-G25, T-G53), hoặc đáp án chép lại định nghĩa (G08). T-G53 ra đúng dạng ví dụ SAI trong prompt → `gpt-4o-mini` chỉ theo prompt một phần. Chưa đạt bar 70%.
- **T-G50 bị chặn** (lần trước ra câu): cả 2 lần kiểm chéo thấy 2 phát biểu cùng đúng. Đúng rủi ro đã đoán: câu "chọn phát biểu đúng" dễ có 2 đáp án đúng. Chặn đúng, không phải chặn oan.
- **Độ trễ tăng 3.6 → 5.5 s:** chưa rõ do prompt dài hơn hay do mạng (12 mẫu). Cần đo lại trong trace.
- **Bước tiếp theo nếu làm:** thêm kiểm tra bằng code trong validator cho mức 2 (regex bắt "…là gì? / …nào?" dạng gọi tên) để sinh lại kèm lý do. Đánh đổi: thêm ~5 s cho câu bị sinh lại, và có thể thêm `no_evidence`.
