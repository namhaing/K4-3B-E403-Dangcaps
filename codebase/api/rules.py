"""Rule của lượt luyện — code thuần, KHÔNG dùng AI.

Tách riêng khỏi app.py để test được mà không cần server hay API key,
và để nói rõ với giám khảo: phần này là rule, AI chỉ nằm ở generate_question().
"""
TOTAL = 5            # số câu tính điểm trong một lượt
START_LEVEL = 2
MIN_ANSWERS = 3      # dưới số này thì "chưa đủ dữ liệu để đánh giá"
FAST_MS = 3000       # trả lời nhanh hơn ngưỡng này bị coi là có dấu hiệu đoán mò
MAX_FAST = 3         # từ 3 câu "quá nhanh" trở lên thì không kết luận
MAX_SAME_WRONG = 2   # sai liên tiếp 2 lần cùng khái niệm thì chuyển khái niệm khác (sửa lỗi kẹt 1 khái niệm cả lượt, 18/9)


def next_level(level: int, correct: bool) -> int:
    """Đúng → khó hơn 1 mức, sai → dễ hơn 1 mức, luôn trong 1–3."""
    return max(1, min(3, level + (1 if correct else -1)))


def pick_concept(order: list[str], answered: list[dict], excluded: set[str]) -> str | None:
    """
    order    : thứ tự khái niệm CỦA LƯỢT NÀY (API xáo ngẫu nhiên mỗi lượt để phủ cả slide, không luôn bắt đầu ở trang 3)
    answered : các câu đã trả lời, mỗi câu có concept_id, correct
    excluded : khái niệm đã thử mà AI không ra được câu có căn cứ

    Vừa sai → giữ khái niệm đó để luyện tiếp (mức đã giảm), NHƯNG sai liên tiếp đủ MAX_SAME_WRONG lần thì chuyển đi.
    Vừa đúng / chưa có câu → khái niệm tiếp theo chưa hỏi.
    Hỏi hết rồi → khái niệm sai nhiều nhất.
    """
    usable = [c for c in order if c not in excluded]
    if not usable:
        return None
    if answered and not answered[-1]["correct"] and answered[-1]["concept_id"] in usable:
        last = answered[-1]["concept_id"]
        streak = 0
        for a in reversed(answered):
            if a["concept_id"] != last or a["correct"]:
                break
            streak += 1
        if streak < MAX_SAME_WRONG:
            return last
    asked = {a["concept_id"] for a in answered}
    for c in usable:
        if c not in asked:
            return c
    wrong = {c: sum(1 for a in answered if a["concept_id"] == c and not a["correct"]) for c in usable}
    just_left = answered[-1]["concept_id"] if answered else None   # vừa sai 2 lần thì không quay lại ngay
    return max(usable, key=lambda c: (c != just_left, wrong[c]))


def is_low_confidence(answered: list[dict]) -> bool:
    """HAX G10: chưa đủ tín hiệu thì không kết luận học viên yếu phần nào."""
    fast = sum(1 for a in answered if a.get("answer_ms") is not None and a["answer_ms"] < FAST_MS)
    return len(answered) < MIN_ANSWERS or fast >= MAX_FAST


def review_target(answered: list[dict]) -> dict | None:
    """Chủ đề cần ôn = khái niệm sai nhiều nhất (bằng nhau thì lấy khái niệm sai gần nhất). Không sai câu nào → None."""
    wrong = [a for a in answered if not a["correct"]]
    if not wrong:
        return None
    counts = {}
    for a in wrong:
        counts[a["concept_id"]] = counts.get(a["concept_id"], 0) + 1
    top = max(counts.values())
    return next(a for a in reversed(wrong) if counts[a["concept_id"]] == top)
