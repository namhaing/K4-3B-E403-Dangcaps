""""Hiểu sâu hơn" — BẢN THỬ cho demo (thêm 19/9), NGOÀI bộ đo và quality bar.

Sau khi học viên đã trả lời, AI tổng hợp từ khoá + điểm cần phân biệt của CHÍNH câu đó, chỉ dựa trên slide.
Khác phần sinh câu hỏi: chưa có validator / kiểm chéo / eval → web ghi rõ "bản thử".
"""
from . import llm
from .prompts import EXPLAIN_SYSTEM, build_explain

MAX_KEYWORDS = 4


def explain_question(q: dict, choice: int, concept: dict, pages: dict) -> dict:
    """Trả {"status": "ok", "keywords": [{term, meaning}], "distinction", "why_wrong"} hoặc {"status": "error"}.
    Lỗi AI không làm hỏng màn phản hồi: web chỉ báo chưa tổng hợp được."""
    try:
        r = llm.call_json(EXPLAIN_SYSTEM, build_explain(q, choice, concept, pages), temperature=0.2)
    except Exception as e:
        return {"status": "error", "reason": type(e).__name__}
    keywords = [{"term": str(k["term"]).strip(), "meaning": str(k["meaning"]).strip()}
                for k in r.get("keywords") or [] if isinstance(k, dict) and str(k.get("term", "")).strip() and str(k.get("meaning", "")).strip()]
    chose_wrong = 0 <= choice <= 3 and choice != q["answer"]
    return {
        "status": "ok",
        "keywords": keywords[:MAX_KEYWORDS],
        "distinction": str(r.get("distinction") or "").strip(),
        "why_wrong": str(r["why_wrong"]).strip() if chose_wrong and r.get("why_wrong") else None,
    }
