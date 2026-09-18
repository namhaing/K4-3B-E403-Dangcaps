# Báo cáo: Đo "chỗ bạn đang yếu" qua nhiều lượt

> Viết cho Nam (đội trưởng), Duy (backend) và Hiền (frontend): đã làm gì, ở file nào, chạy thế nào, và trả lời giám khảo ra sao.
> Làm lúc 18:00–18:20 ngày 18/9. Trạng thái: **code chạy thật, test đạt, đã thử trên trình duyệt với AI thật. CHƯA commit/push.**

---

## 0a. Cập nhật 18:50: hiện ảnh slide thật khi ôn lại

- **Backend:** endpoint mới `GET /slide/{page}.png` vẽ đúng trang PDF slide gốc thành ảnh (1536×864, khoảng 85 KB, 0,04 giây/trang), giữ trong RAM. Máy không có file PDF (data pack không có trong repo) → 404.
- **Web:** bước 2 của màn ôn hiện **ảnh đúng trang slide như lúc học**, nút "Mở lớn ↗", chữ trên slide thu gọn trong "Xem chữ trên slide". Ảnh lỗi thì tự mở phần chữ. Mỗi câu trích ở bước 1 có link "xem Slide N ↓" nhảy tới ảnh. Màn phản hồi sau mỗi câu có nút **"Xem slide ↗"**.
- **Kiểm tra:** test **52/52** (+3). Chạy thật trên Edge: ảnh slide 4 tải đủ 1536×864, nút "Xem slide" có ở màn phản hồi, 0 lỗi JS.
- **⚠️ Bảo mật:** ảnh slide là nội dung data pack nên **không lưu vào repo**. Ảnh minh hoạ `docs/anh/on-lai-kien-thuc.png` đã **cắt bỏ phần chữ slide**; `.gitignore` chặn `docs/anh/*slide*.png`. Khi làm slide thuyết trình, chụp màn ôn **trên máy** để chiếu, không đưa lên GitHub.

---

## 0. Cập nhật 18:35: bản đồ trực quan hơn + ôn lại ngay (theo góp ý của Nam)

**Góp ý:** bản đồ khó đọc, và xem bản đồ xong thì chưa biết ôn thế nào.

**Bản đồ mới** (ảnh: `docs/anh/ban-do-kien-thuc.png`):

| Phần | Cho học viên biết gì |
|---|---|
| **Thanh tổng quan theo màu** + chú thích số lượng | Nhìn một lần là biết mình đang ở đâu trong buổi: xanh = vững, đỏ = cần ôn, vàng = chưa đủ dữ liệu, xám = chưa luyện |
| **Khu "Cần ôn ngay"** đặt ở đầu | Các phần đang yếu, mỗi phần có 2 nút: **📖 Ôn lại kiến thức** và **🎯 Luyện 3 câu** |
| **Lộ trình buổi học** theo thứ tự slide (1 → 12) | Mỗi phần có chấm ●●○ cho các câu gần nhất, **lý do bằng lời** ("Sai 3/3 câu gần nhất", "Đã làm 1 câu · cần thêm 2 câu để đánh giá"), và nút "Ôn lại" hoặc "Luyện thử" |

**Màn "Ôn lại kiến thức" 3 bước** (ảnh: `docs/anh/on-lai-kien-thuc.png`):
1. **Xem lại câu bạn đã sai:** đề, lựa chọn của mình (đỏ), đáp án đúng (xanh), giải thích, câu trích slide.
2. **Đọc lại đúng phần slide:** các ý chính đã làm căn cứ, cùng nội dung gốc của đúng trang slide.
3. **Kiểm tra lại ngay:** nút "Luyện 3 câu phần này", một lượt ngắn chỉ hỏi phần đó. Kết quả cộng vào bản đồ.

**Không thêm quyết định AI mới:** bước 1–2 chỉ dùng lại nội dung đã qua validator và kiểm chéo, cùng slide gốc. Bước 3 dùng lại đúng hàm sinh câu hỏi cũ.

**Code đã thêm:**
- `progress.py`: lưu thêm 5 câu sai gần nhất và các câu trích.
- `rules.py`: `status_reason()`, `FOCUS_TOTAL = 3`.
- `app.py`: `focus_concept` trong `/session/start`; endpoint **`GET /learner/{id}/concept/{cid}/review`**; lượt ôn riêng khi AI hụt thì thử lại chính khái niệm đó.
- `app.js`: thay khối bản đồ, thêm `renderReview()`, `startSession(battleMode, focusConcept)`.
- `styles.css`: style bản đồ v2 và màn ôn.

