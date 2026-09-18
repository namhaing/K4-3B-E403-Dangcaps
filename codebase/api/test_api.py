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
    return TestClient(create_app(generate=fake_generate, pages=PAGES, concepts=CONCEPTS, trace=False, shuffle=False, progress_path=None))


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
AA = [{"concept_id": "a", "correct": False}, {"concept_id": "a", "correct": False}]
check("khái niệm: sai 2 lần liên tiếp → chuyển khái niệm (hết kẹt)", rules.pick_concept(["a", "b"], AA, set()) == "b")
check("hỏi hết rồi thì không quay lại ngay khái niệm vừa sai 2 lần",
      rules.pick_concept(["a", "b"], [{"concept_id": "b", "correct": False}] + AA, set()) == "b")
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
check("sai 1 lần giữ khái niệm, sai lần 2 thì chuyển", concepts_seen[1] == concepts_seen[0] and concepts_seen[2] != concepts_seen[1], concepts_seen)
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
check("báo câu sai không trừ lượt đổi câu (là đường sửa lỗi, HAX G9)", rp["question"]["skips_left"] == rules.MAX_SKIPS - 1, rp["question"])

# Giới hạn "Đổi câu khác": đổi không giới hạn thì lượt không bao giờ xong, và học viên né câu khó
r = c.post("/session/start", json={"lecture": "D01"}).json()
sid, q = r["session_id"], r["question"]
lefts = [q["skips_left"]]
for _ in range(rules.MAX_SKIPS):
    q = c.post("/skip", json={"session_id": sid, "question_id": q["question_id"]}).json()["question"]
    lefts.append(q["skips_left"])
check(f"đổi câu: còn {rules.MAX_SKIPS} → 0 lần", lefts == list(range(rules.MAX_SKIPS, -1, -1)), lefts)
over = c.post("/skip", json={"session_id": sid, "question_id": q["question_id"]})
check("đổi câu quá giới hạn → 409", over.status_code == 409, over.status_code)
done = None
for _ in range(rules.TOTAL):
    a = c.post("/answer", json={"session_id": sid, "question_id": q["question_id"], "choice": 0, "answer_ms": 5000})
    done, q = a.json()["done"], a.json()["next_question"]
check("hết lượt đổi: câu hiện tại vẫn trả lời được và lượt xong đủ 5 câu", a.status_code == 200 and done, a.json())

cs = TestClient(create_app(generate=fake_generate, pages=PAGES, concepts=CONCEPTS, trace=False, shuffle=True, progress_path=None))
firsts = {cs.post("/session/start", json={"lecture": "D01"}).json()["question"]["concept_name"] for _ in range(30)}
check("xáo thứ tự: 30 lượt không cùng bắt đầu ở 1 khái niệm", len(firsts) >= 3, firsts)
sid, out = play(c, [1, 1, 1, 1, 1])
seen = [out[0]["question"]["concept_name"]] + [o["next_question"]["concept_name"] for o in out[1:-1]]
check("sai cả 5 câu → không kẹt 1 khái niệm", len(set(seen)) >= 2, seen)
check("③ xem lượt của người khác (id lạ) → 404", c.get("/session/khong-ton-tai/result").status_code == 404)
check("buổi không hỗ trợ → 400", c.post("/session/start", json={"lecture": "D09"}).status_code == 400)

FAIL.update({"a"})
r = c.post("/session/start", json={"lecture": "D01"}).json()
check("① khái niệm đầu không có căn cứ → đổi khái niệm, báo no_evidence",
      r["status"] == "no_evidence" and r["question"] and r["question"]["concept_name"] == "B", r)
FAIL.update({"b", "c", "d", "e", "f"})
r = c.post("/session/start", json={"lecture": "D01"}).json()
check("① không khái niệm nào có căn cứ → không bịa câu", r["status"] == "no_evidence" and r["question"] is None, r)

