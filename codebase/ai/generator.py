"""generate_question() — quyết định AI trung tâm của Solo Arena.

Rule (API của D) đã chọn khái niệm + mức. Hàm này chỉ làm 1 việc:
sinh 1 câu trắc nghiệm bám đúng trang slide của khái niệm đó, và KHÔNG trả câu nào chưa qua validator.

Luồng:  kiểm input -> gọi LLM -> validator (code) -> kiểm chéo (AI giải lại, không biết đáp án)
        -> (fail) gọi lại 1 lần kèm lý do -> (fail tiếp) no_evidence
"""
import json
import time
from pathlib import Path

from . import llm
from .prompts import SYSTEM, VERIFY_SYSTEM, build_user, build_verify
from .validator import validate

DATA = Path(__file__).resolve().parents[1] / "data"
MAX_ATTEMPTS = 2  # 1 lần đầu + 1 lần sửa. Nhiều hơn thì chậm, học viên phải chờ


def load_concepts(path: Path = DATA / "concepts.json") -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_pages(path: Path = DATA / "pages.json") -> dict:
    if not path.exists():
        raise FileNotFoundError("Chưa có pages.json — chạy: python codebase/ai/extract_pages.py")
    return json.loads(path.read_text(encoding="utf-8"))


def generate_question(concept_id: str, level: int, pages: dict, history: list, concepts: dict | None = None) -> dict:
    """
    concept_id : khái niệm rule đã chọn (khớp concepts.json)
    level      : 1 | 2 | 3
    pages      : {"3": "text trang 3", ...} từ pages.json
    history    : các câu đã hỏi trong lượt, mỗi phần tử có ít nhất {"question": "..."}
    concepts   : nội dung concepts.json (bỏ trống thì tự đọc file)

    Trả về {"status": "ok", ...8 trường câu hỏi..., "meta": {...}}
        hoặc {"status": "no_evidence", "reason": "...", "meta": {...}}
    "meta" để API ghi trace (eval/traces) — KHÔNG gửi xuống web.
    """
    concepts = concepts or load_concepts()
    meta = {"provider": llm.PROVIDER, "model": llm.MODEL, "attempts": 0, "errors": [], "latency_ms": 0}

    # Kiểm input trước khi tốn tiền gọi AI
    concept = next((c for c in concepts["concepts"] if c["concept_id"] == concept_id), None)
    if concept is None:  # lớp ①: khái niệm không có trong slide buổi này
        return {"status": "no_evidence", "reason": "concept_not_in_lecture", "meta": meta}
    if level not in (1, 2, 3):
        return {"status": "no_evidence", "reason": "invalid_level", "meta": meta}
    if not any(len(pages.get(str(p), "")) >= 50 for p in concept["pages"]):
        return {"status": "no_evidence", "reason": "page_text_missing", "meta": meta}

    level_desc = concepts["level_guide"][str(level)]
    asked = [h["question"] for h in history if h.get("question")]
    # Khái niệm có nhiều trang: gợi ý AI dùng trang chưa hỏi trong lượt (để không hỏi mãi 1 trang)
    used = {int(h["page"]) for h in history if h.get("concept_id") == concept_id and h.get("page")}
    fresh = [p for p in concept["pages"] if p not in used and len(pages.get(str(p), "")) >= 50]
    feedback = ""
    reason = "validation_failed"
    start = time.perf_counter()

    for _ in range(MAX_ATTEMPTS):
        meta["attempts"] += 1
        try:
            q = llm.call_json(SYSTEM, build_user(concept, level, level_desc, pages, asked, feedback, fresh if used else []))
        except Exception as e:  # mạng, timeout, thiếu key, JSON hỏng -> không crash, coi như 1 lần fail
            meta["errors"].append([f"llm_error: {type(e).__name__}: {e}"[:300]])
            reason = "llm_error"
            continue
        reason = "validation_failed"

        errors = validate(q, concept=concept, level=level, pages=pages)
        if not errors:
            errors = cross_check(q, concept, pages, meta)
        if not errors:
            meta["latency_ms"] = int((time.perf_counter() - start) * 1000)
            q = {k: q[k] for k in ("concept_id", "level", "page", "evidence_quote", "question", "options", "answer", "explanation")}
            q["page"] = int(q["page"])
            return {"status": "ok", **q, "meta": meta}

        meta["errors"].append(errors)
        feedback = "; ".join(errors)

    meta["latency_ms"] = int((time.perf_counter() - start) * 1000)
    return {"status": "no_evidence", "reason": reason, "meta": meta}


def cross_check(q: dict, concept: dict, pages: dict, meta: dict) -> list[str]:
    """Kiểm chéo nghĩa: AI giải lại câu hỏi mà KHÔNG biết đáp án.
    Đạt khi đề rõ nghĩa VÀ đúng một lựa chọn đúng, trùng với answer.
    Bắt lỗi validator (code) không bắt được: 2 đáp án đúng (case G02), đáp án vô nghĩa (case "AI chính", 18/9)."""
    try:
        v = llm.call_json(VERIFY_SYSTEM, build_verify(q, concept, pages), temperature=0)
    except Exception as e:  # không kiểm được thì KHÔNG đưa câu cho học viên
        return [f"kiểm chéo lỗi: {type(e).__name__}"]
    meta.setdefault("verify", []).append(v)
    right = sorted({int(i) for i in v.get("dap_an_dung", []) if str(i).lstrip("-").isdigit()})
    errors = []
    if not v.get("de_ro_nghia", False):
        errors.append(f"kiểm chéo: đề không rõ nghĩa ({v.get('ly_do', '')})")
    if right != [q["answer"]]:
        errors.append(f"kiểm chéo: theo slide các lựa chọn đúng là {right}, không khớp đáp án {q['answer']} ({v.get('ly_do', '')})")
    return errors
