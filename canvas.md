# A2 · VLearn Solo Arena

| # | Dòng | Nội dung |
|---|---|---|
| 1 | Track + đề | **A2 · Tính năng AI mới trên VLearn — VLearn Solo Arena** |
| 2 | Job executor (ai · đang ở đâu · làm gì) | **Học viên · sau buổi học · làm bài test xếp hạng rồi tham gia một trận đấu ngắn với người có trình độ tương đương.** |
| 3 | Pain một câu (ai – đang làm gì – vướng đâu – hậu quả) | **Học viên khi tự ôn sau buổi học không biết trình độ hiện tại của mình và thường gặp đối thủ quá mạnh hoặc quá yếu, nên trận đấu thiếu công bằng, nhanh mất động lực và không giúp ôn đúng mức.** |
| 4 | 1–2 bằng chứng đầu | **Cần bổ sung từ data pack:** số học viên có câu hỏi/sai bài tập lặp lại sau buổi học, kèm mã hội thoại hoặc tin nhắn. **Cần khảo sát/phỏng vấn:** hỏi ít nhất 5 học viên; ghi số người gặp pain và 1–2 câu trích dẫn ngắn. Không dùng số liệu giả. |
| 5 | Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả) | **Một học viên mới · hoàn thành bài test xếp hạng · AI ước lượng rank kèm độ tin cậy và ghép một đối thủ cùng thực lực · học viên chơi trận 1v1 công bằng, nhận bonus nếu thắng và biết một chủ đề cần ôn lại.** |
| 6 | AI tự làm đến đâu + lý do · ≥3 willing users ngoài nhóm | **AI điều chỉnh độ khó của bài test, đề xuất rank, ghép đối thủ, chọn/tạo biến thể câu hỏi và giải thích kết quả dựa trên dữ liệu có căn cứ; giảng viên quyết định kiến thức được kiểm tra, duyệt ngân hàng câu hỏi và bật/tắt trận vì giảng viên là người chịu trách nhiệm nội dung dạy.** Cần xác nhận willingness với ít nhất 3 học viên ngoài nhóm. |
| 7 | Phân công có tên | **Nguyễn Trần Bảo Tâm** — thu 30 bài trả lời test thật và phối hợp gán nhãn trình độ bằng tay làm đáp án chuẩn · **Trần Thị Thu Hiền** — prototype form test xếp hạng, AI call chấm trình độ và ghép trận · **Bùi Phương Duy** — tạo golden set từ bộ đã gán nhãn, đặt quality bar và eval độ chính xác của rank/mức độ phù hợp của trận ghép · **Nguyễn Hải Nam** — spec tính năng, canvas, slide và demo luồng test → xếp rank → ghép trận → nhận bonus. |

## Phạm vi MVP

- Trước trận đầu tiên, học viên làm bài test xếp hạng thích ứng gồm khoảng 10–15 câu từ kiến thức giảng viên đã duyệt.
- AI bắt đầu bằng câu mức trung bình rồi tăng hoặc giảm độ khó theo câu trả lời để ước lượng trình độ.
- Kết quả gồm một rank cá nhân và độ tin cậy; nếu độ tin cậy thấp, hệ thống yêu cầu thêm câu hỏi trước khi ghép trận xếp hạng.
- AI ưu tiên ghép người cùng rank; chỉ mở rộng sang rank liền kề khi thời gian chờ vượt ngưỡng đã định.
- Trận 1v1 gồm 5 câu, kéo dài khoảng 3 phút.
- Người thắng nhận **Win Bonus** gồm điểm kinh nghiệm và xu để mở huy hiệu hoặc vật phẩm trang trí; phần thưởng không mua được đáp án hay lợi thế trong trận.
- Cả hai người chơi vẫn nhận điểm hoàn thành; người thua không bị trừ thưởng học tập để tránh mất động lực.
- Chuỗi thắng có bonus tăng nhẹ nhưng có mức trần; kết quả trước cùng một đối thủ bị giảm thưởng để hạn chế việc “farm” điểm.
- Rank được cập nhật dần từ kết quả nhiều trận, không bị “đóng đinh” bởi một bài test duy nhất.
- Không công khai điểm yếu, câu trả lời trong bài test hoặc dữ liệu chi tiết dùng để ghép trận.
- Người chơi dùng biệt danh ẩn danh.
- Nội dung chỉ đến từ slide, bài tập và dữ liệu nằm trong pack.
- Giảng viên duyệt chủ đề và ngân hàng câu hỏi trước khi mở trận.
- Sau trận, AI chỉ nhận xét điều có bằng chứng, ví dụ: “Bạn sai 2 câu về vòng lặp”. Nếu thiếu dữ liệu, AI ghi rõ “Chưa đủ dữ liệu để đánh giá”.

## Hard tests

| Tình huống | Cách xử lý |
|---|---|
| Lớp hỏi ít, data thưa | Dùng bài test xếp hạng làm tín hiệu khởi đầu; hiển thị độ tin cậy thấp và cập nhật rank sau các trận tiếp theo. |
| Câu hỏi mẫu chiếm đa số | Giảm trọng số câu mẫu, nhận diện câu trùng và tạo biến thể kiểm tra cùng khái niệm thay vì học thuộc đáp án. |
| Hai trang cùng nói một khái niệm | Gom nội dung theo `concept_id`, không coi mỗi trang là một lỗ hổng riêng và tránh hỏi trùng trong cùng trận. |
| Signal nhiễu do một người hỏi 20 lần | Giới hạn trọng số đóng góp của mỗi học viên theo từng khái niệm; không để một người làm sai lệch độ khó chung. |
| Không tìm được đối thủ phù hợp | Mở chế độ đấu với AI hoặc xếp hàng chờ; không ghép chênh lệch lớn chỉ để bắt đầu nhanh. |
| Học viên đoán mò hoặc làm bài test bất thường | Kiểm tra độ nhất quán giữa độ khó, thời gian trả lời và kết quả; yêu cầu thêm câu thay vì kết luận chắc chắn hoặc tự động phạt. |
| Học viên tiến bộ nhưng rank cũ quá thấp | Cập nhật rank sau nhiều trận gần nhất và cho phép làm lại bài test sau một khoảng thời gian hợp lý. |
| Hai người cố tình đấu lại để farm bonus | Giảm hoặc khóa Win Bonus khi hai tài khoản gặp nhau liên tục; ưu tiên ghép với đối thủ mới cùng trình độ. |
| Bonus khiến học viên chỉ quan tâm thắng thua | Giữ phần thưởng ở mức nhỏ, vẫn thưởng cho việc hoàn thành và hiển thị nội dung cần ôn như kết quả chính của trận. |

## An toàn và đạo đức

- Không hiển thị ai đã hỏi gì, ai yếu phần nào hoặc dữ liệu cá nhân dùng để ghép trận.
- Không đưa dữ liệu học viên ra ngoài data pack.
- Không xếp hạng công khai; kết quả chi tiết chỉ thuộc về từng học viên và giảng viên có quyền phù hợp.
- Bonus chỉ là phần thưởng động lực và vật phẩm trang trí, không được tạo lợi thế học tập hoặc lợi thế thi đấu kiểu “pay-to-win”.
- Rank chỉ phản ánh năng lực trong phạm vi kiến thức đã kiểm tra, không được mô tả như năng lực tổng quát của học viên.
- AI không khẳng định mức hiểu khi thiếu căn cứ và phải nêu giới hạn của đánh giá.
- AI chỉ đề xuất; giảng viên là người quyết định nội dung dạy và nội dung được đưa vào trận.
