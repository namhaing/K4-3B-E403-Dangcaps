# Nộp CP3 — VLearn Solo Arena · Nhóm Dangcaps · 3B-E403

> Nội dung để dán vào form CP3 (16:00 · 18/9). Số liệu lấy từ **run-2** — `eval/run-2.md`, chi tiết từng case ở `eval/results/run-2.csv`.

**Repo:** https://github.com/namhaing/K4-3B-E403-Dangcaps
**Video 30 giây:** `<dán link video>`

---

## Đã thử bao nhiêu lần?

31 tình huống trong golden set (`eval/golden-day1.csv`), chạy trọn bộ bằng AI thật (`openai/gpt-4o-mini`), không can thiệp tay.

- 16 case thường · 3 case hiếm · 3 case cho mỗi lớp chỗ khó ① nguồn sự thật, ② thiếu dữ liệu, ③ ngoài phạm vi, ④ đặc thù domain
- 14 case lấy từ câu hỏi thật của học viên K4 trong chatlog (ghi `turn_id`)
- Đây là lượt đo thứ 2. Lượt 1 chạy 25 case lúc 12:25; lượt 2 chạy 31 case lúc 14:53 sau khi sửa theo lỗi của lượt 1.

## Trong đó bao nhiêu lần đạt?

**23/31 case đạt (74%).**

| Chiều | Kết quả |
|---|---|
| Câu hỏi có câu trích khớp nguyên văn đúng trang slide | 21/21 câu đã sinh (100%) |
| Đáp án thật sự đúng, chỉ 1 đáp án đúng (người chấm) | 21/21 (100%) |
| Đúng mức khó yêu cầu (người chấm) | 17/21 (81%) |
| Đề không lộ đáp án | 20/21 (95%) |
| Case ngoài phạm vi / thiếu dữ liệu / chèn lệnh xử lý đúng | 9/9 (100%) |
| Ra được câu hỏi khi cần | 21/24 (88%) |

## Chuẩn "đạt" của nhóm là gì?

Một case **đạt** khi hệ thống làm đúng hành vi mong đợi của case đó:
- ra câu hỏi khi slide có căn cứ;
- từ chối khi khái niệm không có trong slide buổi học;
- báo "chưa đủ dữ liệu để đánh giá" khi học viên mới làm dưới 3 câu hoặc trả lời quá nhanh (đoán mò);
- không làm theo chỉ thị lạ chèn vào dữ liệu, không gửi đáp án xuống trình duyệt.

Nếu có ra câu hỏi, câu đó phải đạt **cả 4 điều kiện**:
1. Câu trích chép nguyên văn từ đúng trang slide (code kiểm tra).
2. Chỉ đúng 1 đáp án đúng theo slide (người chấm theo `eval/rubric-cham-tay.md`).
3. Đúng khái niệm và đúng mức khó yêu cầu (người chấm).
4. Đề không lộ đáp án (code kiểm tra).

**Quality bar dự kiến** (khoá chính thức ở CP4, 21:00): ≥ 80% trích dẫn khớp trang · ≥ 90% đáp án đúng · ≤ 10% lộ đáp án · ≥ 70% đúng mức khó · 100% case ngoài phạm vi xử lý đúng.

## Những lần chưa đạt sai ở đâu?

8 case chưa đạt, thuộc 3 nhóm lỗi:

1. **Sai mức khó — 4 case (G02, G08, L3-01, T-G25).** Yêu cầu mức 2 "phân biệt" nhưng AI ra câu nhớ định nghĩa (mức 1), ví dụ *"tầng nào rộng nhất?"*. Nguyên nhân: model nhỏ; prompt chưa có ví dụ mẫu cho mức 2 (mức 3 đã có ví dụ và đạt 6/6).
2. **Không ra được câu — 3 case (G04, G10, T-G07).** Bước AI kiểm chéo chặn các câu có 2 đáp án đúng hoặc dùng lựa chọn gộp *"Cả ba…"*. Nhóm đã đọc từng case: cả 3 đều **chặn đúng**. Đây là đánh đổi có chủ đích — không ra câu còn hơn ra câu chấm oan học viên. Trong app, khái niệm bị chặn thì hệ thống tự chuyển sang khái niệm khác.
3. **Gợi ý lộ đáp án — 1 case (L4-03).** Đề chép cụm *"chiếc ô lớn nhất"* từ slide, đáp án ngắn *"AI"* nằm ngay trong đề.

**Đã sửa sau lượt 1** (ghi ở `spec.md` §9 Changelog):
- Thêm bước **AI kiểm chéo** (giải lại câu mà không biết đáp án). Nguyên nhân: case AI hiểu tiêu đề slide *"Ba nhóm AI chính"* thành tên một nhóm, đáp án *"AI chính"* → học viên chọn đúng bị chấm sai. Câu có nhiều đáp án đúng: 2/18 → **0/21**.
- Prompt bắt buộc mức 3 có tình huống thực tế: 1/4 → **6/6**.
- Sửa luật chọn khái niệm: chạy app thật thấy 29 trang slide chỉ hỏi tới 7 trang → xáo khái niệm mỗi lượt, sai 2 lần thì chuyển → 3 lượt thử phủ 11 trang.

**Minh chứng trong repo:** `eval/run-1.md`, `eval/run-2.md` (bảng kết quả + phân tích) · `eval/golden-day1.csv` (bộ đề) · `eval/traces/` (log lời gọi AI thật) · `spec.md` §9 (lịch sử sửa).
