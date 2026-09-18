# Kết quả eval — run-1

Tính lại từ `run-1.csv` lúc 12:34 18/09 (đã gồm cột chấm tay).

> Quality bar ở cột 3 là bản **dự kiến** (canvas). Bar chính thức chốt trong `spec.md` §7 lúc 21:00 18/9, sau đó không sửa.
> Ghi đủ mọi case, kể cả case fail. Không sửa số tay.

## Theo chiều chất lượng

| Chiều | Kết quả | Bar dự kiến | Cách chấm |
|---|---|---|---|
| Ra câu hợp lệ (trích dẫn khớp trang, qua validator) — case cần ra câu | 18/18 (100%) | ≥ 80% | tự động |
| Qua validator ngay lần đầu | 15/18 (83%) | (theo dõi) | tự động |
| Không lộ đáp án (đề không chứa nguyên văn đáp án đúng) | 17/18 (94%) | ≥ 90% (lộ ≤ 10%) | tự động |
| Không chép cụm câu trích vào đề (gợi ý quá mạnh) | 13/18 (72%) | (Nam + Duy chốt) | tự động |
| Không lặp câu đã hỏi | 18/18 (100%) | (theo dõi) | tự động |
| Case ① và ③ xử lý đúng | 6/6 (100%) | 100% | tự động |
| Case ② (chưa đủ dữ liệu) xử lý đúng | 3/3 (100%) | 100% | tự động |
| Answer key đúng | 16/18 (89%) | ≥ 90% | chấm tay |
| Đúng khái niệm đã chọn | 18/18 (100%) | ≥ 80% | chấm tay |
| Đúng mức khó yêu cầu | 13/18 (72%) | ≥ 70% | chấm tay |

## Từng case

| Case | Nhóm | Nguồn | Mong đợi | Thực tế | Hành vi đúng | Lần thử | Trang | Cờ tự động | Câu hỏi |
|---|---|---|---|---|---|---|---|---|---|
| G01 | thuong | chatlog T10417 | ok | ok | ✅ | 1 | 3 | chép cụm câu trích | Tầng nào được mô tả là 'chiếc ô lớn nhất' trong hệ thống AI? |
| G02 | thuong | chatlog T10438 | ok | ok | ✅ | 1 | 3 | — | Khái niệm nào trong số các khái niệm dưới đây là tầng hẹp hơn so với AI? |
| G03 | thuong | chatlog T10414 | ok | ok | ✅ | 1 | 10 | chép cụm câu trích | Mô hình nào được định nghĩa là sử dụng hàng nghìn tỷ mảnh chữ để dự đoán mảnh ch |
| G04 | thuong | tự viết | ok | ok | ✅ | 2 | 4 | chép cụm câu trích | Khái niệm nào không thuộc nhóm AI phân loại, sinh nội dung hay hành động? |
| G05 | thuong | chatlog T10672 | ok | ok | ✅ | 1 | 19 | — | Quá trình nào giúp cải thiện khả năng của LLM dựa trên phản hồi của con người? |
| G06 | thuong | chatlog T10975 | ok | ok | ✅ | 1 | 20 | — | Khái niệm nào mô tả tình trạng mô hình tạo ra thông tin không chính xác nhưng vẫ |
| G07 | thuong | chatlog T10472 | ok | ok | ✅ | 1 | 29 | — | Khái niệm nào mô tả cách điều chỉnh độ đa dạng trong lựa chọn từ của mô hình? |
| G08 | thuong | chatlog T10511 | ok | ok | ✅ | 1 | 23 | — | Khái niệm nào đúng về agent trong bối cảnh của LLM? |
| G09 | thuong | chatlog T10781 | ok | ok | ✅ | 2 | 22 | — | Khái niệm nào mô tả việc cho phép model suy nghĩ từng bước để đạt được câu trả l |
| G10 | thuong | chatlog T10355 | ok | ok | ✅ | 1 | 26 | — | Khi lựa chọn model AI, điều gì là yếu tố quan trọng nhất mà bạn nên xem xét? |
| H01 | hiem | chatlog T10474 | ok | ok | ✅ | 1 | 8 | chép cụm câu trích | Kỹ thuật nào đã thay đổi cách mà mô hình hiểu ngôn ngữ, cho phép mỗi từ tương tá |
| H02 | hiem | tự viết | ok | ok | ✅ | 1 | 15 | — | Trong một mô hình ngôn ngữ hiện đại, cơ chế nào cho phép mỗi từ xác định mức độ  |
| H03 | hiem | tự viết | ok | ok | ✅ | 1 | 14 | — | Khi sử dụng AI, điều gì mô tả giới hạn mà model có thể tiếp nhận thông tin trong |
| L1-01 | lop1 | tự viết (khái niệm Day 2) | no_evidence / concept_not_in_lecture | no_evidence / concept_not_in_lecture | ✅ | 0 |  | — |  |
| L1-02 | lop1 | tự viết (khái niệm Day 3) | no_evidence / concept_not_in_lecture | no_evidence / concept_not_in_lecture | ✅ | 0 |  | — |  |
| L1-03 | lop1 | tự viết | ok | ok | ✅ | 1 | 26 | — | Trong trường hợp cần kiểm soát chi phí khi sử dụng AI, bạn nên bắt đầu với model |
| L2-01 | lop2 | tự viết | not_enough_data | not_enough_data | ✅ |  |  | — | 2 câu đã trả lời |
| L2-02 | lop2 | tự viết | not_enough_data | not_enough_data | ✅ |  |  | — | 5 câu đã trả lời |
| L2-03 | lop2 | tự viết | no_evidence / invalid_level | no_evidence / invalid_level | ✅ | 0 |  | — |  |
| L3-01 | lop3 | chatlog T00273 (prompt injection) | ok | ok | ✅ | 1 | 3 | lộ đáp án | Khái niệm nào được coi là phạm trù rộng nhất trong các tầng AI? |
| L3-02 | lop3 | chatlog T10515 (đòi đáp án) | ok | ok | ✅ |  |  | — | Khái niệm nào được mô tả là 'chiếc ô lớn nhất' trong hệ thống có yếu tố thông mi |
| L3-03 | lop3 | tự viết | http_404 | http_404 | ✅ |  |  | — |  |
| L4-01 | lop4 | chatlog T10455 | ok | ok | ✅ | 1 | 3 | — | Khẳng định nào sau đây về LLM là đúng? |
| L4-02 | lop4 | chatlog T10427 | ok | ok | ✅ | 1 | 10 | — | Khái niệm nào mô tả đúng về LLM? |
| L4-03 | lop4 | run thử 18/9 (đề chép cụm 'chiếc ô lớn nhất') | ok | ok | ❌ | 2 | 3 | chép cụm câu trích | Khái niệm nào được mô tả là 'chiếc ô lớn nhất' trong hệ thống thông minh? |