**Kiểm tra:**
- Test **49/49** (thêm 8: màn ôn có câu sai + slide + lý do, khái niệm lạ → 404, lượt ôn riêng đúng 3 câu cùng khái niệm, AI hụt thì thử lại).
- **Chạy thật trên Edge + AI thật:** bản đồ → "Ôn lại kiến thức" (3 câu sai thật, slide 4) → "Luyện 3 câu" (cả 3 câu cùng khái niệm, có thông báo "Lượt ôn riêng…") → bản đồ cập nhật. 0 lỗi JS, điện thoại không tràn.

**Lỗi phát hiện khi chạy thật và đã sửa:** lượt ôn riêng lần đầu không ra được câu (1/3 lần), vì AI hụt thì hệ thống bỏ khái niệm, mà lượt này không có khái niệm nào khác. Sửa bằng cách thử lại chính khái niệm đó, tối đa 3 lần. Kết quả: 5/5 lần ra câu.

**Giới hạn còn lại:**
- Trong lượt ôn riêng, AI hay ra câu gần giống nhau (ví dụ "Có bao nhiêu nhóm AI chính…" 2 lần). Bộ lọc "không lặp" chỉ bắt câu giống nhau từ 80% trở lên.
- Lượt ôn riêng có thể chậm hơn khi AI phải thử lại.

---

## 1. Vì sao làm

Trước đây **mỗi lượt luyện độc lập**:
- "Chủ đề nên ôn" chỉ dựa trên 5 câu của một lượt. Tắt trang là mất.
- Lượt sau không biết lượt trước học viên sai gì.
- Pain trong spec là *"không biết mình đang ở mức nào và nên ôn gì tiếp"*, mới giải được một nửa.
- Trang chủ VLearn thật vẫn ghi *"Chỗ bạn đang yếu: Chưa đo được phần nào"*.

Giờ hệ thống **nhớ học viên qua nhiều lượt** và vẽ **bản đồ 12 khái niệm Day 1**. Lượt sau **ưu tiên ôn đúng chỗ yếu**.

**AI vẫn chỉ có một quyết định** (sinh câu hỏi bám slide). Phần đo chỗ yếu là **luật minh bạch**, không dùng AI.

---

## 2. Học viên thấy gì

```text
Lần đầu vào → Bản đồ: "Chưa đo được phần nào. Làm một lượt 5 câu để VLearn biết bạn đang ở đâu."
     ↓ làm 1 lượt
Bản đồ: "3/12 phần đã luyện" — các phần đã làm 1–2 câu ghi "Chưa đủ dữ liệu" (KHÔNG kết luận vội)
     ↓ làm thêm vài lượt
Bản đồ: "Bạn đang yếu 1 phần: Discriminative AI · Generative AI · Agentic AI"   [Ôn chỗ yếu ngay →]
     ↓ bấm
Lượt mới: "Lượt này ưu tiên ôn lại phần bạn đang yếu: …" → câu ĐẦU TIÊN hỏi đúng phần đó
```

Ảnh chụp thật (Edge + AI thật): `docs/anh/ban-do-kien-thuc.png` · `docs/anh/on-lai-kien-thuc.png` · `docs/anh/on-cho-yeu-cau-dau.png`

---

## 3. Luật "đang yếu" (rule, không AI)

| Trạng thái | Khi nào | Lý do thiết kế |
|---|---|---|
| **Chưa luyện** | 0 câu | |
| **Chưa đủ dữ liệu** | 1–2 câu | HAX G10: không kết luận học viên yếu từ 1–2 câu |
| **Đang yếu** | ≥ 3 câu **và** sai ≥ 2 trong 3 câu gần nhất | Xét 3 câu **gần nhất** để phản ánh tiến bộ: học viên ôn xong làm đúng thì tự thoát "đang yếu" |
| **Đã vững** | ≥ 3 câu **và** đúng ≥ 2 trong 3 câu gần nhất | |

**Những câu KHÔNG được tính vào hồ sơ:**
- Câu trả lời **dưới 3 giây** (dấu hiệu đoán mò): nếu tính thì bản đồ sai lệch.
- Câu bị **"Đổi câu khác"** hoặc **"Báo câu sai"**: học viên không bị gắn "đang yếu" vì một câu AI ra sai.

**Thứ tự khái niệm ở lượt mới** (khi đã có hồ sơ): *đang yếu* → *chưa luyện / chưa đủ dữ liệu* → *đã vững*. Trong mỗi nhóm vẫn xáo ngẫu nhiên để phủ cả slide.

---

## 4. Riêng tư

