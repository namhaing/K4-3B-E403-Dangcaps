# Phiếu chấm lại 5 câu — người NGOÀI nhóm

> **Mục đích:** kiểm tra định nghĩa chấm của nhóm có đủ rõ để người khác chấm ra cùng kết quả không (rubric mục "Kiểm tra định nghĩa có rõ không").
> **Thời gian:** khoảng 15–20 phút.

## Hướng dẫn cho người chấm

1. Đọc 3 mục định nghĩa trong [`eval/rubric-cham-tay.md`](rubric-cham-tay.md): `answer_key_dung`, `dung_khai_niem`, `dung_muc` (khoảng 5 phút).
2. Với mỗi câu dưới đây, mở **đúng trang slide** ghi ở câu đó (slide Day 1 trên máy của nhóm — file PDF không có trên repo) và chấm **chỉ dựa vào slide**.
3. Điền **Y** (đạt) hoặc **N** (không đạt) vào 3 ô. Chấm N thì ghi lý do ngắn.
4. **Không** mở `eval/results/`, không hỏi nhóm chấm thế nào, không mở phần "Dành cho Duy" ở cuối file.

Nhắc nhanh 3 chiều:
- **Answer key đúng:** lựa chọn được đánh dấu đúng theo slide · không có lựa chọn nào khác cũng đúng · giải thích không nói trái slide.
- **Đúng khái niệm:** điều học viên phải biết để trả lời thuộc đúng khái niệm yêu cầu.
- **Đúng mức khó:** mức 1 nhận biết · mức 2 **phân biệt** (so sánh 2 khái niệm gần nhau, hoặc chọn phát biểu đúng mà lựa chọn sai là hiểu nhầm hay gặp — dạng "mô tả → gọi tên" là mức 1) · mức 3 tình huống mới không có trên slide. Lệch mức (dễ hơn hay khó hơn) đều là N.

Người chấm: `Claude (chấm hộ theo yêu cầu Duy)` · Thời gian chấm: `2026-09-18`
---

## Câu 1

- **Khái niệm yêu cầu:** Giới hạn của LLM: knowledge cutoff, hallucination, học đường tắt
- **Mức yêu cầu:** 2 · Phân biệt
- **Trang slide làm căn cứ:** 20

**Đề:** Trong bối cảnh làm việc với LLM, phát biểu nào sau đây về các giới hạn của mô hình là đúng?

- **A.** Knowledge cutoff giúp mô hình luôn cập nhật thông tin mới nhất từ internet.
- **B.** Hallucination là hiện tượng mô hình tự tin đưa ra kết quả sai mà không tra cứu sự thật.
- **C.** Học đường tắt giúp mô hình hiểu ngữ nghĩa của câu một cách chính xác hơn.
- **D.** Knowledge cutoff cho phép mô hình ghi nhớ tất cả thông tin mà nó đã học.

**Đáp án AI đánh dấu:** B
**Giải thích của AI:** Phát biểu đúng là về hallucination, nơi mô hình có thể tự tin đưa ra thông tin sai lệch mà không kiểm chứng sự thật, như đã nêu trong slide.

| Chiều | Y / N | Lý do (nếu N) |
|---|---|---|
| Answer key đúng | Y | |
| Đúng khái niệm | Y | |
| Đúng mức khó | Y | |
---

## Câu 2

- **Khái niệm yêu cầu:** Quy trình tạo LLM: pre-training, SFT, RLHF, luyện suy luận
- **Mức yêu cầu:** 2 · Phân biệt
- **Trang slide làm căn cứ:** 18

**Đề:** Một nhóm nghiên cứu đang tìm hiểu về quy trình huấn luyện LLM. Họ muốn biết lý do tại sao cần phải có cả bước SFT và RLHF trong quy trình này. Phát biểu nào dưới đây là đúng?

- **A.** SFT giúp model học kiến thức từ hàng triệu tài liệu mà không cần phản hồi từ con người.
- **B.** RLHF giúp model tạo ra nhiều câu trả lời khác nhau cho cùng một câu hỏi.
- **C.** SFT và RLHF đều chỉ tập trung vào việc cải thiện khả năng suy luận của model.
- **D.** Chỉ cần SFT là đủ để model có thể trả lời phỏng vấn một cách chính xác.

