"""Test validator — chạy offline, không cần API key.

    python -m codebase.ai.test_validator
"""
import copy
import sys

from .validator import validate

sys.stdout.reconfigure(encoding="utf-8")

PAGES = {"3": "AI — chiếc ô lớn nhất: mọi hệ thống có yếu tố\n“thông minh”.\nMachine learning — học từ dữ liệu thay vì viết\nluật tay."}
CONCEPT = {"concept_id": "ai_layers", "name": "Các tầng AI", "pages": [3]}
GOOD = {
    "concept_id": "ai_layers",
    "level": 2,
    "page": 3,
    "evidence_quote": "Machine learning — học từ dữ liệu thay vì viết luật tay.",  # trên slide bị xuống dòng giữa câu
    "question": "Điểm khác biệt cốt lõi của Machine Learning so với cách lập trình truyền thống là gì?",
    "options": ["Học từ dữ liệu", "Viết luật bằng tay", "Luôn dùng mạng nơ-ron", "Chỉ xử lý văn bản"],
    "answer": 0,
    "explanation": "Slide trang 3: ML học từ dữ liệu thay vì viết luật tay.",
}


def check(name, change, expect_error):
    q = copy.deepcopy(GOOD)
    change(q)
    errors = validate(q, concept=CONCEPT, level=2, pages=PAGES)
    passed = (expect_error in " ".join(errors)) if expect_error else not errors
    print(f"{'PASS' if passed else 'FAIL'}  {name:45s} -> {errors or 'hợp lệ'}")
    return passed


CASES = [
    ("Câu hợp lệ (xuống dòng khác slide vẫn khớp)", lambda q: None, None),
    ("① Câu trích bịa, không có trong slide", lambda q: q.update(evidence_quote="Machine learning luôn cần GPU cực mạnh để chạy."), "không có nguyên văn"),
    ("① Trang không thuộc khái niệm", lambda q: q.update(page=17), "không thuộc khái niệm"),
    ("① Câu trích quá ngắn", lambda q: q.update(evidence_quote="học từ dữ liệu"), "quá ngắn"),
    ("④ Đề lộ đáp án", lambda q: q.update(question="ML học từ dữ liệu. Vậy ML có học từ dữ liệu không?"), "lộ đáp án"),
    ("AI tự đổi mức khó", lambda q: q.update(level=3), "sai mức"),
    ("AI tự đổi khái niệm", lambda q: q.update(concept_id="attention"), "sai khái niệm"),
    ("Chỉ có 3 lựa chọn", lambda q: q["options"].pop(), "4 lựa chọn"),
    ("2 lựa chọn trùng nhau", lambda q: q["options"].__setitem__(3, "học từ  dữ liệu"), "trùng"),
    ("answer ngoài 0-3", lambda q: q.update(answer=4), "answer"),
    ("Thiếu trường", lambda q: q.pop("evidence_quote"), "thiếu trường"),
    ("Lựa chọn có tiền tố 'A.' (case G04)", lambda q: q.update(options=["A. Học từ dữ liệu", "B. Viết luật bằng tay", "C. Luôn dùng mạng nơ-ron", "D. Chỉ xử lý văn bản"]), "tiền tố"),
    ("Lựa chọn 'Cả A và B' (case G04)", lambda q: q["options"].__setitem__(3, "Cả A và B"), "lựa chọn gộp"),
    ("Lựa chọn 'Cả ba đều không liên quan'", lambda q: q["options"].__setitem__(3, "Cả ba đều không liên quan"), "lựa chọn gộp"),
    ("Lựa chọn 'Tất cả các đáp án trên'", lambda q: q["options"].__setitem__(3, "Tất cả các đáp án trên"), "lựa chọn gộp"),
    ("Không báo nhầm: lựa chọn bắt đầu bằng 'Cả' bình thường", lambda q: q["options"].__setitem__(3, "Cảm biến thu dữ liệu ảnh"), None),
    ("Không báo nhầm: 'X và Y đều không…' là nội dung thật", lambda q: q["options"].__setitem__(3, "Cả temperature và top_p đều không ảnh hưởng đến cách chọn từ."), None),
    ("Lựa chọn 'Tất cả đều đúng.'", lambda q: q["options"].__setitem__(3, "Tất cả đều đúng."), "lựa chọn gộp"),
    ("Không báo nhầm: chữ 'A' đầu câu không phải tiền tố", lambda q: q["options"].__setitem__(3, "AI chỉ xử lý văn bản"), None),
]

if __name__ == "__main__":
    results = [check(*c) for c in CASES]
    print(f"\n{sum(results)}/{len(results)} test đạt")
    sys.exit(0 if all(results) else 1)
