"""Lớp gọi LLM — đổi nhà cung cấp chỉ bằng biến môi trường, code còn lại không đổi.

.env (ở thư mục gốc repo):
    LLM_PROVIDER=openai        # openai | gemini | mock
    LLM_MODEL=gpt-4o-mini      # tên model của nhà cung cấp đó
    LLM_API_KEY=...

LLM_PROVIDER=mock: KHÔNG gọi AI thật, trả JSON dựng từ text slide.
Chỉ dùng để test code offline / cho web & API chạy thử. Không dùng để quay video CP3 hay chạy eval.
"""
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
MODEL = os.getenv("LLM_MODEL", {"openai": "gpt-4o-mini", "gemini": "gemini-2.0-flash"}.get(PROVIDER, "mock"))
TEMPERATURE = 0.7  # đủ đa dạng để "Cho tôi câu khác" ra câu mới; validator chặn phần bịa


def call_json(system: str, user: str) -> dict:
    """Gửi prompt, bắt model trả JSON, parse thành dict. Lỗi mạng/parse -> raise để generator xử lý."""
    if PROVIDER == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("LLM_API_KEY"), timeout=30)
        resp = client.chat.completions.create(
            model=MODEL,
            temperature=TEMPERATURE,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return json.loads(resp.choices[0].message.content)

    if PROVIDER == "gemini":
        import google.generativeai as genai

        genai.configure(api_key=os.getenv("LLM_API_KEY"))
        model = genai.GenerativeModel(MODEL, system_instruction=system)
        resp = model.generate_content(
            user,
            generation_config={"response_mime_type": "application/json", "temperature": TEMPERATURE},
            request_options={"timeout": 30},
        )
        return json.loads(resp.text)

    if PROVIDER == "mock":
        return _mock(user)

    raise ValueError(f"LLM_PROVIDER không hợp lệ: {PROVIDER}")


def _mock(user: str) -> dict:
    """Câu hỏi giả, hợp lệ về cấu trúc: lấy câu dài đầu tiên của trang làm căn cứ."""
    req = json.loads(user.split("<request>")[1].split("</request>")[0])
    first = user.split("<slide>")[1].split("</slide>")[0].split("[trang ")[1]
    page, text = first.split("]\n", 1)
    quote = next((ln for ln in text.split("\n") if len(ln) >= 25), text[:60])
    return {
        "concept_id": req["concept_id"],
        "level": req["level"],
        "page": int(page),
        "evidence_quote": quote,
        "question": f"[MOCK] Theo slide trang {page}, phát biểu nào đúng về: {req['concept_name']}?",
        "options": ["Phát biểu A (đúng)", "Phát biểu B", "Phát biểu C", "Phát biểu D"],
        "answer": 0,
        "explanation": f"[MOCK] Slide trang {page} ghi: \"{quote}\"",
    }
