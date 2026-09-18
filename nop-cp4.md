# Nộp CP4 — VLearn Solo Arena · Nhóm Dangcaps · 3B-E403

> Nội dung để dán vào form CP4 (18/9). Số liệu lấy từ **run-5** — lượt đo trọn bộ 31 case trên bản hiện tại (`eval/run-5.md`, chi tiết `eval/results/run-5.csv`). Spec đầy đủ: `spec.md` §7.

**Repo:** https://github.com/namhaing/K4-3B-E403-Dangcaps (nhánh `main`)

---

## Chuẩn "đạt" của nhóm là gì?

**Một case đạt** khi hệ thống làm đúng hành vi mong đợi: ra câu khi slide có căn cứ, từ chối khi khái niệm không có trong buổi học, báo "chưa đủ dữ liệu" khi dưới 3 câu hoặc trả lời quá nhanh. Nếu ra câu, câu đó phải đạt **cả 4**: trích dẫn khớp nguyên văn đúng trang · chỉ 1 đáp án đúng theo slide · đúng khái niệm và mức khó · không lộ đáp án.

**Quality bar** (khoá 20:40 18/9): ≥ 80% ra câu có trích dẫn khớp trang · ≥ 80% đúng khái niệm · ≥ 90% answer key đúng · ≤ 10% lộ đáp án · ≥ 70% đúng mức khó · 100% case nguồn sự thật (①) và ngoài phạm vi (③). Case không ra được câu vẫn tính trượt.

## Kết quả lượt đo mới nhất (run-5)

31 case Day 1 (`eval/golden-day1.csv`: 16 thường · 3 hiếm · 3 case cho mỗi lớp ①②③④; 14 case từ câu hỏi thật của học viên K4 trong chatlog), chạy trọn bộ bằng AI thật (`openai/gpt-4o-mini`) trên bản hiện tại, không can thiệp tay. Lượt đo thứ 3 trọn bộ (run-1 12:25 · run-2 14:53 · run-5 20:46).

**27/31 case đạt toàn bộ (87%)** — run-2 là 23/31 (74%).

| Chiều | Bar | run-2 | **run-5** |
|---|---|---|---|
| Ra câu, trích dẫn khớp trang | ≥ 80% | 21/24 (88%) | **22/24 (92%)** ✅ |
| Đúng khái niệm | ≥ 80% | 21/21 | **22/22 (100%)** ✅ |
| Answer key đúng | ≥ 90% | 21/21 | **21/22 (95%)** ✅ |
| Lộ đáp án | ≤ 10% | 1/21 (5%) | **1/22 (5%)** ✅ |
| Đúng mức khó | ≥ 70% | 14/21 (67%) khi chấm đúng rubric ❌ | **22/22 (100%)** ✅ |
| Case ① nguồn + ③ ngoài phạm vi | 100% | 6/6 | **6/6** ✅ |
| Case ② chưa đủ dữ liệu | 100% | 3/3 | **3/3** ✅ |

**Mọi chiều đạt bar.** Mức khó tăng nhờ sửa sau run-2: prompt định nghĩa lại mức 2 (phải *phân biệt*, lựa chọn sai là hiểu nhầm có thật) + validator chặn bằng code câu mức 2 dạng "mô tả → gọi tên" rồi cho AI sinh lại.

**4 case chưa đạt:**
- **G05 — sai đáp án:** câu về RLHF đánh dấu đáp án không đúng với slide, và bước AI kiểm chéo (cùng model) cũng hiểu sai nên cho qua. Lỗi nặng nhất vì sẽ chấm oan học viên.
- **G07 — không ra câu:** lần 1 validator chặn nhầm một lựa chọn "Cả hai đều…" có nội dung; lần 2 kiểm chéo chặn đúng (2 đáp án cùng đúng).
- **G09 — không ra câu:** AI 2 lần không chép được câu trích nguyên văn trang 22.
- **L4-03 — lộ đáp án:** đáp án ngắn "AI" nằm trong đề (lỗi đã biết từ run-1).

Chi tiết: `eval/run-5.md` · từng case: `eval/results/run-5.csv` · lịch sử sửa: `spec.md` §9.

## Phần nào chưa làm xong?

- **G05 sai đáp án mà AI kiểm chéo cho qua** — kiểm chéo dùng cùng model nên có thể sai giống bước ra đề; chưa thử model khác.
- 3 case khác chưa đạt: G07, G09 không ra được câu; L4-03 lộ đáp án.
- Chấm tay run-5 chưa được Nam/Duy duyệt; chưa có người ngoài nhóm chấm lại 5 case.
- Chưa chạy bộ 60 case (gồm Day 2); chưa user test với người ngoài nhóm; §3 giải pháp tương tự còn trống.
- Chế độ đấu: đối thủ, rating, bảng xếp hạng là mô phỏng; hồ sơ người chơi còn khởi tạo số liệu mẫu.