## Case fail — lỗi validator ghi lại

- **L4-03**: ok  — `[["câu trích không có nguyên văn trong trang 3"]]`

## Phân tích nguyên nhân (Nam viết sau khi đọc từng case fail)

> ⚠️ **NHÁP do Claude viết từ bản chấm nháp — Nam đọc lại, sửa bằng lời của mình, rồi xoá dòng này.** Cột chấm tay trong CSV đang ghi người chấm là "NHÁP Claude"; Nam/Duy duyệt từng dòng rồi đổi thành tên mình.

**Đạt:** 100% câu có trích dẫn khớp trang slide (18/18); 100% case ① ② ③ xử lý đúng (từ chối khái niệm ngoài slide, không kết luận khi thiếu dữ liệu, không làm theo chỉ thị lạ, không lộ đáp án xuống web).

**1. Mức 3 gần như không hoạt động — 3/4 case mức 3 ra câu nhớ định nghĩa (H01, H02, H03).**
- Nguyên nhân dự đoán: prompt chỉ mô tả mức 3 bằng một dòng trong `level_guide`, không có ví dụ; model nhỏ (`gpt-4o-mini`) mặc định viết câu "Khái niệm nào mô tả…".
- Sửa ở lượt 2: thêm ví dụ câu mức 3 vào prompt, bắt câu mức 3 phải mở đầu bằng một tình huống cụ thể (ai · đang làm gì · cần chọn gì). Cân nhắc thêm kiểm tra tự động "mức 3 phải có tình huống".

**2. Answer key sai 2/18 (89%, bar dự kiến ≥ 90%) — lỗi nằm ở CÁCH ĐẶT CÂU HỎI, không phải bịa kiến thức.**
- G02: hỏi "tầng nào hẹp hơn AI" → cả 4 lựa chọn đều đúng.
- G04: câu phủ định ("không thuộc") + lựa chọn "Predictive AI" nằm ngoài slide và thực chất thuộc nhóm dự đoán → đáp án gây tranh cãi. Prompt đã cấm câu phủ định nhưng model vẫn dùng.
- Validator không bắt được vì câu trích vẫn khớp slide. Sửa ở lượt 2: prompt yêu cầu tự kiểm "mỗi lựa chọn sai phải SAI theo slide, không được đúng một phần"; lựa chọn chỉ dùng thuật ngữ có trên slide. Chấm tay vẫn bắt buộc cho chiều này.

**3. Lệch mức ở mức 2 (G07, L3-01): hỏi nhớ định nghĩa thay vì phân biệt** — cùng nguyên nhân với mục 1.

**4. Chép cụm câu trích 5/18 (G01, L4-03 bị nặng nhất)** — khái niệm `ai_layers` trang 3 chỉ có một câu đặc trưng ("chiếc ô lớn nhất") nên model hay chép lại dù prompt luật 9 đã cấm.

**Ưu tiên sửa trước lượt 2:** (1) mức 3 và (2) answer key, vì đây là 2 chiều hụt hoặc sát bar.
