# Golden set cho web học AI

Bộ gồm 60 case dựa trên 6 chủ đề người dùng cung cấp: 36 case thường (mỗi chủ đề có 6 case, hai case cho mỗi mức), 24 case khó và biên. Phạm vi này theo yêu cầu mới, rộng hơn giới hạn Day 1 trong kế hoạch cũ.

## Trước khi chạy

- Mở golden.csv bằng Excel (Data > From Text/CSV, chọn UTF-8) hoặc import vào Google Sheets.
- Đây là bộ yêu cầu kiểm thử, không phải ngân hàng câu hỏi trắc nghiệm có sẵn.
- Tất cả case là tự thiết kế; chưa lấy từ chatlog, chưa đối chiếu bài giảng, chưa chạy sản phẩm.
- Điền nguon_bai_giang và trang_hoac_muc bằng nguồn thật. Kiểm tra kỳ vọng với bài giảng rồi đổi trang_thai_nguon thành DA_DOI_CHIEU. Không bịa số trang.
- Nếu vẫn áp dụng yêu cầu của kế hoạch nhóm về ít nhất 10 case từ chatlog, thay hoặc bổ sung case từ log thật, ghi mã hội thoại vào nguon_case. Bộ hiện tại chưa đáp ứng yêu cầu nguồn đó.
- Các case API/UI dùng rule trong kế hoạch nhóm. Xác nhận rule còn áp dụng cho sản phẩm trước khi khóa bộ.

## Cách chấm

Với case sinh câu, ngoài ky_vong riêng của dòng, yêu cầu:
1. Đúng khái niệm; bốn lựa chọn và chỉ một đáp án đúng.
2. Đáp án và giải thích đúng kiến thức, được nguồn bài giảng hỗ trợ.
3. Nguồn dẫn tồn tại, trích dẫn khớp và liên quan tới nội dung.
4. Đúng mức yêu cầu: mức 1 nhận biết; mức 2 phân biệt hoặc áp dụng đơn giản; mức 3 phân tích tình huống và đánh đổi.
5. Không lộ đáp án trên màn hình trước khi nộp bài. Answer key nội bộ để chấm không tự nó là lỗi lộ đáp án.

Người chấm kiểm tra nội dung và mức khó; kiểm tra chuỗi trích dẫn bằng code không thay thế kiểm tra đúng nghĩa. Với case hành vi, chấm kỳ vọng riêng và tiền điều kiện, không áp tiêu chí sinh câu khi hệ thống cần từ chối.

## Chạy và báo cáo

1. Chốt đầu vào, nguồn và kỳ vọng trước lượt chạy. Ghi phiên bản ứng dụng, model, prompt và ngày chạy.
2. Chạy qua kênh ghi ở kenh_kiem_thu. Case timeout cần giả lập lỗi; case lịch sử cần tạo phiên tương ứng.
3. Lưu đầu ra hoặc đường dẫn trace vào dau_ra_thuc_te. Ghi DAT hoặc TRUOT vào ket_qua, kèm lý do và người chấm.
4. Case chưa đủ nguồn hoặc chưa thể chạy giữ CHUA_CHAY; không tính là đạt.
5. Báo cáo số đã chạy / 60, số đạt / số đã chạy và số chưa chạy. Báo riêng tỷ lệ đúng đáp án, đúng nguồn, đúng mức và xử lý tình huống khó với mẫu số tương ứng.
6. Case yêu cầu sinh câu mà không sinh được vẫn là trượt, không loại khỏi báo cáo để làm đẹp số.
7. Giữ cùng bộ cho lần chạy sau; ghi lại mọi thay đổi case và lý do.

Quality bar cần được nhóm chốt trước khi đánh giá; file này không tự thay đổi quality bar trong spec. Chưa có kết quả thực nghiệm.
