# Luồng hoạt động — VLearn Solo Arena (bản core, cập nhật 18/9)

> Thay cho bản CP2 cũ (test xếp hạng → rank → ghép đối thủ → Win Bonus). Bản cũ đã bị cắt vì có 5 quyết định AI và phần lõi là thuật toán Elo/IRT, không cần AI. Lý do chi tiết: `SOLO-ARENA-HANDOFF.md` mục 3.

**Mức prototype nhắm tới:** Working. Lời gọi AI thật nằm ở bước sinh câu hỏi. Phần nào mock thì ghi nhãn "Mock" trên UI.

## Lát cắt

Một học viên vừa xong buổi học, đang trong một lượt luyện 5 câu · cần câu tiếp theo vừa sức · hệ thống chọn khái niệm × mức khó theo câu vừa rồi đúng hay sai, rồi **AI sinh câu hỏi bám đúng trang slide của khái niệm đó** · kết quả là câu hỏi kèm `[trang N]`, cuối lượt là một chủ đề cần ôn có dẫn nguồn.

## Flow chính (happy path)

```text
[Màn 1] Chọn buổi: "Day 1: AI, ML, DL, LLM"
        dòng cố định: "Câu hỏi chỉ lấy từ slide Day 1"
    ↓ Bấm "Bắt đầu luyện 5 câu"
[Màn 2] Câu hỏi 1/5 · Mức 2
        đề trắc nghiệm, 4 lựa chọn, [trang N]
        nút phụ: "Cho tôi câu khác" · "Báo câu sai"
    ↓ Chọn đáp án
[Màn 3] Phản hồi: Đúng/Sai + đáp án đúng + giải thích + câu trích nguyên văn từ slide [trang N]
    ↓ "Câu tiếp" (lặp lại màn 2 → 3 cho đến câu 5)
[Màn 4] Kết quả: bảng 5 câu (khái niệm, đúng/sai)
        + 1 chủ đề cần ôn kèm [trang N] và câu trích
        (không có rank, không có bảng xếp hạng)
```

## Bên trong mỗi lần bấm "Câu tiếp"

```text
Web ──POST /answer {choice, answer_ms}──▶ API
  1. Chấm đúng/sai so với đáp án                                     (rule)
  2. Mức khó: đúng → +1, sai → −1, kẹp trong 1–3                     (rule)
  3. Khái niệm: vừa sai → giữ khái niệm đó; vừa đúng → khái niệm chưa hỏi (rule)
  4. generate_question(concept, level, pages, history)               (AI thật)
  5. Validator: trích dẫn có nằm trong trang N? đáp án có trong 4 lựa chọn?
     đề có lộ đáp án? → fail thì sinh lại 1 lần → fail tiếp thì trả no_evidence
  6. Ghi trace vào eval/traces/*.jsonl
◀── {correct, explanation, page, next_question, status}
```

## Bốn đường đi

| Đường đi | Khi nào | Học viên thấy gì |
|---|---|---|
| Happy | Câu hỏi qua được validator | Câu hỏi kèm `[trang N]`, phản hồi có câu trích slide |
| Low-confidence | Dưới 3 câu đã trả lời, **hoặc** ≥3 câu trả lời dưới 3 giây | Màn kết quả ghi "Chưa đủ dữ liệu để đánh giá. Làm thêm 2 câu?", không kết luận điểm yếu |
| Failure | Validator fail 2 lần, hoặc API LLM lỗi | "Chưa có căn cứ trong slide cho khái niệm này" → chuyển sang khái niệm khác. Không bao giờ hiện câu không có nguồn |
| Correction | Bấm "Báo câu sai" (chọn lý do) hoặc "Cho tôi câu khác" | Câu bị báo không tính điểm, hệ thống sinh câu thay thế và ghi log. "Câu khác" giữ nguyên khái niệm và mức |

## Điểm an toàn thể hiện trên UI

- Chỉ hỏi trong slide Day 1, mỗi câu đều có nguồn `[trang N]`.
- Không kết luận học viên yếu khi chưa đủ dữ liệu.
- Kết quả chỉ học viên đó thấy. Không có rank, không có bảng xếp hạng trong core.
- Chấm đúng/sai bằng đáp án, không để AI tự chấm.
- Thoát lượt bất kỳ lúc nào, không mất gì.

## Phần mở rộng (chỉ làm sau khi core xong)

Thách đấu qua link, XP và bảng xếp hạng opt-in, xem `ke-hoach-nhom.md` mục 9. Phần này không thêm quyết định AI mới.