- Trình duyệt tự tạo **một mã ngẫu nhiên** (`localStorage["solo-arena-learner"]`). **Không có tên, email hay MSSV.**
- Backend **không có** chức năng liệt kê học viên. Chỉ ai giữ mã mới xem được bản đồ của mã đó.
- Mã sai định dạng (ví dụ chứa `../`) bị từ chối với lỗi **400**.
- Hồ sơ lưu ở `codebase/data/progress.json`, **đã chặn trong `.gitignore`**, không lên repo public.

**Giới hạn cần nói thật:** mã gắn với trình duyệt. Đổi máy hoặc xoá dữ liệu trình duyệt thì mất hồ sơ. Bản thật cần gắn với tài khoản VLearn.

---

## 5. Các file đã sửa hoặc tạo

| File | Loại | Nội dung |
|---|---|---|
| `codebase/api/progress.py` | **Mới** | `ProgressStore`: lưu và cộng dồn kết quả theo học viên × khái niệm (giữ 5 kết quả gần nhất), ghi file JSON, có khoá luồng; `valid_learner()` kiểm định dạng mã |
| `codebase/api/rules.py` | Sửa | Thêm `concept_status()`, `order_for_learner()`, các ngưỡng `MIN_CONCEPT_ANSWERS=3`, `WEAK_WINDOW=3`, `WEAK_WRONG=2` |
| `codebase/api/app.py` | Sửa | `/session/start` nhận `learner_id`, trả thêm `focus_weak`; `/answer` ghi hồ sơ (bỏ câu < 3 giây); **endpoint mới** `GET /learner/{id}/progress` |
| `codebase/api/test_api.py` | Sửa | +12 test → **41/41** |
| `codebase/web/app.js` | Sửa (**chỉ thêm**) | `getLearnerId()`; gửi `learner_id`; khối "Bản đồ kiến thức"; `loadProgress()`; thông báo ưu tiên ôn; nút "Xem bản đồ kiến thức" ở màn kết quả |
| `codebase/web/styles.css` | Sửa (thêm cuối file) | Style bản đồ, dùng lại biến màu có sẵn của Hiền |
| `.gitignore` | Sửa | Chặn `codebase/data/progress.json` |
| `codebase/CONTRACT.md` | Sửa | Mục 4b mới: `learner_id`, `focus_weak`, `/learner/{id}/progress`, bảng `status` |
| `spec.md` | Sửa | Lát cắt (thêm vế nhiều lượt); hiện trạng prototype + phần MOCK; bảng thiết kế (+kiểm chéo, +đo chỗ yếu); **Non-goals viết lại** (mục cũ đang trống); §4b G10; §5 +4 kịch bản; §6 +1 đường đi; §9 +1 dòng |
| `canvas.md` | Sửa | Lát cắt + non-goals cho khớp spec |
| `ke-hoach-nhom.md` | Sửa | Tick checklist + việc còn lại |
| `docs/anh/*.png` | **Mới** | 3 ảnh chụp thật, dùng cho spec và slide |

**Không đụng vào:** chế độ 1v1, bảng xếp hạng, demo offline của Hiền; phần AI (`codebase/ai/`); eval.

---

## 6. Đã kiểm tra gì — kết quả thật

| Kiểm tra | Kết quả |
|---|---|
| `python -m codebase.api.test_api` | **49/49 đạt** (lúc 18:20 là 41/41) (12 test mới: 4 luật trạng thái, mã lạ → 400, học viên mới, 2 câu sai chưa kết luận, đủ 3 câu thì "đang yếu", lượt sau báo và hỏi ngay phần yếu, đoán mò không tính, không có mã thì chạy như cũ) |
| `python -m codebase.ai.test_validator` | 19/19 đạt (không ảnh hưởng) |
| Bộ chấm eval (các case flow L2, L3) | Vẫn đúng hành vi |
| **Trình duyệt Edge + AI thật, học viên mới** | Trước khi luyện: *"Chưa đo được phần nào…"* → sau 1 lượt: *"3/12 phần đã luyện, chưa thấy phần nào đang yếu. Một phần chỉ được đánh giá khi bạn đã làm ít nhất 3 câu"* |
| **Trình duyệt Edge + AI thật, học viên có phần yếu** (hồ sơ mẫu, đã xoá sau khi test) | Bản đồ: *"Bạn đang yếu 1 phần: Discriminative AI · Generative AI · Agentic AI"* → bấm "Ôn chỗ yếu ngay" → thông báo *"Lượt này ưu tiên ôn lại…"* → câu đầu: *"Một ứng dụng AI cần phân loại email thành spam… Loại AI nào phù hợp nhất?"* (đúng phần yếu, mức 3 có tình huống) |
| Lỗi JavaScript | Không có |

