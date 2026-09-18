"""API của Solo Arena — nối web (Hiền) với hàm AI (Nam). Hợp đồng: codebase/CONTRACT.md

Chạy (từ thư mục gốc repo):
    uvicorn codebase.api.main:app --reload --port 8000
Mở http://localhost:8000/docs để bấm thử từng endpoint.

Session lưu trong RAM: tắt server là mất. Đủ cho lát cắt (mỗi lượt độc lập, non-goal 4).
"""
import json
import os
import random
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Callable, Literal

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from codebase.ai import generate_question, load_concepts, load_pages

from . import rules
from .progress import ProgressStore, valid_learner

TRACE_DIR = Path(__file__).resolve().parents[2] / "eval" / "traces"
WEB_DIR = Path(__file__).resolve().parents[1] / "web"
PROGRESS_FILE = Path(__file__).resolve().parents[1] / "data" / "progress.json"  # không commit
# PDF slide gốc (data pack, KHÔNG có trong repo). Máy không có file thì /slide trả 404 và web hiện chữ thay ảnh.
SLIDE_PDF = Path(os.getenv("SLIDE_PDF", Path(__file__).resolve().parents[2] / "data" / "vlearn-pack" / "slides" / "d1-slide-hackathon.pdf"))
MAX_CONCEPT_TRIES = 3  # AI fail ở khái niệm này thì thử tối đa 3 khái niệm khác trước khi báo lỗi


class _NoShuffle:
    """Dùng khi test (shuffle=False): giữ nguyên thứ tự trong mỗi nhóm."""
    def shuffle(self, x):
        pass


class StartReq(BaseModel):
    lecture: str = "D01"
    learner_id: str | None = None   # mã ngẫu nhiên của trình duyệt; bỏ trống = lượt độc lập như cũ
    focus_concept: str | None = None  # "Luyện 3 câu phần này": lượt ngắn chỉ hỏi 1 khái niệm


class AnswerReq(BaseModel):
    session_id: str
    question_id: str
    choice: int
    answer_ms: int | None = None
    timed_out: bool = False   # chế độ đấu: hết giờ mà chưa chọn (choice = -1) → 0 điểm, KHÔNG tính vào bản đồ chỗ yếu


class SkipReq(BaseModel):
    session_id: str
    question_id: str


class ReportReq(BaseModel):
    session_id: str
    question_id: str
    reason: Literal["wrong_answer", "unclear", "not_in_slide"]


