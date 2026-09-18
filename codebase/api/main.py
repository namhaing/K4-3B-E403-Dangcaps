"""Điểm chạy server:  uvicorn codebase.api.main:app --reload --port 8000"""
from .app import create_app

app = create_app(prefetch=True)  # sinh sẵn câu tiếp theo trong lúc học viên đọc câu hiện tại (giảm chờ sau khi trả lời)
