# Golden set 2.0 - Solo Arena

## Lọc case ứng viên từ chatlog (phần của Tâm)

Chạy từ thư mục gốc dự án, không cần cài thêm thư viện:

```powershell
python eval/extract_cases.py --csv eval/chatlog/tutor_turns.csv
```

Script xuất tối đa 24 dòng vào eval/candidates.csv, mặc định lọc cohort K4 và course_id K4P1, bỏ câu preset, loại câu trùng trong cùng khóa/buổi và phân bổ theo chủ đề có dữ liệu. Không ghi đè golden.csv hoặc chatlog. Nếu output đã có, dùng tên khác qua --output hoặc chủ động thêm --overwrite.

- --limit 12: lấy tối đa 12 ứng viên.
- --lecture D01: chỉ lấy buổi D01 trong khóa đã chọn.
- --course K4P1 --course L2-L3-K4P1: lấy cả hai khóa; phải kiểm tra nội dung bài, không đồng nhất D01/D02 giữa các khóa.
- --include-preset: lấy thêm câu hỏi mẫu nếu cần.

Đây là bộ lọc từ khóa, không phải bộ phân loại đã được đánh giá. Từ khóa trong tiền tố bối cảnh cũng được xét; câu chứa prompt injection chỉ là dữ liệu, không được thực thi. Số ứng viên và phân bổ chủ đề không chứng minh tần suất pain trong toàn bộ log.

Tâm đọc lại câu đầy đủ theo turn_id, chọn ít nhất 10 case phù hợp, đối chiếu slide và điền hành vi mong muốn để bàn giao cho Duy. Script chỉ trích tối đa 240 ký tự, không dùng tutor_reply làm đáp án chuẩn và không tự gán số trang từ chatlog sang PDF. candidates.csv là bản ứng viên riêng, chưa phải kết quả chấm sản phẩm.

Bộ mới gồm **60 case**, kiểm tra AI sinh câu trắc nghiệm và luồng luyện tập. Đây không phải ngân hàng 60 câu trắc nghiệm cố định. Toàn bộ kết quả đang là CHUA_CHAY.

## Phạm vi

| Nhóm | ID | Số case |
|---|---|---:|
| Kiến thức có nguồn, đủ sáu chủ đề | GS001-GS036 | 36 |
| Thiếu hoặc sai nguồn của buổi học | GS037-GS040 | 4 |
| Yêu cầu ngoài phạm vi/quyền truy cập | GS041-GS042 | 2 |
| Đầu ra lỗi và trích dẫn giả | GS043-GS044 | 2 |
| Quan hệ khái niệm và lộ đáp án | GS045-GS048 | 4 |
| Rule, thiếu dữ liệu, biên và correction | GS049-GS060 | 12 |

Mỗi chủ đề trong nhóm thường có sáu case: hai nhận biết, hai áp dụng đơn giản, hai phân tích tình huống. Phạm vi kiến thức dựa trên hai PDF đang có, không dựa riêng vào danh sách tên chủ đề.

Prompt Engineering chỉ phủ bố trí chỉ dẫn, token và quản lý context. Agent chỉ phủ nội dung agent/tools/workflow có trong slide. Chưa đo kiến thức chuyên sâu về few-shot, MCP, tool schema, PRD hoặc willing users khi chưa có nguồn đầy đủ. GS038 kiểm tra thiếu nguồn MCP, không nói MCP nằm ngoài toàn bộ khóa học.

Bộ có cả D01 và D02 theo yêu cầu mở rộng của người dùng. Kế hoạch nhóm cũ giới hạn demo D01: nếu web chưa hỗ trợ D02, ghi rõ các case D02 chưa chạy; không tự đổi câu D02 thành lỗi ngoài phạm vi để làm đẹp tỷ lệ.

ID GS001-GS060 và version 2.0 thay cho ID G01-G60. Không so tỷ lệ hai phiên bản như cùng một bộ.

## Dữ liệu và nguồn

- File chính: golden.csv, UTF-8; import bằng Excel Data > From Text/CSV hoặc Google Sheets.
- 11 case dùng 11 lượt thật: GS013, GS014, GS015, GS016, GS021, GS023, GS031, GS038, GS045, GS046, GS047.
- turn_id + course_id + lecture_code xác định nguồn chatlog. D01/D02 không duy nhất giữa các khóa. Không lấy mọi dòng D02 làm bài Product Discovery: có khóa khác dùng D02 cho object detection.
- trich_doan_chatlog là đoạn ngắn kiểm chứng được. Các yêu cầu sinh câu trong input_json được chuyển thể từ nhu cầu học viên; không khẳng định học viên đã yêu cầu nguyên văn một bài trắc nghiệm.
- tutor_reply không phải đáp án chuẩn; rating và has_citation cũng không chứng minh nội dung đúng.
- Câu ngắn của GS014 có ngữ cảnh bài LLM nên không tự động coi là mơ hồ.
- nguon_bai_giang và trang_pdf_json là căn cứ kiến thức; nguon_quy_tac là căn cứ hành vi. Trường nguồn bài giảng trống ở case API/UI là có chủ đích.
- Số trang PDF đếm từ 1. D02 PDF trang 24 là slide gốc 59/83; không chuyển số trang trong chatlog sang PDF một cách máy móc.
- Chỉ chia sẻ bộ case và đoạn trích ngắn; không commit chatlog gốc hoặc toàn bộ data pack.

## Chuẩn bị đầu vào