# ---------- Đo chỗ yếu qua nhiều lượt ----------
check("trạng thái: chưa làm → chưa luyện", rules.concept_status(None) == "chua_luyen")
check("trạng thái: 2 câu sai → CHƯA đủ dữ liệu (G10, không kết luận vội)", rules.concept_status({"attempts": 2, "recent": [False, False]}) == "chua_du_du_lieu")
check("trạng thái: sai ≥ 2/3 câu gần nhất → đang yếu", rules.concept_status({"attempts": 3, "recent": [False, True, False]}) == "dang_yeu")
check("trạng thái: đúng ≥ 2/3 câu gần nhất → đã vững", rules.concept_status({"attempts": 4, "recent": [False, True, False, True, True][-3:]}) == "da_vung")

FAIL.clear()
cp = TestClient(create_app(generate=fake_generate, pages=PAGES, concepts=CONCEPTS, trace=False, shuffle=False, progress_path=None))
L = "hocvien-test-0001"


def play_as(learner, choices, ms=5000):
    r = cp.post("/session/start", json={"lecture": "D01", "learner_id": learner}).json()
    q, first = r["question"], r
    for ch in choices:
        q = cp.post("/answer", json={"session_id": r["session_id"], "question_id": q["question_id"], "choice": ch, "answer_ms": ms}).json()["next_question"]
    return first


check("learner_id lạ (ký tự đặc biệt) → 400", cp.post("/session/start", json={"lecture": "D01", "learner_id": "../../etc"}).status_code == 400)
p0 = cp.get(f"/learner/{L}/progress").json()
check("học viên mới: 6/6 khái niệm 'chưa luyện', không có chỗ yếu", p0["summary"]["chua_luyen"] == 6 and p0["weak"] == [], p0["summary"])
play_as(L, [1, 1, 0, 0, 0])            # lượt 1: sai A 2 lần → chuyển B, C, D đúng
p1 = cp.get(f"/learner/{L}/progress").json()
st = {i["concept_id"]: i for i in p1["concepts"]}
check("lượt 1: A sai 2 câu → vẫn 'chưa đủ dữ liệu', chưa kết luận yếu", st["a"]["status"] == "chua_du_du_lieu" and st["a"]["attempts"] == 2, st["a"])
play_as(L, [1, 0, 0, 0, 0])            # lượt 2: bắt đầu lại ở A (chưa vững), sai thêm 1 → A: 3 câu, sai 3
p2 = cp.get(f"/learner/{L}/progress").json()
check("lượt 2: A đủ 3 câu, sai 3 → 'đang yếu'", [w["concept_id"] for w in p2["weak"]] == ["a"], p2["weak"])
r3 = play_as(L, [])
check("lượt 3: báo 'ưu tiên ôn' đúng khái niệm yếu", r3["focus_weak"] == ["A"], r3.get("focus_weak"))
check("lượt 3: câu đầu tiên hỏi NGAY khái niệm đang yếu", r3["question"]["concept_name"] == "A", r3["question"]["concept_name"])
before = cp.get(f"/learner/{L}/progress").json()["concepts"][0]["attempts"]
play_as(L, [0, 0, 0, 0, 0], ms=800)    # đoán mò: trả lời < 3 giây
after = cp.get(f"/learner/{L}/progress").json()["concepts"][0]["attempts"]
check("câu trả lời < 3 giây (đoán mò) KHÔNG tính vào hồ sơ", before == after, (before, after))
L2 = "hocvien-test-0002"
r = cp.post("/session/start", json={"lecture": "D01", "learner_id": L2}).json()
to = cp.post("/answer", json={"session_id": r["session_id"], "question_id": r["question"]["question_id"], "choice": -1,
                              "answer_ms": 30000, "timed_out": True}).json()
check("chế độ đấu hết giờ: tính sai, vẫn trả đáp án đúng + giải thích, lượt đi tiếp",
      to["correct"] is False and to["correct_choice"] == 0 and to["explanation"] and to["next_question"], to)
