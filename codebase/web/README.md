# Frontend — VLearn Solo Arena

Frontend tĩnh, không cần cài package hoặc build.

## Chạy frontend độc lập — không cần data, API hoặc key

```powershell
python -m http.server 5173 --directory codebase/web
```

Mở `http://localhost:5173`, sau đó chọn **Xem demo frontend**. Chế độ này dùng câu hỏi mẫu nằm trong `app.js`, luôn gắn thông báo DEMO và không gọi AI.

## Chuẩn bị lần đầu

Từ thư mục gốc repo:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r codebase\api\requirements.txt -r codebase\ai\requirements.txt
```

API cần `codebase/data/pages.json`. Nếu data pack nằm đúng vị trí mặc định:

```powershell
.\.venv\Scripts\python.exe codebase\ai\extract_pages.py
```

Nếu PDF nằm ở chỗ khác:

```powershell
.\.venv\Scripts\python.exe codebase\ai\extract_pages.py --pdf "C:\duong-dan\d1-slide-hackathon.pdf"
```

Để thử giao diện mà chưa gọi AI thật, copy `.env.example` thành `.env` và đặt `LLM_PROVIDER=mock`.

## Chạy local

Từ thư mục gốc repo, mở hai terminal:

```powershell
# Terminal 1 — backend
.\.venv\Scripts\python.exe -m uvicorn codebase.api.main:app --reload --port 8000

# Terminal 2 — frontend
python -m http.server 5173 --directory codebase/web
```

Mở `http://localhost:5173`.

Frontend mặc định gọi `http://localhost:8000`. Có thể đổi bằng nút **Thiết lập kết nối**, hoặc query string:

```text
http://localhost:5173/?api=http://127.0.0.1:8000
```

## Luồng đã hỗ trợ

- Bắt đầu lượt luyện Day 1.
- Chọn và nộp đáp án; đo `answer_ms` từ lúc câu được hiển thị.
- Hiện đúng/sai, giải thích, trang và câu trích sau khi nộp.
- Luyện thường: đổi câu cùng chủ đề/mức qua `/skip`; chế độ đấu không hiển thị chức năng đổi câu.
- Báo câu sai với ba lý do qua `/report`.
- Thông báo khi API tự đổi chủ đề vì thiếu căn cứ.
- Màn `no_evidence`, `not_enough_data`, lỗi kết nối và kết quả cuối lượt.
- Chế độ **Đấu Solo 1v1**: tìm đối thủ, bảng điểm từng vòng và kết quả thắng/thua. Đối thủ hiện là mô phỏng frontend vì backend chưa có tài khoản, phòng đấu hoặc WebSocket.
- **Bảng xếp hạng mùa**: top 3, danh sách người chơi, hạng cá nhân, bậc rank và rating cộng/trừ sau trận. Hồ sơ prototype được lưu bằng `localStorage` trên trình duyệt.
- Điều khiển bàn phím: phím `1`–`4` chọn đáp án, `Enter` để nộp.

Không có đáp án hoặc explanation nào được nhúng sẵn trong frontend; chúng chỉ xuất hiện sau phản hồi của `/answer`.
