"""Chạy thử generate_question() từ dòng lệnh (từ thư mục gốc repo).

    python -m codebase.ai.try_generate                       # khái niệm ai_layers, mức 2
    python -m codebase.ai.try_generate --concept attention --level 3
    python -m codebase.ai.try_generate --all                 # mỗi khái niệm 1 câu, in bảng tổng
    python -m codebase.ai.try_generate --concept day3_rag    # case ①: khái niệm ngoài slide
"""
import argparse
import json
import sys

from .generator import generate_question, load_concepts, load_pages

sys.stdout.reconfigure(encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--concept", default="ai_layers")
    p.add_argument("--level", type=int, default=2)
    p.add_argument("--all", action="store_true")
    a = p.parse_args()

    pages, concepts = load_pages(), load_concepts()

    if not a.all:
        print(json.dumps(generate_question(a.concept, a.level, pages, [], concepts), ensure_ascii=False, indent=2))
        return

    ok = 0
    ids = [c["concept_id"] for c in concepts["concepts"]]
    for cid in ids:
        r = generate_question(cid, a.level, pages, [], concepts)
        ok += r["status"] == "ok"
        detail = f"trang {r['page']}: {r['question'][:70]}" if r["status"] == "ok" else f"{r['reason']} {r['meta']['errors']}"
        print(f"{cid:18s} {r['status']:12s} lần thử={r['meta']['attempts']} {r['meta']['latency_ms']:>6}ms  {detail}")
    print(f"\nQua validator: {ok}/{len(ids)}")


if __name__ == "__main__":
    main()
