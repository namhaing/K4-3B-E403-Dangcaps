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
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
MODEL = os.getenv("LLM_MODEL", {"openai": "gpt-4o-mini", "gemini": "gemini-2.0-flash"}.get(PROVIDER, "mock"))
TEMPERATURE = 0.5  # sinh câu: đủ đa dạng cho "Cho tôi câu khác"; hạ từ 0.7 sau case "AI chính" (18/9)


@lru_cache(maxsize=1)
def _openai_client():
    """Dùng chung 1 client: giữ kết nối mở giữa các lần gọi, không bắt tay TLS lại mỗi lần (client an toàn khi dùng nhiều luồng)."""
    from openai import OpenAI

    return OpenAI(api_key=os.getenv("LLM_API_KEY"), timeout=30)


def call_json(system: str, user: str, temperature: float | None = None) -> dict:
    """Gửi prompt, bắt model trả JSON, parse thành dict. Lỗi mạng/parse -> raise để generator xử lý."""
    temp = TEMPERATURE if temperature is None else temperature
    if PROVIDER == "openai":
        resp = _openai_client().chat.completions.create(
            model=MODEL,
            temperature=temp,
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
            generation_config={"response_mime_type": "application/json", "temperature": temp},
            request_options={"timeout": 30},
        )
        return json.loads(resp.text)

    if PROVIDER == "mock":
        if "<verify>" in user:  # kiểm chéo giả: mock luôn đặt đáp án ở lựa chọn 0
            return {"dap_an_dung": [0], "de_ro_nghia": True, "ly_do": "[MOCK]"}
        if "<explain>" in user:  # "Hiểu sâu hơn" giả
            return {"keywords": [{"term": "[MOCK] thuật ngữ", "meaning": "giải thích một câu theo slide"}],
                    "distinction": "[MOCK] khái niệm dễ nhầm và điểm khác nhau", "why_wrong": "[MOCK] vì sao lựa chọn này chưa đúng"}
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