**Đáp án AI đánh dấu:** B
**Giải thích của AI:** Bước RLHF giúp model cải thiện khả năng trả lời bằng cách học từ phản hồi của con người, điều này là cần thiết để trở thành một trợ lý hữu ích.

| Chiều | Y / N | Lý do (nếu N) |
|---|---|---|
| Answer key đúng | N | B chỉ là bước "model viết nhiều câu trả lời" trong pipeline RLHF (slide 19), không nêu lý do cần *cả* SFT và RLHF. A cũng sai: gán cho SFT việc "học kiến thức từ hàng triệu tài liệu" — đó là mô tả pre-training ("đọc cả thư viện"), không phải SFT ("học theo ví dụ mẫu"). Không phát biểu nào khớp lý do slide nêu ("đọc vạn cuốn sách chưa chắc biết trả lời phỏng vấn — cần SFT, RLHF"). |
| Đúng khái niệm | Y | |
| Đúng mức khó | Y | |
---

## Câu 3

- **Khái niệm yêu cầu:** Các tầng AI ⊃ ML ⊃ Deep Learning ⊃ GenAI ⊃ LLM
- **Mức yêu cầu:** 2 · Phân biệt
- **Trang slide làm căn cứ:** 3

**Đề:** Trong các khái niệm về AI, phát biểu nào sau đây mô tả đúng về Generative AI?

- **A.** Generative AI chỉ là một phần nhỏ của AI, không có khả năng sinh nội dung.
- **B.** Generative AI là công nghệ giúp nhận diện giọng nói và hình ảnh.
- **C.** Generative AI có khả năng sinh ra nội dung mới như văn bản và hình ảnh.
- **D.** Generative AI là một phương pháp học máy truyền thống.

**Đáp án AI đánh dấu:** C
**Giải thích của AI:** Generative AI được định nghĩa là khả năng sinh ra nội dung mới, bao gồm văn bản, ảnh và code, điều này phân biệt nó với các khái niệm khác trong AI.

| Chiều | Y / N | Lý do (nếu N) |
|---|---|---|
| Answer key đúng | Y | |
| Đúng khái niệm | N | Câu hỏi và các lựa chọn (B: "nhận diện giọng nói, hình ảnh" vs C: "sinh nội dung") thực ra phân biệt Discriminative AI vs Generative AI — khái niệm `ai_types` ở trang 4 — chứ không kiểm tra quan hệ *bao trùm* giữa các tầng AI⊃ML⊃DL⊃GenAI⊃LLM (`ai_layers`, trang 3) như yêu cầu. |
| Đúng mức khó | N | Dạng "phát biểu nào mô tả đúng về X" — đúng khuôn ví dụ mức-1 trong rubric-cham-tay.md ("Khái niệm nào sau đây miêu tả chính xác về AI?" → N vì là nhận biết), không phải phân biệt 2 khái niệm gần nhau theo đúng nghĩa mức 2. |
---

## Câu 4

- **Khái niệm yêu cầu:** Giới hạn của LLM: knowledge cutoff, hallucination, học đường tắt
- **Mức yêu cầu:** 2 · Phân biệt
- **Trang slide làm căn cứ:** 20

**Đề:** Một nhóm nghiên cứu đang tìm hiểu về cách mà các mô hình ngôn ngữ sinh ra thông tin. Họ nhận thấy rằng mô hình có thể tạo ra câu trả lời tự tin nhưng không chính xác. Điều này liên quan đến khái niệm nào dưới đây?

- **A.** Knowledge cutoff, khi mô hình không biết thông tin mới sau một thời điểm nhất định.
- **B.** Hallucination, khi mô hình tạo ra câu trả lời không chính xác nhưng vẫn tự tin.
- **C.** Học đường tắt, khi mô hình dựa vào các yếu tố không liên quan để đưa ra kết luận.
- **D.** Context window, khi mô hình chỉ xem xét một phần nhỏ thông tin để đưa ra dự đoán.

**Đáp án AI đánh dấu:** B
**Giải thích của AI:** Khái niệm hallucination đề cập đến việc mô hình tạo ra câu trả lời sai nhưng vẫn thể hiện sự tự tin, như đã nêu trong slide.