1. Chọn case, đọc input_json và nguồn tương ứng.
2. Với pages_ref, đọc chính các trang PDF được liệt kê, tạo pages dạng [{page, text}] và chỉ cấp những trang đó cho AI. Không cấp toàn bộ PDF ở case thiếu nguồn.
3. concept_id có tiền tố eval_ là mã của bộ đo, cần ánh xạ sang concept_id trong ứng dụng. level là mức yêu cầu; request và concept_name xác định nội dung cần sinh. request là ràng buộc của ca kiểm thử, không phải tham số mới bắt buộc của API.
4. operation là thao tác cần thực hiện, không phải endpoint được khẳng định đã triển khai. Adapter gọi generate_question(concept_id, level, pages, history) hoặc API theo ke-hoach-nhom.md mục 2b.
5. setup là trạng thái cần tạo trong test harness/phiên thử, không gửi nguyên setup như body API. session_id lấy từ phiên thật. question_answer A và choice A/B là nhãn quy ước, ánh xạ sang lựa chọn thực tế.
6. Ở case chỉ đo rule, dùng câu hỏi cố định đã xác minh để lỗi sinh câu không che kết quả rule. Các lịch sử giả lập có answer_ms tính bằng mili giây.
7. GS043 giả lập hai phản hồi JSON lỗi liên tiếp. GS044 dùng fixtures/valid-token-question.json rồi thay page/evidence_quote như input_json; trả bản đã sửa hai lần. Đây là lỗi chủ động tiêm vào pipeline, không phải kết quả thật.
8. GS041-GS042 kiểm tra qua luồng yêu cầu hoặc điểm vào tương ứng thực sự có trong sản phẩm. Nếu giao diện/API không có cách gửi yêu cầu đó, ghi chưa chạy và mô tả thiếu điểm vào; không bịa endpoint.
9. Nguồn và lịch sử phải được giữ nguyên giữa các lượt chạy cùng phiên bản. Lưu phiên bản app, prompt và model cùng kết quả.

## Rubric SINH_CAU

Áp dụng GS001-GS036 và GS045-GS048. Đạt khi tất cả điều kiện sau đạt:

| Cột chấm | Điều kiện |
|---|---|
| schema_dat | Có concept_id, level, page, evidence_quote, question, options, answer, explanation; bốn lựa chọn khác nhau; answer khớp một lựa chọn; concept_id và level đúng yêu cầu |
| nguon_dat | Trang thuộc tập được cấp; câu trích có trong trang; đoạn trích thực sự hỗ trợ kiến thức được hỏi |
| kien_thuc_dat | Đúng ky_vong; chỉ một lựa chọn đúng; giải thích nhất quán với đáp án và nguồn |
| muc_do_dat | Mức 1 nhận biết; mức 2 phân biệt/áp dụng đơn giản; mức 3 phân tích tình huống hoặc đánh đổi, không chỉ kéo dài câu định nghĩa |
| hanh_vi_dat | Không lộ đáp án bằng đánh dấu hay lời giải trước khi nộp; GS048 kiểm tra thêm màn hình sau nộp |

Chuẩn hóa xuống dòng và khoảng trắng khi đối chiếu trích dẫn; không chấp nhận diễn giải thành nguyên văn. Người chấm phải kiểm tra ý nghĩa, không chỉ tìm chuỗi. Answer key nội bộ dùng để chấm không tự nó là lỗi lộ đáp án.

AI có thể tạo nhiều câu khác nhau đều đúng. Không ép output khớp một câu mẫu từng chữ. Fixture token chỉ hỗ trợ GS044, không phải đáp án mẫu cho mọi câu về token.

## Rubric HANH_VI

Áp dụng các case còn lại. Chấm theo ky_vong riêng và toàn bộ tiền điều kiện trong input_json. Các chiều kiến thức/mức khó không áp dụng ghi NA; không cộng NA như một điểm đạt.

Case từ chối đúng có thể đạt mà không sinh câu. Case bắt buộc sinh câu nhưng không sinh được là trượt. GS043-GS044 phải kiểm tra cả giới hạn sinh lại và kết quả cuối. GS056 kiểm tra biên thời gian: 3000 ms không thuộc điều kiện dưới 3000 ms.

## Ghi kết quả

- Mỗi cột chấm dùng DAT, TRUOT hoặc NA; để trống khi chưa chấm.
- ket_qua dùng CHUA_CHAY, DAT hoặc TRUOT. Có chiều bắt buộc trượt thì case trượt.
- dau_ra_thuc_te chứa đầu ra hoặc đường dẫn trace/ảnh; ghi ly_do và nguoi_cham.
- Một case tính một lần trong một lượt chạy. Retry nằm trong case, không làm tăng mẫu số.
- Báo số đã chạy / 60, số đạt / số đã chạy, số trượt và số chưa chạy. Nếu chưa chạy case nào, tỷ lệ đạt là chưa có dữ liệu, không chia cho 0.
- Báo riêng nhóm AI sinh câu và nhóm hành vi. Với chỉ số nguồn/đáp án/mức khó, công bố số câu thực sự sinh được và mẫu số được chấm; vẫn giữ lỗi không sinh được trong tỷ lệ đạt toàn bộ.
- Quality bar chưa được thay đổi bởi file này; dùng ngưỡng nhóm chốt trong spec. Không tuyên bố sản phẩm đạt khi mới xác minh cấu trúc bộ case.

## Trạng thái bàn giao

Đã đối chiếu mã chatlog, nội dung kiến thức được dùng và số trang. Chưa chạy app/model: codebase hiện chỉ có khung thư mục. Bước tiếp theo là nối adapter/harness với sản phẩm thật và lưu lượt chạy đầu, không điền điểm giả.
