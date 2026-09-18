"""Test rule + API bằng hàm AI GIẢ (không tốn tiền, kết quả lặp lại được).

    python -m codebase.api.test_api          (chạy từ thư mục gốc repo)

Test này kiểm LUỒNG và RULE. Chất lượng câu hỏi AI thật được đo ở eval/run_eval.py.
"""
import sys
import warnings

from fastapi.testclient import TestClient

from . import rules
from .app import create_app

sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore", message=".*httpx.*starlette.testclient.*")  # cảnh báo thư viện, không ảnh hưởng kết quả

CONCEPTS = {
    "lecture": "D01",
    "level_guide": {"1": "", "2": "", "3": ""},
    "concepts": [{"concept_id": c, "name": c.upper(), "pages": [i + 1]} for i, c in enumerate(["a", "b", "c", "d", "e", "f"])],
}
PAGES = {str(i): "x" * 60 for i in range(1, 7)}
FAIL = set()  # khái niệm mà hàm giả trả no_evidence


def fake_generate(concept_id, level, pages, history, concepts):
    if concept_id in FAIL:
        return {"status": "no_evidence", "reason": "validation_failed", "meta": {}}
    n = len(history) + 1
    return {"status": "ok", "concept_id": concept_id, "level": level, "page": 1, "evidence_quote": "trích",
            "question": f"câu {n} về {concept_id} mức {level}", "options": ["đúng", "sai1", "sai2", "sai3"],
            "answer": 0, "explanation": "vì slide nói vậy", "meta": {}}


def client():
    FAIL.clear()
    return TestClient(create_app(generate=fake_generate, pages=PAGES, concepts=CONCEPTS, trace=False))


def play(c, choices, ms=5000):
    """Chơi hết các lựa chọn trong choices (0 = đúng). Trả (session_id, danh sách response)."""
    r = c.post("/session/start", json={"lecture": "D01"}).json()
    sid, q, out = r["session_id"], r["question"], [r]
    for ch in choices:
        r = c.post("/answer", json={"session_id": sid, "question_id": q["question_id"], "choice": ch, "answer_ms": ms}).json()
        out.append(r)
        q = r["next_question"]
    return sid, out


RESULTS = []


def check(name, cond, detail=""):
    cond = bool(cond)
    RESULTS.append(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  -> {detail}" if not cond else ""))


# ---------- rule thuần ----------
check("mức: đúng → +1", rules.next_level(2, True) == 3)
check("mức: sai → −1", rules.next_level(2, False) == 1)
check("mức: không vượt 3 / dưới 1", rules.next_level(3, True) == 3 and rules.next_level(1, False) == 1)
A = [{"concept_id": "a", "correct": False}]
check("khái niệm: vừa sai → giữ khái niệm", rules.pick_concept(["a", "b"], A, set()) == "a")
check("khái niệm: vừa đúng → khái niệm chưa hỏi", rules.pick_concept(["a", "b"], [{"concept_id": "a", "correct": True}], set()) == "b")
check("khái niệm: bỏ khái niệm đã bị loại", rules.pick_concept(["a", "b"], [], {"a"}) == "b")
check("② dưới 3 câu → chưa đủ dữ liệu", rules.is_low_confidence([{"answer_ms": 9000}] * 2))
check("② 3 câu trả lời < 3 giây → chưa đủ dữ liệu", rules.is_low_confidence([{"answer_ms": 900}] * 3 + [{"answer_ms": 9000}] * 2))
check("② 5 câu bình thường → đủ dữ liệu", not rules.is_low_confidence([{"answer_ms": 9000}] * 5))

# ---------- API ----------
c = client()
sid, out = play(c, [0, 1, 1, 0, 0])
check("happy: 5 câu xong thì done", out[-1]["done"] and out[-1]["next_question"] is None)
check("không gửi đáp án xuống web", all(k not in out[0]["question"] for k in ("answer", "explanation", "evidence_quote")))
levels = [o["next_question"]["level"] for o in out[1:-1]]
check("mức đổi theo đúng/sai: 2→3→2→1→2", levels == [3, 2, 1, 2], levels)
concepts_seen = [o["next_question"]["concept_name"] for o in out[1:-1]]
check("sai thì câu sau giữ khái niệm", concepts_seen[1] == concepts_seen[0] and concepts_seen[2] == concepts_seen[1], concepts_seen)
res = c.get(f"/session/{sid}/result").json()
check("kết quả: đủ 5 câu, có chủ đề cần ôn kèm trang", res["status"] == "ok" and len(res["items"]) == 5 and res["review_concept"] and res["page"], res)

sid, _ = play(c, [0, 0, 0, 0, 0])
res = c.get(f"/session/{sid}/result").json()
check("đúng hết → không bịa chủ đề cần ôn", res["status"] == "ok" and res["review_concept"] is None, res)

sid, _ = play(c, [1, 1])
check("② thoát sau 2 câu → not_enough_data", c.get(f"/session/{sid}/result").json()["status"] == "not_enough_data")
sid, _ = play(c, [0, 1, 0, 1, 0], ms=800)
check("② trả lời toàn < 3 giây → not_enough_data", c.get(f"/session/{sid}/result").json()["status"] == "not_enough_data")

r = c.post("/session/start", json={"lecture": "D01"}).json()
sid, q = r["session_id"], r["question"]
k = c.post("/skip", json={"session_id": sid, "question_id": q["question_id"]}).json()
check("skip: cùng khái niệm, cùng mức, câu mới", k["question"]["concept_name"] == q["concept_name"]
      and k["question"]["level"] == q["level"] and k["question"]["question"] != q["question"], k)
rp = c.post("/report", json={"session_id": sid, "question_id": k["question"]["question_id"], "reason": "wrong_answer"}).json()
check("report: status reported + có câu thay thế", rp["status"] == "reported" and rp["question"], rp)
check("câu bị skip/report không tính vào số câu", rp["question"]["index"] == 1, rp["question"])
old = c.post("/answer", json={"session_id": sid, "question_id": q["question_id"], "choice": 0})
check("trả lời câu cũ đã bị thay → 409", old.status_code == 409, old.status_code)

check("③ xem lượt của người khác (id lạ) → 404", c.get("/session/khong-ton-tai/result").status_code == 404)
check("buổi không hỗ trợ → 400", c.post("/session/start", json={"lecture": "D09"}).status_code == 400)

FAIL.update({"a"})
r = c.post("/session/start", json={"lecture": "D01"}).json()
check("① khái niệm đầu không có căn cứ → đổi khái niệm, báo no_evidence",
      r["status"] == "no_evidence" and r["question"] and r["question"]["concept_name"] == "B", r)
FAIL.update({"b", "c", "d", "e", "f"})
r = c.post("/session/start", json={"lecture": "D01"}).json()
check("① không khái niệm nào có căn cứ → không bịa câu", r["status"] == "no_evidence" and r["question"] is None, r)

print(f"\n{sum(RESULTS)}/{len(RESULTS)} test đạt")
sys.exit(0 if all(RESULTS) else 1)
