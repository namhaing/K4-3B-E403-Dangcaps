"""Chạy golden set qua hệ thống thật và chấm tự động. (Duy viết — Nam chạy từng lượt)

Chạy từ thư mục gốc repo:
    python -m eval.run_eval --label run-1          # chạy + chấm tự động → eval/run-1.md + eval/results/run-1.csv
    python -m eval.run_eval --summarize run-1      # sau khi người chấm điền cột chấm tay trong CSV → tính lại bảng

Hai loại case trong golden-day1.csv:
    gen  : gọi thẳng generate_question() (AI thật)
    flow : chạy cả API (rule + AI thật) qua TestClient, như một học viên bấm trên web

Chiều TỰ ĐỘNG (code chấm):   hành vi đúng · qua validator lần đầu · không lộ đáp án · không chép cụm câu trích · không lặp câu cũ · không theo chỉ thị lạ
Chiều CHẤM TAY (người chấm): answer key đúng · đúng mức khó · đúng khái niệm   → xem eval/rubric-cham-tay.md
"""
import argparse
import csv
import json
import re
import sys
import warnings
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore", message=".*httpx.*starlette.testclient.*")  # cảnh báo thư viện, không ảnh hưởng kết quả
EVAL = Path(__file__).resolve().parent
MANUAL = ["answer_key_dung", "dung_muc", "dung_khai_niem"]
REPEAT_RATIO = 0.8   # giống câu cũ ≥ 80% ký tự → coi là lặp
COPY_SYLLABLES = 4   # đề chép ≥ 4 tiếng liên tiếp của câu trích → gợi ý quá mạnh


# ---------------- chấm tự động ----------------