| Chiều | Y / N | Lý do (nếu N) |
|---|---|---|
| Answer key đúng | Y | |
| Đúng khái niệm | Y | |
| Đúng mức khó | N | Đây là "mô tả hiện tượng → gọi tên khái niệm" (khoác vỏ "một nhóm nghiên cứu nhận thấy..."), đúng ví dụ mức-1 trong rubric-cham-tay.md dù có tình huống, không phải mức 2. |
---

## Câu 5

- **Khái niệm yêu cầu:** Token và context (bàn làm việc có hạn)
- **Mức yêu cầu:** 2 · Phân biệt
- **Trang slide làm căn cứ:** 14

**Đề:** Một nhóm nghiên cứu muốn tối ưu hóa việc sử dụng AI trong việc xử lý văn bản. Họ cần phân biệt giữa hai khái niệm token và context. Phát biểu nào sau đây là chính xác về sự khác nhau giữa chúng?

- **A.** Token là đơn vị mà model sử dụng để đọc và xử lý văn bản, trong khi context là lượng chữ mà model có thể xem cùng một lúc.
- **B.** Token và context đều là các đơn vị đo lường số lượng chữ trong văn bản.
- **C.** Context là số lượng từ mà model có thể xử lý trong một lần, còn token là tổng số từ trong văn bản.
- **D.** Token chỉ là một phần của context, không có vai trò trong việc xử lý văn bản.

**Đáp án AI đánh dấu:** A
**Giải thích của AI:** Phát biểu đúng là token là đơn vị mà model sử dụng để đọc và xử lý văn bản, trong khi context là lượng chữ mà model có thể xem cùng một lúc, cho thấy sự khác biệt rõ ràng giữa hai khái niệm này.

| Chiều | Y / N | Lý do (nếu N) |
|---|---|---|
| Answer key đúng | Y | |
| Đúng khái niệm | Y | |
| Đúng mức khó | Y | *Lưu ý nhỏ (không phải 1 trong 3 chiều):* định nghĩa token nằm ở trang 13, không phải trang 14 như cột "page" ghi — người chấm chỉ mở đúng trang 14 sẽ thiếu căn cứ để xác nhận vế token. |
---

**Người chấm dừng ở đây. Phần dưới dành cho Duy so sánh sau khi người chấm đã nộp phiếu.**

<details>
<summary>Dành cho Duy — điểm của nhóm và bảng so sánh (bấm để mở)</summary>

| Câu | Case (lượt) | Nhóm: answer key | Nhóm: khái niệm | Nhóm: mức | Người duyệt | Vì sao chọn |
|---|---|---|---|---|---|---|
| 1 | G06 (run-5) | Y | Y | Y | Duy | Y rõ |
| 2 | G05 (run-5) | N | Y | Y | Duy | N — sai đáp án |
| 3 | L4-01 (run-5) | Y | Y | Y | Duy | phân vân — mức 2 sát ranh giới nhận biết |
| 4 | T-G53 (run-3-muc2) | Y | Y | N | Duy | N — mức 2 dạng "gọi tên" |
| 5 | T-G50 (run-5) | Y | Y | Y | Duy | Y rõ |

**Cách so sánh:** mỗi câu 3 ô → tổng 15 ô. Đếm số ô người ngoài chấm **khác** nhóm theo từng chiều.

| Chiều | Số câu lệch / 5 | Kết luận theo rubric |
|---|---|---|
| Answer key đúng | 0 | lệch 0–1: định nghĩa đủ rõ · lệch ≥ 2: viết lại định nghĩa |
| Đúng khái niệm | 1 (câu 3) | lệch 0–1: định nghĩa đủ rõ |
| Đúng mức khó | 1 (câu 3) | lệch 0–1: định nghĩa đủ rõ |
| **Tổng ô khớp** | 13 / 15 = 86.7 % | cả 3 chiều đủ rõ; lệch duy nhất ở câu 3 nhiều khả năng do sai trang/khái niệm khi tạo câu hỏi (nội dung thực chất là `ai_types` trang 4, bị gắn nhãn `ai_layers` trang 3), không phải do định nghĩa rubric mơ hồ |

Ghi kết quả vào **cuối `eval/run-5.md`** (rubric yêu cầu), vào `spec.md` §7 (dòng "Chưa làm") và §9, và đưa **% khớp** lên slide 5. Nếu lệch ≥ 2/5 ở chiều nào: viết lại định nghĩa chiều đó trong rubric và ghi lý do.

</details>