check("chế độ đấu hết giờ: KHÔNG tính vào bản đồ chỗ yếu",
      all(i["attempts"] == 0 for i in cp.get(f"/learner/{L2}/progress").json()["concepts"]))
check("không có learner_id → lượt độc lập như cũ, không ghi hồ sơ", play_as(None, [0])["focus_weak"] == [])

# ---------- Ôn lại kiến thức + luyện riêng 1 phần ----------
rv = cp.get(f"/learner/{L}/concept/a/review").json()
check("ôn lại: có danh sách câu đã sai, mỗi câu kèm đáp án đúng + giải thích + câu trích",
      len(rv["mistakes"]) >= 3 and all(k in rv["mistakes"][0] for k in ("question", "choice", "correct_choice", "explanation", "evidence_quote", "page")), rv["mistakes"][:1])
check("ôn lại: có nội dung slide gốc của khái niệm", rv["slides"] and rv["slides"][0]["page"] == 1 and rv["slides"][0]["text"], rv["slides"])
check("ôn lại: có lý do trạng thái bằng lời", rv["status"] == "dang_yeu" and rv["status_reason"].startswith("Sai"), rv["status_reason"])
check("ôn lại: khái niệm không có trong buổi → 404", cp.get(f"/learner/{L}/concept/khong-co/review").status_code == 404)
check("lý do trạng thái: 1 câu → 'cần thêm 2 câu'", "cần thêm 2 câu" in rules.status_reason({"attempts": 1, "recent": [False]}))

rf = cp.post("/session/start", json={"lecture": "D01", "learner_id": L, "focus_concept": "c"}).json()
qs, q = [rf["question"]], rf["question"]
while q:
    nxt = cp.post("/answer", json={"session_id": rf["session_id"], "question_id": q["question_id"], "choice": 1, "answer_ms": 5000}).json()
    q = nxt["next_question"]; qs += [q] if q else []
check("luyện riêng 1 phần: đúng 3 câu, cả 3 cùng khái niệm đã chọn", len(qs) == 3 and {x["concept_name"] for x in qs} == {"C"} and qs[0]["total"] == 3,
      [(x["concept_name"], x["total"]) for x in qs])
calls = {"n": 0}


def flaky(concept_id, level, pages, history, concepts):   # lần đầu AI không ra câu có căn cứ, lần sau ra
    calls["n"] += 1
    return {"status": "no_evidence", "reason": "validation_failed", "meta": {}} if calls["n"] == 1 else fake_generate(concept_id, level, pages, history, concepts)


cf = TestClient(create_app(generate=flaky, pages=PAGES, concepts=CONCEPTS, trace=False, shuffle=False, progress_path=None))
rr = cf.post("/session/start", json={"lecture": "D01", "focus_concept": "c"}).json()
check("luyện riêng: AI hụt 1 lần → thử lại CHÍNH khái niệm đó, không bỏ cuộc", rr["question"] and rr["question"]["concept_name"] == "C", rr)
check("luyện riêng: khái niệm lạ → 404", cp.post("/session/start", json={"lecture": "D01", "focus_concept": "zzz"}).status_code == 404)

# ---------- Ảnh slide cho màn ôn lại ----------
import tempfile
from pathlib import Path

import pymupdf

tmp_pdf = Path(tempfile.mkdtemp()) / "slide-thu.pdf"
doc = pymupdf.open(); doc.new_page().insert_text((72, 72), "Trang 1"); doc.new_page(); doc.save(tmp_pdf); doc.close()
ci = TestClient(create_app(generate=fake_generate, pages=PAGES, concepts=CONCEPTS, trace=False, progress_path=None, slide_pdf=tmp_pdf))
img = ci.get("/slide/1.png")
check("ảnh slide: trang có thật → ảnh PNG", img.status_code == 200 and img.headers["content-type"] == "image/png" and img.content[:4] == b"\x89PNG", img.status_code)
check("ảnh slide: trang không tồn tại → 404", ci.get("/slide/99.png").status_code == 404)
cn = TestClient(create_app(generate=fake_generate, pages=PAGES, concepts=CONCEPTS, trace=False, progress_path=None, slide_pdf=Path("khong-co.pdf")))
check("ảnh slide: máy không có PDF gốc → 404 (web tự hiện chữ thay ảnh)", cn.get("/slide/1.png").status_code == 404)