def syllables(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def copies_quote(question: str, quote: str, n: int = COPY_SYLLABLES) -> bool:
    q, e = syllables(question), syllables(quote)
    grams = {tuple(e[i:i + n]) for i in range(len(e) - n + 1)}
    return any(tuple(q[i:i + n]) in grams for i in range(len(q) - n + 1))


def leak(r: dict) -> bool:
    """Lộ đáp án: nguyên văn lựa chọn đúng nằm sẵn trong đề (kể cả đáp án ngắn như 'AI', validator chỉ xét từ 6 ký tự)."""
    ans = syllables(r["options"][r["answer"]])
    q = syllables(r["question"])
    return bool(ans) and any(q[i:i + len(ans)] == ans for i in range(len(q) - len(ans) + 1))


def copies_hint(r: dict) -> bool:
    """Gợi ý quá mạnh: đề chép cụm đặc trưng (≥ 4 tiếng liên tiếp) của câu trích, bất kể đáp án dài hay ngắn.
    Vd đề hỏi 'khái niệm nào là 'chiếc ô lớn nhất'' → không học bài cũng đoán ra. (case L4-03, 18/9)"""
    return copies_quote(r["question"], r["evidence_quote"])


def repeats(question: str, history: list[str]) -> bool:
    return any(SequenceMatcher(None, question.lower(), h.lower()).ratio() >= REPEAT_RATIO for h in history)


# ---------------- chạy từng loại case ----------------

def run_gen(case, pages, concepts, generate):
    history = json.loads(case["history"] or "[]")
    level = int(case["level"])
    r = generate(case["concept_id"], level, pages, [{"question": h} for h in history], concepts)
    row = {"status": r["status"], "reason": r.get("reason", ""), "attempts": r["meta"].get("attempts", 0),
           "latency_ms": r["meta"].get("latency_ms", 0), "errors": json.dumps(r["meta"].get("errors", []), ensure_ascii=False)}
    ok_behavior = r["status"] == case["expect_status"] and (not case["expect_reason"] or row["reason"] == case["expect_reason"])
    row["hanh_vi_dung"] = ok_behavior
    if r["status"] == "ok":
        row.update(page=r["page"], question=r["question"], options=" || ".join(r["options"]),
                   answer=f"{r['answer']}: {r['options'][r['answer']]}", evidence_quote=r["evidence_quote"],
                   explanation=r["explanation"])
        row["qua_lan_dau"] = r["meta"]["attempts"] == 1
        row["khong_lo_dap_an"] = not leak(r)
        row["khong_chep_cau_trich"] = not copies_hint(r)
        row["khong_lap"] = not repeats(r["question"], history)
        if case["nhom"] == "lop3":
            text = json.dumps(r, ensure_ascii=False).lower()
            row["khong_theo_chi_thi_la"] = "bỏ qua" not in text and "không cần trích dẫn" not in text
        # Case có yêu cầu riêng (cột kiem_them): hành vi chỉ đúng khi chiều đó cũng đạt
        extra = case.get("kiem_them", "").strip()
        if extra:
            row["hanh_vi_dung"] = ok_behavior and row.get(extra, False)
    elif case.get("kiem_them", "").strip():
        row["hanh_vi_dung"] = False
    return row


def run_flow(case, pages, concepts, generate):
    from fastapi.testclient import TestClient

    from codebase.api.app import create_app

    last = {}

    def spy(*a, **k):  # ghi lại đáp án câu vừa sinh để "cố tình" trả lời đúng/sai theo kịch bản
        r = generate(*a, **k)
        last.update(r)
        return r

    c = TestClient(create_app(generate=spy, pages=pages, concepts=concepts))
    script, _, opt = case["flow"].partition("|")
    row = {}

    if script == "inspect_question":
        r = c.post("/session/start", json={"lecture": concepts["lecture"]}).json()
        q = r["question"] or {}
        row.update(status=r["status"], question=q.get("question", ""))
        row["hanh_vi_dung"] = bool(q) and not any(k in q for k in ("answer", "explanation", "evidence_quote"))
        return row

    if script == "foreign_session":
        code = c.get("/session/khong-phai-cua-ban/result").status_code
        row.update(status=f"http_{code}", hanh_vi_dung=code == 404)
        return row

    ms = int(opt.split("=")[1]) if opt.startswith("ms=") else 6000
    r = c.post("/session/start", json={"lecture": concepts["lecture"]}).json()
    sid, q = r["session_id"], r["question"]
    for step in script.split(","):
        if q is None:
            break
        choice = last["answer"] if step == "right" else (last["answer"] + 1) % 4
        q = c.post("/answer", json={"session_id": sid, "question_id": q["question_id"], "choice": choice, "answer_ms": ms}).json()["next_question"]
    res = c.get(f"/session/{sid}/result").json()
    row.update(status=res["status"], question=f"{len(res['items'])} câu đã trả lời", hanh_vi_dung=res["status"] == case["expect_status"])
    return row


# ---------------- tổng hợp ----------------

def pct(rows, key):
    vals = [r[key] for r in rows if r.get(key) not in ("", None)]
    vals = [v if isinstance(v, bool) else str(v).strip().upper() in ("TRUE", "Y", "1") for v in vals]
    return (sum(vals), len(vals))


def fmt(p):
    return f"{p[0]}/{p[1]} ({p[0] / p[1] * 100:.0f}%)" if p[1] else "chưa có số liệu"


def summarize(label: str, rows: list[dict], meta: str):
    ok_rows = [r for r in rows if r.get("loai_test") == "gen" and r.get("expect_status") == "ok"]
    ok13 = [r for r in rows if r.get("nhom") in ("lop1", "lop3")]
    ok2 = [r for r in rows if r.get("nhom") == "lop2"]
    ra_cau = (sum(1 for r in ok_rows if r.get("status") == "ok"), len(ok_rows))
    dims = [
        ("Ra câu hợp lệ (trích dẫn khớp trang, qua validator) — case cần ra câu", ra_cau, "≥ 80%", "tự động"),
        ("Qua validator ngay lần đầu", pct(ok_rows, "qua_lan_dau"), "(theo dõi)", "tự động"),
        ("Không lộ đáp án (đề không chứa nguyên văn đáp án đúng)", pct(ok_rows, "khong_lo_dap_an"), "≥ 90% (lộ ≤ 10%)", "tự động"),
        ("Không chép cụm câu trích vào đề (gợi ý quá mạnh)", pct(ok_rows, "khong_chep_cau_trich"), "(Nam + Duy chốt)", "tự động"),
        ("Không lặp câu đã hỏi", pct(ok_rows, "khong_lap"), "(theo dõi)", "tự động"),
        ("Case ① và ③ xử lý đúng", pct(ok13, "hanh_vi_dung"), "100%", "tự động"),
        ("Case ② (chưa đủ dữ liệu) xử lý đúng", pct(ok2, "hanh_vi_dung"), "100%", "tự động"),
        ("Answer key đúng", pct(ok_rows, "answer_key_dung"), "≥ 90%", "chấm tay"),
        ("Đúng khái niệm đã chọn", pct(ok_rows, "dung_khai_niem"), "≥ 80%", "chấm tay"),
        ("Đúng mức khó yêu cầu", pct(ok_rows, "dung_muc"), "≥ 70%", "chấm tay"),
    ]
    lines = [f"# Kết quả eval — {label}", "", meta, "",
             "> Quality bar ở cột 3 là bản **dự kiến** (canvas). Bar chính thức chốt trong `spec.md` §7 lúc 21:00 18/9, sau đó không sửa.",
             "> Ghi đủ mọi case, kể cả case fail. Không sửa số tay.", "",
             "## Theo chiều chất lượng", "", "| Chiều | Kết quả | Bar dự kiến | Cách chấm |", "|---|---|---|---|"]
    lines += [f"| {d} | {fmt(p)} | {b} | {how} |" for d, p, b, how in dims]
    lines += ["", "## Từng case", "", "| Case | Nhóm | Nguồn | Mong đợi | Thực tế | Hành vi đúng | Lần thử | Trang | Cờ tự động | Câu hỏi |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        flags = [n for n, k in (("lộ đáp án", "khong_lo_dap_an"), ("chép cụm câu trích", "khong_chep_cau_trich"), ("lặp câu", "khong_lap"), ("theo chỉ thị lạ", "khong_theo_chi_thi_la"))
                 if str(r.get(k, "")).strip().upper() in ("FALSE", "N", "0")]
        exp = r["expect_status"] + (f" / {r['expect_reason']}" if r.get("expect_reason") else "")
        act = str(r.get("status", "")) + (f" / {r['reason']}" if r.get("reason") else "")
        hv = "✅" if str(r.get("hanh_vi_dung")).upper() in ("TRUE", "Y", "1") else "❌"
        q = str(r.get("question", "")).replace("|", "/")[:80]
        lines.append(f"| {r['case_id']} | {r['nhom']} | {r['nguon']} | {exp} | {act} | {hv} | {r.get('attempts', '')} | {r.get('page', '')} | {', '.join(flags) or '—'} | {q} |")
    fails = [r for r in rows if str(r.get("hanh_vi_dung")).upper() not in ("TRUE", "Y", "1")]
    lines += ["", "## Case fail — lỗi validator ghi lại", ""]
    lines += [f"- **{r['case_id']}**: {r.get('status')} {r.get('reason', '')} — `{str(r.get('errors', ''))[:300]}`" for r in fails] or ["- (không có)"]
    lines += ["", "## Phân tích nguyên nhân (Nam viết sau khi đọc từng case fail)", "", "- ...", ""]
    (EVAL / f"{label}.md").write_text("\n".join(lines), encoding="utf-8")
    start = lines.index("## Theo chiều chất lượng")
    print("\n".join(lines[start + 2:start + 4 + len(dims)]))
    print(f"\n→ {EVAL / (label + '.md')}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--label", help="tên lượt chạy, vd run-1")
    p.add_argument("--summarize", help="tính lại bảng từ eval/results/<label>.csv sau khi chấm tay")
    p.add_argument("--only", help="chỉ chạy các case_id này, cách nhau bằng dấu phẩy (chạy thử, không dùng cho số liệu nộp)")
    a = p.parse_args()

    if a.summarize:
        path = EVAL / "results" / f"{a.summarize}.csv"
        rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
        summarize(a.summarize, rows, f"Tính lại từ `{path.name}` lúc {datetime.now():%H:%M %d/%m} (đã gồm cột chấm tay).")
        return

    from codebase.ai import generate_question, llm, load_concepts, load_pages

    pages, concepts = load_pages(), load_concepts()
    cases = list(csv.DictReader(open(EVAL / "golden-day1.csv", encoding="utf-8-sig")))
    if a.only:
        cases = [c for c in cases if c["case_id"] in a.only.split(",")]
    label = a.label or f"run-{datetime.now():%H%M}"

    rows = []
    for c in cases:
        run = run_gen if c["loai_test"] == "gen" else run_flow
        try:
            r = run(c, pages, concepts, generate_question)
        except Exception as e:
            r = {"status": "crash", "reason": f"{type(e).__name__}: {e}"[:200], "hanh_vi_dung": False}
        rows.append({**c, **r, **{m: "" for m in MANUAL}, "nguoi_cham": "", "ghi_chu_cham": ""})
        print(f"{c['case_id']:6s} {'✅' if r.get('hanh_vi_dung') else '❌'} {r.get('status')} {r.get('reason', '')}")

    out = EVAL / "results" / f"{label}.csv"
    out.parent.mkdir(exist_ok=True)
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    meta = (f"Chạy lúc {datetime.now():%H:%M %d/%m/%Y} · model `{llm.PROVIDER}/{llm.MODEL}` · {len(rows)} case · "
            f"file chi tiết (có cột chấm tay): `eval/results/{label}.csv`")
    summarize(label, rows, meta)


if __name__ == "__main__":
    main()
