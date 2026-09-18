"""API của Solo Arena — nối web (Hiền) với hàm AI (Nam). Hợp đồng: codebase/CONTRACT.md

Chạy (từ thư mục gốc repo):
    uvicorn codebase.api.main:app --reload --port 8000
Mở http://localhost:8000/docs để bấm thử từng endpoint.

Session lưu trong RAM: tắt server là mất. Đủ cho lát cắt (mỗi lượt độc lập, non-goal 4).
"""
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from codebase.ai import generate_question, load_concepts, load_pages

from . import rules

TRACE_DIR = Path(__file__).resolve().parents[2] / "eval" / "traces"
MAX_CONCEPT_TRIES = 3  # AI fail ở khái niệm này thì thử tối đa 3 khái niệm khác trước khi báo lỗi


class StartReq(BaseModel):
    lecture: str = "D01"


class AnswerReq(BaseModel):
    session_id: str
    question_id: str
    choice: int
    answer_ms: int | None = None


class SkipReq(BaseModel):
    session_id: str
    question_id: str


class ReportReq(BaseModel):
    session_id: str
    question_id: str
    reason: Literal["wrong_answer", "unclear", "not_in_slide"]


def create_app(generate: Callable = generate_question, pages: dict | None = None, concepts: dict | None = None,
               trace: bool = True) -> FastAPI:
    """generate có thể thay bằng hàm giả khi test rule (xem test_api.py)."""
    pages = pages if pages is not None else load_pages()
    concepts = concepts or load_concepts()
    names = {c["concept_id"]: c["name"] for c in concepts["concepts"]}
    order = [c["concept_id"] for c in concepts["concepts"]]
    sessions: dict[str, dict] = {}

    app = FastAPI(title="VLearn Solo Arena API")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    # ---------- tiện ích ----------

    def log(kind: str, data: dict):
        if not trace:
            return
        TRACE_DIR.mkdir(parents=True, exist_ok=True)
        rec = {"ts": datetime.now().isoformat(timespec="seconds"), "kind": kind, **data}
        with open(TRACE_DIR / f"api-{datetime.now():%Y%m%d}.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def get_session(sid: str) -> dict:
        if sid not in sessions:
            raise HTTPException(404, "Không tìm thấy lượt luyện")
        return sessions[sid]

    def answered(s: dict) -> list[dict]:
        return [q for q in s["questions"] if q["state"] == "answered"]

    def public(s: dict, q: dict) -> dict:
        """Dạng gửi xuống web. KHÔNG có answer / explanation / evidence_quote (lộ đáp án)."""
        return {
            "question_id": q["question_id"],
            "index": len(answered(s)) + 1,
            "total": rules.TOTAL,
            "concept_name": names[q["concept_id"]],
            "level": q["level"],
            "page": q["page"],
            "question": q["question"],
            "options": q["options"],
        }

    def new_question(s: dict, concept_id: str | None, level: int) -> tuple[dict | None, str]:
        """Gọi AI. Khái niệm fail thì loại khỏi lượt và thử khái niệm khác. Trả (câu, status)."""
        status = "ok"
        for _ in range(MAX_CONCEPT_TRIES):
            if concept_id is None:
                concept_id = rules.pick_concept(order, answered(s), s["excluded"])
            if concept_id is None:
                break
            history = [{"question": q["question"]} for q in s["questions"]]
            start = time.perf_counter()
            r = generate(concept_id, level, pages, history, concepts)
            log("generate", {"session_id": s["id"], "concept_id": concept_id, "level": level,
                             "api_ms": int((time.perf_counter() - start) * 1000), "result": r})
            if r["status"] == "ok":
                q = {k: v for k, v in r.items() if k != "meta"}
                q.update(question_id=f"q{len(s['questions']) + 1}", state="pending")
                s["questions"].append(q)
                s["current"] = q["question_id"]
                return q, status
            s["excluded"].add(concept_id)
            status = "no_evidence"   # báo web: đã đổi sang khái niệm khác vì thiếu căn cứ
            concept_id = None
        s["current"] = None
        return None, "no_evidence"

    def current(s: dict, qid: str) -> dict:
        if s["current"] != qid:
            raise HTTPException(409, "question_id không phải câu đang hỏi")
        return next(q for q in s["questions"] if q["question_id"] == qid)

    # ---------- endpoint ----------

    @app.get("/health")
    def health():
        return {"ok": True, "concepts": len(order), "pages": len(pages)}

    @app.post("/session/start")
    def start(req: StartReq):
        if req.lecture != concepts["lecture"]:
            raise HTTPException(400, f"Chỉ hỗ trợ buổi {concepts['lecture']}")
        s = {"id": uuid.uuid4().hex[:12], "level": rules.START_LEVEL, "questions": [], "excluded": set(), "current": None}
        sessions[s["id"]] = s
        q, status = new_question(s, None, s["level"])
        return {"session_id": s["id"], "question": public(s, q) if q else None, "status": status}

    @app.post("/answer")
    def answer(req: AnswerReq):
        s = get_session(req.session_id)
        q = current(s, req.question_id)
        q.update(state="answered", correct=req.choice == q["answer"], choice=req.choice, answer_ms=req.answer_ms)
        s["level"] = rules.next_level(s["level"], q["correct"])
        resp = {
            "correct": q["correct"],
            "correct_choice": q["answer"],
            "explanation": q["explanation"],
            "page": q["page"],
            "evidence_quote": q["evidence_quote"],
        }
        if len(answered(s)) >= rules.TOTAL:
            s["current"] = None
            return {**resp, "next_question": None, "done": True, "status": "ok"}
        nq, status = new_question(s, None, s["level"])
        return {**resp, "next_question": public(s, nq) if nq else None, "done": False, "status": status}

    @app.post("/skip")
    def skip(req: SkipReq):
        """'Cho tôi câu khác': cùng khái niệm, cùng mức, không tính điểm câu cũ."""
        s = get_session(req.session_id)
        q = current(s, req.question_id)
        q["state"] = "skipped"
        nq, status = new_question(s, q["concept_id"], q["level"])
        return {"question": public(s, nq) if nq else None, "status": status}

    @app.post("/report")
    def report(req: ReportReq):
        """'Báo câu sai': không tính điểm, ghi log để giảng viên xem, sinh câu thay thế."""
        s = get_session(req.session_id)
        q = current(s, req.question_id)
        q["state"] = "reported"
        log("report", {"session_id": s["id"], "reason": req.reason, "question": q})
        nq, _ = new_question(s, q["concept_id"], q["level"])
        return {"question": public(s, nq) if nq else None, "status": "reported"}

    @app.get("/session/{sid}/result")
    def result(sid: str):
        s = get_session(sid)
        done = answered(s)
        items = [{"concept_name": names[a["concept_id"]], "level": a["level"], "correct": a["correct"]} for a in done]
        if rules.is_low_confidence(done):
            return {"items": items, "review_concept": None, "page": None, "evidence_quote": None, "status": "not_enough_data"}
        t = rules.review_target(done)
        return {
            "items": items,
            "review_concept": names[t["concept_id"]] if t else None,   # None = đúng hết, không có chủ đề cần ôn
            "page": t["page"] if t else None,
            "evidence_quote": t["evidence_quote"] if t else None,
            "status": "ok",
        }

    return app

