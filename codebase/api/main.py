"""Điểm chạy server:  uvicorn codebase.api.main:app --reload --port 8000"""
from .app import create_app

app = create_app()
