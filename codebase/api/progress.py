"""Lưu tiến độ học viên QUA NHIỀU LƯỢT, theo từng khái niệm (Duy).

Trước đây mỗi lượt độc lập: tắt trang là mất, "chỗ yếu" chỉ dựa trên 5 câu của 1 lượt.
Giờ mỗi câu trả lời (trừ câu đoán mò) được cộng dồn vào hồ sơ của học viên.

Riêng tư: học viên chỉ có MÃ NGẪU NHIÊN do trình duyệt tạo (không tên, không email, không MSSV).
Không có endpoint nào liệt kê hồ sơ của người khác.
File lưu: codebase/data/progress.json (không commit — đã chặn trong .gitignore).
"""
import json
import re
import threading
from datetime import datetime
from pathlib import Path

LEARNER_ID = re.compile(r"^[A-Za-z0-9-]{8,64}$")
RECENT = 5  # giữ 5 kết quả gần nhất của mỗi khái niệm
KEEP = 5    # giữ 5 câu sai gần nhất + 6 câu trích gần nhất để học viên ôn lại


def valid_learner(learner_id: str | None) -> bool:
    return bool(learner_id) and bool(LEARNER_ID.match(learner_id))


class ProgressStore:
    """path=None → chỉ lưu trong RAM (dùng khi test)."""

    def __init__(self, path: Path | None = None):
        self.path = path
        self.lock = threading.Lock()
        self.data: dict = {}
        if path and path.exists():
            try:
                self.data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self.data = {}  # file hỏng thì bắt đầu lại, không làm sập API

    def get(self, learner_id: str) -> dict:
        """{concept_id: {"attempts", "correct", "recent": [bool…], "last_level", "updated"}}"""
        return self.data.get(learner_id, {})

    def record(self, learner_id: str, concept_id: str, correct: bool, level: int, detail: dict | None = None):
        """detail: câu hỏi vừa làm (đề, lựa chọn, đáp án, giải thích, câu trích, trang) — dùng cho màn "Ôn lại kiến thức"."""
        with self.lock:
            c = self.data.setdefault(learner_id, {}).setdefault(
                concept_id, {"attempts": 0, "correct": 0, "recent": [], "last_level": level})
            c["attempts"] += 1
            c["correct"] += int(correct)
            c["recent"] = (c["recent"] + [bool(correct)])[-RECENT:]
            c["last_level"] = level
            c["updated"] = datetime.now().isoformat(timespec="seconds")
            if detail:
                if not correct:
                    c["mistakes"] = (c.get("mistakes", []) + [{**detail, "at": c["updated"]}])[-KEEP:]
                quote = {"page": detail.get("page"), "quote": detail.get("evidence_quote")}
                if quote["quote"] and quote not in c.get("quotes", []):
                    c["quotes"] = (c.get("quotes", []) + [quote])[-(KEEP + 1):]
            if self.path:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=1), encoding="utf-8")
