"""Extract review candidates from VLearn chat logs; no third-party packages required."""

import argparse
import csv
import re
from collections import Counter, defaultdict, deque
from pathlib import Path


TOPICS = {
    "AI Product Thinking": ("jtbd", "job statement", "job executor", "pain", "problem statement", "mvp", "prd", "bài toán", "điểm đau"),
    "Product Discovery": ("survey", "interview", "khảo sát", "phỏng vấn", "evidence", "canvas", "baseline", "discovery"),
    "LLM Fundamentals": ("llm", "token", "context", "attention", "machine learning", "deep learning", "chatgpt", "chat gpt", "latency", "streaming"),
    "Prompt Engineering": ("prompt", "few-shot", "few shot", "system prompt", "constraints", "overfitting"),
    "AI Agent & Tool Calling": ("agent", "tool", "mcp", "react", "workflow", "function calling"),
    "Evaluation & Safety": ("golden", "eval", "quality bar", "hallucination", "hitl", "fallback", "precision", "recall", "kiểm thử"),
}
PATTERNS = {
    topic: [(term, re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.I)) for term in terms]
    for topic, terms in TOPICS.items()
}
REQUIRED = {"turn_id", "course_id", "cohort_hint", "lecture_code", "student_question", "is_preset"}
FIELDS = [
    "candidate_id", "turn_id", "course_id", "lecture_code", "chu_de_goi_y",
    "tu_khoa_khop", "is_preset", "trich_doan_ngan", "do_dai_cau_goc",
    "can_doc_day_du", "nguon_chatlog", "nguon_bai_giang", "trang_pdf",
    "hanh_vi_mong_muon", "trang_thai",
]


def classify(question):
    matches = {topic: [term for term, pattern in patterns if pattern.search(question)]
               for topic, patterns in PATTERNS.items()}
    topic = max(matches, key=lambda name: len(matches[name]))
    return (topic, matches[topic]) if matches[topic] else None


def select_candidates(path, limit, cohort, courses, lectures, include_preset):
    buckets = defaultdict(list)
    counts = Counter()
    seen_ids, seen_questions = set(), set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
        for row in reader:
            counts["read"] += 1
            if row["cohort_hint"] != cohort or row["course_id"] not in courses:
                continue
            if lectures and row["lecture_code"] not in lectures:
                continue
            counts["in_scope"] += 1
            preset = (row["is_preset"] or "").strip().lower() in {"true", "1", "yes"}
            if preset and not include_preset:
                continue
            question = row["student_question"] or ""
            normalized = " ".join(question.split())
            identity = (row["course_id"], row["lecture_code"], normalized.casefold())
            if not row["turn_id"] or not normalized or row["turn_id"] in seen_ids or identity in seen_questions:
                continue
            match = classify(question)
            if match is None:
                continue
            topic, terms = match
            seen_ids.add(row["turn_id"])
            seen_questions.add(identity)
            candidate = {
                "turn_id": row["turn_id"], "course_id": row["course_id"],
                "lecture_code": row["lecture_code"], "chu_de_goi_y": topic,
                "tu_khoa_khop": "; ".join(terms), "is_preset": str(preset).lower(),
                "trich_doan_ngan": normalized[:240], "do_dai_cau_goc": len(question),
                "can_doc_day_du": "CO" if len(normalized) > 240 else "KHONG",
                "nguon_chatlog": path.name, "nguon_bai_giang": "", "trang_pdf": "",
                "hanh_vi_mong_muon": "", "trang_thai": "UNG_VIEN_CHUA_DOI_CHIEU",
            }
            # Rank focused questions, then round-robin across the available topics.
            buckets[topic].append(((-len(terms), len(question), row["turn_id"]), candidate))
            counts["matched_unique"] += 1
    queues = {topic: deque(row for _, row in sorted(items, key=lambda item: item[0]))
              for topic, items in buckets.items()}
    selected = []
    while len(selected) < limit:
        added = False
        for topic in TOPICS:
            if queues.get(topic) and len(selected) < limit:
                selected.append(queues[topic].popleft())
                added = True
        if not added:
            break
    for index, row in enumerate(selected, 1):
        row["candidate_id"] = f"C{index:03d}"
    return selected, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("eval/candidates.csv"))
    parser.add_argument("--limit", type=int, default=24)
    parser.add_argument("--cohort", default="K4")
    parser.add_argument("--course", action="append", help="Exact course_id; repeatable; default K4P1")
    parser.add_argument("--lecture", action="append", help="Exact lecture_code; repeatable")
    parser.add_argument("--include-preset", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    if args.output.resolve() in {args.csv.resolve(), Path(__file__).with_name("golden.csv").resolve()}:
        parser.error("Output must not replace the input chatlog or golden.csv")
    if args.output.exists() and not args.overwrite:
        parser.error("Output exists; choose another --output or explicitly use --overwrite")
    try:
        rows, counts = select_candidates(args.csv, args.limit, args.cohort,
                                         set(args.course or ["K4P1"]), set(args.lecture or []),
                                         args.include_preset)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w" if args.overwrite else "x", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Read: {counts['read']}; in scope: {counts['in_scope']}; unique keyword matches: {counts['matched_unique']}")
    print(f"Exported {len(rows)} candidates -> {args.output}")
    for topic, count in Counter(row["chu_de_goi_y"] for row in rows).items():
        print(f"  {topic}: {count}")
    if len(rows) < 12:
        print("NOTE: fewer than 12 candidates; review filters. No cases were invented.")
    print("Manual review and slide sources required; tutor replies were not used as ground truth.")


if __name__ == "__main__":
    main()
