# Log dùng thử — 5 người ngoài nhóm

> Người phụ trách: **Duy (D)** (giao lại 21:15 18/9, trước là Tâm). Kết quả đưa lên **slide 5 (Validation)** và `spec.md` §8.
> **Chưa có buổi nào thì để trống bảng và ghi "chưa làm" — không điền số hay câu nói không có thật.**

## Chuẩn bị (trước khi mời người thử)

- Máy của nhóm chạy server với AI thật: `uvicorn codebase.api.main:app --port 8000`, **bật trước ~20 giây** cho câu đầu sinh sẵn xong. Mở `http://localhost:8000/app/`.
- **Mỗi người một cửa sổ ẩn danh mới** (InPrivate / Incognito) → mã học viên và bản đồ chỗ yếu không lẫn với người trước.
- Xin phép trước: "Mình ghi lại chỗ bạn thấy khó và vài câu bạn nói, không ghi tên thật nếu bạn không muốn."
- Ưu tiên 2 người đã khai là willing user ở CP1.

## Cách quan sát

- Đọc task cho người thử, **không giải thích giao diện**, rồi ngồi im quan sát.
- Người thử kẹt quá ~60 giây → ghi "kẹt" vào bảng rồi mới gợi ý.
- Ghi **câu nói nguyên văn** (đặt trong ngoặc kép), không tóm tắt lại bằng lời mình.

## Task giao cho người thử

| Task | Câu đọc cho người thử | Hoàn thành khi |
|---|---|---|
| T1 | "Bạn vừa học xong buổi Day 1. Hãy làm một lượt luyện tập." | Làm xong 5 câu, thấy màn kết quả |
| T2 | "Theo app, bạn nên ôn lại phần nào? Hãy mở phần đó ra xem." | Tìm được chủ đề cần ôn / mở "Ôn lại kiến thức" hoặc "Xem slide" |
| T3 (1–2 người) | "Thử chế độ Ghép trận 1v1." | Đấu xong 5 vòng |

Hỏi thêm cuối buổi (ghi nguyên văn): **"Chỗ nào khó hiểu nhất?"** · **"Sau buổi học bạn có dùng lại cái này không? Vì sao?"**

Để ý riêng: có ai **hết giờ** ở chế độ đấu (3 s đọc đề + 10 s trả lời) · có hiểu dòng **"Chưa đủ dữ liệu"** không · có tìm thấy **trích dẫn / "Xem slide"** không.

## Bảng log

| # | Ai (mã · mô tả ngắn, VD "N1 · học viên K4") | Task | Hoàn thành? (có/không · mất bao lâu) | Kẹt ở đâu | Câu nói nguyên văn | Nhóm quyết định gì (sửa / giữ / để dành) |
|---|---|---|---|---|---|---|
| 1 |Minh-học viên khóa 4 |1 |Có-2 phút |sai câu lựa chọn mô hình ở các tầng | |để dành |
| 2 |Minh-học viên khóa 4 |2 |không|không mở được slide|Máy chủ không có file slide gốc |sửa |
| 3 |Minh-học viên khóa 4 |3 |có-2 phút |thời gian nhanh quá |thời gian đọc nhanh quá |sửa |
| 4 |Phi-học viên khóa 4 |1 |có-2 phút |chưa xác thực được chất lượng câu hỏi |bạn duy ơi mình cảm thấy về các câu hỏi này được llm sinh ra liệu có chất lượng hơn quiz sẵn có của vlearn hay không |xem xét |
| 5 |Phi-học viên khóa 4 |3 |có-2 phút |làm không kịp vì thời gian quá nhanh |hãy thêm các độ khó phù hợp tương ứng với thời gian: dễ, trung bình, khó |sửa |
| 6 |Linh-học viên khóa 4 |2 |có-2 phút |Tìm nút xem lại bài hơi lâu|"Nút 'Xem slide' bé quá, mình nhìn lướt qua không thấy, |sửa |
| 7 |Tuấn-học viên khóa 4 |3 |không |Hết giờ trước khi kịp đọc xong đề và đáp án|Trời ơi chưa kịp đọc xong đề nó đã đếm ngược xong rồi, thua luôn. |sửa |
| 8 |Hương-học viên khóa 4 |2 |có-1 phút |Không kẹt|Bấm vào trích dẫn nó nhảy đúng trang slide này tiện ghê, sau này ôn thi nhàn hẳn|giữ |

## Tổng kết (viết sau khi đủ 5 người)

- **Chủ đề lặp lại nhiều nhất:**Ở task 3 chế độ solo thời gian trôi nhanh quá không kịp đọc câu hỏi và câu trả lời
- **Sửa gì trước demo:**Sửa thời gian cho phù hợp
- **Giữ gì và vì sao:** Luồng làm một lượt luyện tập (task 1) — cả Minh và Phi đều hoàn thành trong ~2 phút, không kẹt nghiêm trọng, giữ nguyên.
- **Để dành gì (backlog):** (1) Chất lượng câu hỏi do LLM sinh so với quiz sẵn có của VLearn — Phi đặt nghi vấn, cần đánh giá thêm sau demo. (2) Phân độ khó (dễ/trung bình/khó) tương ứng thời gian đọc — Phi đề xuất, có thể làm ở bản sau nếu không kịp sửa trước 22:30. (3) Cách chọn mô hình ở các tầng bị Minh chọn sai (task 1) — chưa rõ do UI khó hiểu hay do thao tác, cần xem lại sau.