def create_app(generate: Callable = generate_question, pages: dict | None = None, concepts: dict | None = None,
               trace: bool = True, shuffle: bool = True, progress_path: Path | None = PROGRESS_FILE,
               slide_pdf: Path | None = SLIDE_PDF, prefetch: bool = False) -> FastAPI:
    """generate có thể thay bằng hàm giả khi test rule (xem test_api.py). shuffle=False để test có thứ tự cố định.
    prefetch=True (main.py bật): trong lúc học viên đọc câu hiện tại, sinh sẵn câu tiếp theo cho CẢ 2 nhánh đúng/sai
    → /answer trả gần như ngay. Sinh 1 câu mất ~7 s (gồm kiểm chéo + sinh lại), học viên nghĩ thường lâu hơn thế."""
    pages = pages if pages is not None else load_pages()
    concepts = concepts or load_concepts()
    names = {c["concept_id"]: c["name"] for c in concepts["concepts"]}
    order = [c["concept_id"] for c in concepts["concepts"]]
    sessions: dict[str, dict] = {}
    progress = ProgressStore(progress_path)   # progress_path=None → chỉ trong RAM (test)
    slide_cache: dict[int, bytes] = {}         # ảnh slide đã vẽ, chỉ giữ trong RAM (không ghi ra repo)
    pool = ThreadPoolExecutor(max_workers=8, thread_name_prefix="prefetch") if prefetch else None
    # Câu đầu của lượt (mức START_LEVEL, chưa có lịch sử) sinh sẵn cho mọi khái niệm ngay khi bật server;
    # dùng 1 câu thì sinh bù câu mới → lượt nào cũng mở ra ngay, và không học viên nào nhận lại câu người khác đã làm.
    warm = {c: pool.submit(generate, c, rules.START_LEVEL, pages, [], concepts) for c in order} if pool else {}

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
            "total": s["total"],
            "concept_name": names[q["concept_id"]],
            "level": q["level"],
            "page": q["page"],
            "question": q["question"],
            "options": q["options"],
            "skips_left": rules.MAX_SKIPS - s["skips"],   # web hiện "Đổi câu khác (còn n)", hết thì ẩn nút
        }

    def history_of(s: dict) -> list[dict]:
        return [{"question": q["question"], "concept_id": q["concept_id"], "page": q["page"]} for q in s["questions"]]

    def start_prefetch(s: dict, q: dict):
        """Sinh sẵn câu tiếp theo cho cả 2 nhánh, theo ĐÚNG luật /answer sẽ dùng (pick_concept + next_level).
        Nhánh không xảy ra thì bỏ (tốn thêm 1 lần gọi AI mỗi câu — đổi tiền lấy thời gian chờ của học viên)."""
        s["prefetch"] = {}
        if pool is None or len(answered(s)) + 1 >= s["total"]:   # câu cuối của lượt: không có câu tiếp
            return
        history = history_of(s)
        for correct in (True, False):
            concept_id = rules.pick_concept(s["order"], answered(s) + [{**q, "correct": correct}], s["excluded"])
            level = rules.next_level(s["level"], correct)
            if concept_id is not None:
                s["prefetch"][correct] = (concept_id, level, pool.submit(generate, concept_id, level, pages, history, concepts))

    def take_prefetched(ready, concept_id: str, level: int) -> dict | None:
        """Kết quả sinh sẵn nếu đúng khái niệm + mức cần hỏi. Lỗi hoặc lệch kế hoạch → None, gọi AI như bình thường."""
        if not ready or ready[:2] != (concept_id, level):
            return None
        try:
            return ready[2].result(timeout=60)
        except Exception:
            return None

    def take_warm(s: dict):
        """Câu đầu đã sinh sẵn cho khái niệm mà luật sẽ chọn; lấy ra thì sinh bù ngay."""
        concept_id = rules.pick_concept(s["order"], [], s["excluded"])
        fut = warm.pop(concept_id, None)   # pop một lần: 2 lượt mở cùng lúc không lấy trùng 1 câu
        if fut is None:
            return None
        warm[concept_id] = pool.submit(generate, concept_id, rules.START_LEVEL, pages, [], concepts)
        return concept_id, rules.START_LEVEL, fut

    def new_question(s: dict, concept_id: str | None, level: int, ready=None) -> tuple[dict | None, str]:
        """Gọi AI (hoặc dùng câu đã sinh sẵn `ready`). Khái niệm fail thì loại khỏi lượt và thử khái niệm khác. Trả (câu, status)."""
        status = "ok"
        for _ in range(MAX_CONCEPT_TRIES):
            if concept_id is None:
                concept_id = rules.pick_concept(s["order"], answered(s), s["excluded"])
            if concept_id is None:
                break
            start = time.perf_counter()
            r = take_prefetched(ready, concept_id, level)
            prefetched, ready = r is not None, None
            if r is None:
                r = generate(concept_id, level, pages, history_of(s), concepts)
            # api_ms = thời gian học viên thật sự phải chờ (câu sinh sẵn thì gần 0)
            log("generate", {"session_id": s["id"], "concept_id": concept_id, "level": level, "prefetched": prefetched,
                             "api_ms": int((time.perf_counter() - start) * 1000), "result": r})
            if r["status"] == "ok":
                q = {k: v for k, v in r.items() if k != "meta"}
                q.update(question_id=f"q{len(s['questions']) + 1}", state="pending")
                s["questions"].append(q)
                s["current"] = q["question_id"]
                start_prefetch(s, q)
                return q, status
            if s.get("focus"):   # ôn riêng 1 khái niệm: không có khái niệm khác để chuyển → thử lại chính nó (tối đa MAX_CONCEPT_TRIES)
                continue
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
        if req.learner_id is not None and not valid_learner(req.learner_id):
            raise HTTPException(400, "learner_id không hợp lệ")
        learner = req.learner_id
        # Có hồ sơ: ưu tiên khái niệm đang yếu → chưa luyện → đã vững (đo chỗ yếu qua nhiều lượt, 18/9).
        # Không có: xáo ngẫu nhiên (trước đây mọi lượt bắt đầu ở trang 3, 29 trang chỉ dùng tới 7).
        if learner and progress.get(learner):
            s_order = rules.order_for_learner(order, progress.get(learner), random.Random() if shuffle else _NoShuffle())
        else:
            s_order = random.sample(order, len(order)) if shuffle else list(order)
        weak = [c for c in order if rules.concept_status(progress.get(learner or "").get(c)) == "dang_yeu"]
        total = rules.TOTAL
        if req.focus_concept is not None:   # ôn riêng 1 khái niệm: 3 câu, mức vẫn đổi theo đúng/sai
            if req.focus_concept not in names:
                raise HTTPException(404, "Không có khái niệm này trong buổi học")
            s_order, weak, total = [req.focus_concept], [], rules.FOCUS_TOTAL
        s = {"id": uuid.uuid4().hex[:12], "level": rules.START_LEVEL, "questions": [], "excluded": set(), "current": None,
             "order": s_order, "learner": learner, "total": total, "focus": req.focus_concept is not None, "skips": 0}
        sessions[s["id"]] = s
        q, status = new_question(s, None, s["level"], take_warm(s))
        return {"session_id": s["id"], "question": public(s, q) if q else None, "status": status,
                "focus_weak": [names[c] for c in weak]}   # web báo "lượt này ưu tiên ôn: …"

    @app.post("/answer")
    def answer(req: AnswerReq):
        s = get_session(req.session_id)
        q = current(s, req.question_id)
        q.update(state="answered", correct=req.choice == q["answer"], choice=req.choice, answer_ms=req.answer_ms)
        s["level"] = rules.next_level(s["level"], q["correct"])
        # Cộng dồn vào hồ sơ. Câu trả lời quá nhanh (< FAST_MS, dấu hiệu đoán mò) KHÔNG tính vào chỗ yếu (G10).
        # Hết giờ cũng không tính: không chọn kịp chưa chứng minh là hiểu sai.
        if s.get("learner") and not req.timed_out and (req.answer_ms is None or req.answer_ms >= rules.FAST_MS):
            progress.record(s["learner"], q["concept_id"], q["correct"], q["level"], detail={
                "question": q["question"], "options": q["options"], "choice": req.choice, "correct_choice": q["answer"],
                "explanation": q["explanation"], "evidence_quote": q["evidence_quote"], "page": q["page"], "level": q["level"]})
        resp = {
            "correct": q["correct"],
            "correct_choice": q["answer"],
            "explanation": q["explanation"],
            "page": q["page"],
            "evidence_quote": q["evidence_quote"],
        }
        if len(answered(s)) >= s["total"]:
            s["current"] = None
            return {**resp, "next_question": None, "done": True, "status": "ok"}
        nq, status = new_question(s, None, s["level"], s.get("prefetch", {}).get(q["correct"]))
        return {**resp, "next_question": public(s, nq) if nq else None, "done": False, "status": status}

    @app.post("/skip")
    def skip(req: SkipReq):
        """'Cho tôi câu khác': cùng khái niệm, cùng mức, không tính điểm câu cũ. Tối đa MAX_SKIPS lần mỗi lượt."""
        s = get_session(req.session_id)
        q = current(s, req.question_id)
        if s["skips"] >= rules.MAX_SKIPS:
            raise HTTPException(409, f"Đã dùng hết {rules.MAX_SKIPS} lần đổi câu trong lượt này")
        s["skips"] += 1
        q["state"] = "skipped"
        # Câu bị đổi nhiều = câu khó hiểu hoặc khái niệm học viên né → dữ liệu cho eval, KHÔNG đưa vào bản đồ
        log("skip", {"session_id": s["id"], "concept_id": q["concept_id"], "level": q["level"], "question": q["question"]})
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

    @app.get("/learner/{learner_id}/progress")
    def learner_progress(learner_id: str):
        """Bản đồ kiến thức của 1 học viên (chỉ ai giữ mã mới xem được). Không có endpoint liệt kê học viên."""
        if not valid_learner(learner_id):
            raise HTTPException(400, "learner_id không hợp lệ")
        data = progress.get(learner_id)
        items = []
        for c in concepts["concepts"]:
            st = data.get(c["concept_id"], {})
            status = rules.concept_status(st)
            items.append({"concept_id": c["concept_id"], "concept_name": c["name"], "pages": c["pages"],
                          "status": status, "status_label": rules.STATUS_LABEL[status],
                          "attempts": st.get("attempts", 0), "correct": st.get("correct", 0),
                          "recent": st.get("recent", []), "status_reason": rules.status_reason(st)})
        summary = {k: sum(1 for i in items if i["status"] == k) for k in rules.STATUS_LABEL}
        return {"lecture": concepts["lecture"], "min_answers": rules.MIN_CONCEPT_ANSWERS,
                "summary": summary, "concepts": items,
                "weak": [i for i in items if i["status"] == "dang_yeu"]}

    @app.get("/learner/{learner_id}/concept/{concept_id}/review")
    def concept_review(learner_id: str, concept_id: str):
        """Màn "Ôn lại kiến thức": câu học viên đã sai (kèm đáp án đúng, giải thích, câu trích đã kiểm chéo)
        + nội dung slide gốc của khái niệm. KHÔNG gọi AI — chỉ dùng lại nội dung đã được kiểm tra."""
        if not valid_learner(learner_id):
            raise HTTPException(400, "learner_id không hợp lệ")
        c = next((x for x in concepts["concepts"] if x["concept_id"] == concept_id), None)
        if c is None:
            raise HTTPException(404, "Không có khái niệm này trong buổi học")
        st = progress.get(learner_id).get(concept_id, {})
        status = rules.concept_status(st)
        return {"concept_id": concept_id, "concept_name": c["name"], "status": status,
                "status_label": rules.STATUS_LABEL[status], "status_reason": rules.status_reason(st),
                "attempts": st.get("attempts", 0), "correct": st.get("correct", 0), "recent": st.get("recent", []),
                "mistakes": list(reversed(st.get("mistakes", []))), "quotes": st.get("quotes", []),
                "slides": [{"page": p, "text": pages.get(str(p), "")} for p in c["pages"]]}

    @app.get("/slide/{page}.png")
    def slide_image(page: int):
        """Ảnh đúng trang slide để học viên ôn lại (vẽ từ PDF gốc trên máy chạy server, lưu tạm trong RAM)."""
        if not slide_pdf or not Path(slide_pdf).exists():
            raise HTTPException(404, "Máy chủ không có file slide gốc")
        if page not in slide_cache:
            import pymupdf
            with pymupdf.open(slide_pdf) as doc:
                if not 1 <= page <= len(doc):
                    raise HTTPException(404, "Không có trang này")
                slide_cache[page] = doc[page - 1].get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6)).tobytes("png")
        return Response(slide_cache[page], media_type="image/png", headers={"Cache-Control": "max-age=3600"})

    # Web của Hiền: mở http://localhost:8000/app/ (cùng máy chủ nên không lo CORS)
    if WEB_DIR.exists():
        app.mount("/app", StaticFiles(directory=WEB_DIR, html=True), name="web")

    return app

