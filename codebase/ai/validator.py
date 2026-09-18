"""Validator: kiểm tra câu hỏi AI sinh ra TRƯỚC khi đưa cho học viên.

Mọi kiểm tra ở đây là code thuần, không gọi AI -> chạy nhanh, kết quả lặp lại được,
và dùng lại được trong eval (Duy gọi validate() để chấm tự động chiều "trích dẫn khớp trang").
"""
import re
import unicodedata

REQUIRED = ["concept_id", "level", "page", "evidence_quote", "question", "options", "answer", "explanation"]
MIN_QUOTE_CHARS = 20   # câu trích quá ngắn thì "khớp" không chứng minh được gì
MIN_LEAK_CHARS = 6     # đáp án ngắn hơn (vd "LLM") dễ trùng tình cờ trong đề, không coi là lộ

# Lựa chọn có tiền tố "A." / "B)" / "(C)": web tự đánh chữ cái, và khi đổi thứ tự thì nhãn sai
LETTER_PREFIX = re.compile(r"^\s*\(?[a-d]\s*[\.\):]\s+", re.I)
# Lựa chọn "gộp" kiểu "Cả A và B", "Tất cả đều đúng", "Không có đáp án nào": dễ tạo 2 đáp án đúng
# và phụ thuộc thứ tự lựa chọn. Phát hiện 18/9 ở case G04 (answer key chấm oan học viên).
META_OPTION = re.compile(
    r"^(cả|tất cả)\s+(a|b|c|d|hai|ba|bốn|các|những)\b"
    r"|\bđều\s+(đúng|sai)\s*\.?$"   # "Tất cả đều đúng." — không bắt "X và Y đều không ảnh hưởng…" (báo nhầm 18/9)
    r"|^không\s+(có\s+)?(đáp án|phương án|lựa chọn|ý)\s+nào"
    r"|\b(các|những)\s+(đáp án|phương án|lựa chọn|ý)\s+(trên|còn lại)\b",
    re.I,
)
# Mức 2 kiểu "mô tả → gọi tên": "…hiện tượng này được gọi là gì?", "Họ nên chọn loại AI nào?" — thật ra là mức 1.
# run-2: 7/11 câu mức 2 bị lỗi này; sau khi sửa prompt (run-3-muc2) vẫn còn 5/12 → chặn bằng code để AI sinh lại.
# Không bắt "X khác Y ở điểm nào?" / "Phát biểu nào đúng?" / "Điểm khác biệt … là gì?" (câu phân biệt hợp lệ).
NAMING = re.compile(
    r"\b(khái niệm|thuật ngữ|hiện tượng|loại|nhóm|công nghệ|tầng|bước|kỹ thuật|phương pháp)(\s+ai)?\s+(nào|gì)\b"
    r"|\b(được gọi là|gọi là|có tên là)\s+gì\b",
    re.I,
)
SHORT_OPTION_WORDS = 3  # cả 4 lựa chọn chỉ là tên khái niệm ("Machine Learning", "LLM"…) → đề đang hỏi tên


def normalize(text: str) -> str:
    """Chuẩn hoá để so khớp: bỏ khác biệt về xuống dòng, khoảng trắng, hoa/thường, kiểu dấu ngoặc."""
    text = unicodedata.normalize("NFC", str(text)).lower()
    text = re.sub(r"[“”«»\"„]", '"', text)
    text = re.sub(r"[‘’`]", "'", text)
    text = re.sub(r"[–—]", "-", text)
    text = text.replace("…", "...")
    return re.sub(r"\s+", " ", text).strip()


def validate(q: dict, *, concept: dict, level: int, pages: dict) -> list[str]:
    """Trả về danh sách lỗi. Danh sách rỗng = câu hỏi hợp lệ."""
    errors = []

    missing = [k for k in REQUIRED if k not in q]
    if missing:
        return [f"thiếu trường: {', '.join(missing)}"]

    # Đúng khái niệm và mức đã yêu cầu (AI không được tự đổi)
    if q["concept_id"] != concept["concept_id"]:
        errors.append(f"sai khái niệm: yêu cầu {concept['concept_id']}, nhận {q['concept_id']}")
    if q["level"] != level:
        errors.append(f"sai mức: yêu cầu {level}, nhận {q['level']}")

    # Nguồn sự thật (lớp ①): trang phải thuộc khái niệm, câu trích phải có nguyên văn trong trang
    try:
        page = int(q["page"])
    except (TypeError, ValueError):
        page = None
    if page not in concept["pages"]:
        errors.append(f"trang {q['page']} không thuộc khái niệm (hợp lệ: {concept['pages']})")
    else:
        quote = normalize(q["evidence_quote"])
        if len(quote) < MIN_QUOTE_CHARS:
            errors.append("câu trích quá ngắn")
        elif quote not in normalize(pages.get(str(page), "")):
            errors.append(f"câu trích không có nguyên văn trong trang {page}")

    # Cấu trúc trắc nghiệm
    opts = q["options"]
    if not isinstance(opts, list) or len(opts) != 4 or not all(isinstance(o, str) and o.strip() for o in opts):
        errors.append("options phải là 4 lựa chọn không rỗng")
    elif len({normalize(o) for o in opts}) != 4:
        errors.append("có 2 lựa chọn trùng nhau")
    else:
        if any(LETTER_PREFIX.match(o) for o in opts):
            errors.append("lựa chọn không được có tiền tố A./B./C./D.")
        meta = [o for o in opts if META_OPTION.search(normalize(o))]
        if meta:
            errors.append(f"không dùng lựa chọn gộp kiểu 'Cả A và B', 'Tất cả đều đúng', 'Không có đáp án nào': {meta}")
    if not isinstance(q["answer"], int) or not 0 <= q["answer"] <= 3:
        errors.append("answer phải là số 0-3")
    if not str(q["question"]).strip():
        errors.append("đề rỗng")

    # Lộ đáp án: nguyên văn lựa chọn đúng nằm sẵn trong đề
    if not errors:
        correct = normalize(opts[q["answer"]])
        if len(correct) >= MIN_LEAK_CHARS and correct in normalize(q["question"]):
            errors.append("đề lộ đáp án (lựa chọn đúng nằm nguyên văn trong đề)")

    # Mức 2 phải bắt học viên phân biệt, không chỉ nhớ tên. Lỗi ghi rõ cách sửa vì được gửi lại cho AI khi sinh lại.
    if level == 2 and not errors:
        naming = NAMING.search(normalize(q["question"]))
        if naming or all(len(o.split()) <= SHORT_OPTION_WORDS for o in opts):
            hint = f"'{naming.group(0)}'" if naming else "4 lựa chọn chỉ là tên khái niệm"
            errors.append(f"mức 2 đang hỏi dạng mô tả → gọi tên ({hint}); viết lại thành so sánh 2 khái niệm gần nhau "
                          "('X khác Y ở điểm nào?') hoặc 'phát biểu nào đúng' với 4 phát biểu đầy đủ, mỗi phát biểu sai là một hiểu nhầm")

    return errors
