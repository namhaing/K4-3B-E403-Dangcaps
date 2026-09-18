"""Trích text từng trang slide Day 1 -> codebase/data/pages.json

Chạy (từ thư mục gốc repo):
    python codebase/ai/extract_pages.py
    python codebase/ai/extract_pages.py --pdf data/vlearn-pack/slides/d1-slide-hackathon.pdf

pages.json chứa nội dung slide của data pack -> KHÔNG commit (đã chặn trong .gitignore).
Mỗi người tự chạy script này trên máy mình.
"""
import argparse
import json
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF = ROOT / "data" / "vlearn-pack" / "slides" / "d1-slide-hackathon.pdf"
DEFAULT_OUT = ROOT / "codebase" / "data" / "pages.json"

# Dòng chân trang lặp lại ở mọi slide, không mang nội dung
FOOTERS = ("AI IN ACTION - HACKATHON", "AI IN ACTION")


def clean(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and ln not in FOOTERS]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", default=str(DEFAULT_PDF))
    p.add_argument("--out", default=str(DEFAULT_OUT))
    a = p.parse_args()

    doc = fitz.open(a.pdf)
    pages = {str(i + 1): clean(page.get_text()) for i, page in enumerate(doc)}

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    empty = [k for k, v in pages.items() if len(v) < 50]
    print(f"Đã ghi {len(pages)} trang -> {out}")
    if empty:
        print(f"Cảnh báo: trang gần như không có chữ (có thể là ảnh): {empty}")


if __name__ == "__main__":
    main()