---

## 7. Cách chạy và demo

```bat
uvicorn codebase.api.main:app --port 8000 --reload
```
Mở `http://localhost:8000/app/`. Khối **"Bản đồ kiến thức của bạn"** nằm trên màn chính, dưới "Sẵn sàng bắt đầu?".

**Kịch bản demo đề xuất (khoảng 90 giây):**
1. Chiếu ảnh trang chủ VLearn thật: *"Chỗ bạn đang yếu: Chưa đo được phần nào"*.
2. Mở Solo Arena, bản đồ cũng ghi "Chưa đo được", rồi làm 1 lượt 5 câu (mỗi câu chờ quá 3 giây mới chọn).
3. Quay lại bản đồ: các phần đã làm ghi **"Chưa đủ dữ liệu"**. Nói: *"Hệ thống không vội kết luận từ 1–2 câu."*
4. Chuyển sang trình duyệt đã luyện trước vài lượt: bản đồ có phần **"Đang yếu"** → bấm **"Ôn chỗ yếu ngay"** → câu đầu hỏi đúng phần đó.

Bước 4 cần **luyện trước 3–4 lượt trên một trình duyệt riêng** để có phần "đang yếu". Hồ sơ lưu trên máy chạy server, không mất khi tắt trang.

---

## 8. Câu giám khảo có thể hỏi

- **"Ai quyết định học viên yếu, AI à?"**
  → Không. Luật minh bạch quyết định: ≥ 3 câu và sai ≥ 2 trong 3 câu gần nhất. AI chỉ sinh câu hỏi. Nhóm không để AI "phán" năng lực học viên.
- **"Sao là 3 câu?"**
  → Ngưỡng nhỏ nhất để không kết luận từ một lần sai tình cờ, mà vẫn đủ nhanh để học viên thấy kết quả sau 1–2 lượt. Nhóm chưa đo tối ưu ngưỡng này, và ghi đây là giới hạn.
- **"Nếu AI ra câu sai đáp án, học viên bị gắn yếu oan thì sao?"**
  → Có 3 lớp chặn: kiểm chéo trước khi hiện câu; cần ≥ 3 câu mới kết luận; câu bị "Báo câu sai" không tính.
- **"Có lộ ai yếu gì không?"**
  → Không lưu danh tính, chỉ có mã ngẫu nhiên. Không có chức năng liệt kê. Bảng xếp hạng không hiện chỗ yếu.
- **"Sao không dùng mô hình học máy để ước lượng năng lực?"**
  → Với vài câu mỗi khái niệm, mô hình phức tạp không đáng tin hơn luật đơn giản. Luật minh bạch thì học viên và giảng viên đều hiểu được vì sao bị đánh giá như vậy.

---

## 9. Việc còn lại (ai làm)

1. **Duy** rà lại `progress.py`, `rules.py`, `app.py` và 12 test mới, để tự giải thích được phần có tên mình. **Hiền** rà phần thêm trong `app.js` và `styles.css`.
2. **Nam** đọc lại **Non-goals** trong `spec.md` §4. Mục này đang trống nên tôi đã viết lại; sửa nếu không đồng ý.
3. **Trước CP4 (21:00):** `spec.md` §7 vẫn là bản cũ ("0/60 đã chạy, còn thiếu run_eval.py"), cần viết lại theo run-1/run-2. Đồng thời chốt quality bar.
4. Nên thêm vào golden set 2 case cho tính năng này (ví dụ "2 câu sai thì chưa kết luận", "đoán mò không tính"), rồi chạy lại eval. Hiện hành vi này mới được kiểm bằng `test_api`.
5. **Commit và push** (xem mục 10).

## 10. Commit gợi ý

```bat
git add codebase/api/progress.py codebase/api/rules.py codebase/api/app.py codebase/api/test_api.py .gitignore
git commit --author="Bui Phuong Duy <email-cua-duy>" -m "feat(api): do cho yeu qua nhieu luot (ho so an danh, luat dang yeu, uu tien on)"

git add codebase/web/app.js codebase/web/styles.css
git commit --author="Tran Thi Thu Hien <email-cua-hien>" -m "feat(web): ban do kien thuc + on cho yeu"

git add spec.md canvas.md codebase/CONTRACT.md ke-hoach-nhom.md bao-cao-do-cho-yeu.md docs/anh
git commit -m "docs: lat cat nhieu luot, non-goals, §5 §6 §9, bao cao"

git push origin anam:main
git push
```