# ---------- Sinh sẵn câu tiếp theo trong lúc học viên đọc câu (giảm chờ sau khi trả lời) ----------
import threading
import time

slow_calls = []


def slow_generate(concept_id, level, pages, history, concepts):   # AI thật mất vài giây; giả lập 0.3 s
    slow_calls.append(threading.current_thread().name.startswith("prefetch"))
    time.sleep(0.3)
    return fake_generate(concept_id, level, pages, history, concepts)


def play_prefetch(actions, fail=()):
    """actions: số = chọn đáp án, "skip" = cho tôi câu khác. Trả (các câu đã hiện, thời gian chờ mỗi /answer)."""
    c = TestClient(create_app(generate=slow_generate, pages=PAGES, concepts=CONCEPTS, trace=False, shuffle=False,
                              progress_path=None, prefetch=True))
    FAIL.clear(); FAIL.update(fail)
    time.sleep(0.5)   # vừa bật server: câu đầu của mọi khái niệm đang được sinh sẵn
    t = time.perf_counter()
    r = c.post("/session/start", json={"lecture": "D01"}).json()
    sid, q, shown, waits = r["session_id"], r["question"], [r["question"]["question"]], [time.perf_counter() - t]
    for a in actions:
        time.sleep(0.5)   # học viên đọc câu → server sinh sẵn xong
        t = time.perf_counter()
        if a == "skip":
            q = c.post("/skip", json={"session_id": sid, "question_id": q["question_id"]}).json()["question"]
        else:
            q = c.post("/answer", json={"session_id": sid, "question_id": q["question_id"], "choice": a, "answer_ms": 5000}).json()["next_question"]
            waits.append(time.perf_counter() - t)
        shown.append(q["question"] if q else None)
    return shown, waits


def play_plain(actions, fail=()):
    c = client(); FAIL.update(fail)
    r = c.post("/session/start", json={"lecture": "D01"}).json()
    sid, q, shown = r["session_id"], r["question"], [r["question"]["question"]]
    for a in actions:
        if a == "skip":
            q = c.post("/skip", json={"session_id": sid, "question_id": q["question_id"]}).json()["question"]
        else:
            q = c.post("/answer", json={"session_id": sid, "question_id": q["question_id"], "choice": a, "answer_ms": 5000}).json()["next_question"]
        shown.append(q["question"] if q else None)
    return shown


pattern = [0, 1, 1, 0]   # đúng → sai → sai (đủ 2 lần, đổi khái niệm) → đúng
shown, waits = play_prefetch(pattern)
check("sinh sẵn: chuỗi câu (khái niệm + mức) giống hệt khi không sinh sẵn", shown == play_plain(pattern), (shown, play_plain(pattern)))
check("sinh sẵn: câu đầu và mỗi câu sau khi trả lời đều có gần như ngay (< 0.2 s, AI giả mất 0.3 s)", max(waits) < 0.2, waits)
check("sinh sẵn: mọi lần gọi AI chạy nền — 6 câu đầu + 1 câu bù + 2 nhánh × 4 câu, câu cuối không sinh thừa", len(slow_calls) == 15 and all(slow_calls), slow_calls)
check("sinh sẵn: sau 'Cho tôi câu khác' vẫn đúng luật", play_prefetch(["skip", 0, 1])[0] == play_plain(["skip", 0, 1]))
check("sinh sẵn: câu sinh sẵn thiếu căn cứ → đổi khái niệm như cũ", play_prefetch([0, 0], fail={"b"})[0] == play_plain([0, 0], fail={"b"}))
FAIL.clear()

print(f"\n{sum(RESULTS)}/{len(RESULTS)} test đạt")
sys.exit(0 if all(RESULTS) else 1)
