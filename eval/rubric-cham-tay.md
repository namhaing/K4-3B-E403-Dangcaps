# Rubric chấm tay — 3 chiều code không tự chấm được

> Dùng cho các case `gen` có `status = ok` trong `eval/results/<lượt>.csv`.
> Điền **Y** (đạt) hoặc **N** (không đạt) vào 3 cột `answer_key_dung`, `dung_khai_niem`, `dung_muc`. Ghi tên vào `nguoi_cham`. Chọn N thì ghi lý do ngắn vào `ghi_chu_cham`.
> Chấm xong chạy `python -m eval.run_eval --summarize <lượt>` để tính lại %.

**Cách chấm:** mở slide Day 1 đúng trang ở cột `page`. Chấm từng chiều độc lập, chỉ dựa vào slide, không dựa vào hiểu biết riêng ngoài slide.

---

## 1. `answer_key_dung`: đáp án đánh dấu đúng có thật sự đúng không?

**Y** khi **cả 3** điều sau đều đúng:
1. Lựa chọn ở cột `answer` đúng theo nội dung slide trang `page`.
2. **Không** có lựa chọn nào khác cũng đúng theo slide (chỉ 1 đáp án đúng).
3. `explanation` không nói điều trái với slide.

**N** nếu vi phạm một trong ba.

| Ví dụ | Chấm |
|---|---|
| Hỏi "tầng nào bao trùm tất cả", đáp án "AI". Slide trang 3: AI là chiếc ô lớn nhất | Y |
| Hỏi "LLM thuộc nhóm nào", 2 lựa chọn "Generative AI" và "Deep Learning" đều đúng theo sơ đồ trang 3 | **N**: có 2 đáp án đúng |
| Đáp án đúng nhưng giải thích nói "LLM không thuộc ML" | **N**: giải thích sai kiến thức |

## 2. `dung_khai_niem`: câu hỏi có đúng khái niệm được yêu cầu không?

**Y** khi phần cốt lõi của câu hỏi (điều học viên phải biết mới trả lời được) thuộc khái niệm ở cột `concept_id`, xem tên khái niệm trong `codebase/data/concepts.json`.

**N** khi câu hỏi thật ra kiểm tra một khái niệm khác, dù trang trích dẫn có đúng.

| Ví dụ | Chấm |
|---|---|
| `attention`, câu hỏi: "mỗi token 'nhìn sang' các token khác để làm gì?" | Y |
| `attention`, câu hỏi: "Transformer ra đời năm nào?" | **N**: đây là lịch sử AI, không phải attention |

## 3. `dung_muc`: câu hỏi có đúng mức khó yêu cầu (cột `level`) không?

| Mức | Học viên phải làm gì để trả lời | Dấu hiệu nhận ra |
|---|---|---|
| **1 · Nhận biết** | Nhớ một định nghĩa hoặc sự kiện **nói thẳng** trên slide | "X là gì?", "Theo slide, X được mô tả là…" |
| **2 · Phân biệt** | So sánh **2 khái niệm gần nhau**, hoặc chọn phát biểu đúng/sai mà các lựa chọn sai là hiểu nhầm hay gặp | "X khác Y ở điểm nào?", "Phát biểu nào SAI về X?" |
| **3 · Áp dụng** | Đọc một **tình huống mới không có trên slide** và dùng khái niệm để chọn cách hiểu hoặc cách làm | "Một nhóm muốn… nên chọn…", "Trong tình huống sau…" |

**Y** khi câu hỏi đúng mức yêu cầu. **N** khi lệch mức, dễ hơn hay khó hơn đều tính N.

| Ví dụ | Mức yêu cầu | Chấm |
|---|---|---|
| "Khái niệm nào sau đây miêu tả chính xác về AI?" | 2 | **N**: đây là câu nhận biết (mức 1) |
| "Discriminative AI khác Generative AI ở đầu ra thế nào?" | 2 | Y |
| "Ứng dụng cần kết quả ổn định giữa các lần chạy, nên đặt temperature thế nào?" | 3 | Y |

---

## Kiểm tra định nghĩa có rõ không (bắt buộc cho R4)

Sau lượt 2, nhờ **1 người ngoài nhóm** chấm độc lập **5 case** (chọn 2 case Y, 2 case N, 1 case khó phân vân), rồi so với người trong nhóm:
- Lệch **0–1/5 case** trên mỗi chiều: định nghĩa đủ rõ.
- Lệch **≥ 2/5 case**: định nghĩa còn mơ hồ. **Viết lại định nghĩa** trước khi chấm tiếp, và ghi lại lần sửa trong `spec.md` §7.

Ghi kết quả so sánh vào cuối file `eval/run-N.md` tương ứng.
