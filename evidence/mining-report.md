# Báo cáo mining - 18/09/2026

Nguồn: eval/chatlog/tutor_turns.csv (data pack ẩn danh, không đưa file gốc vào Git).
Script: [mining.py](../mining.py). Từ điển dữ liệu: eval/chatlog/DATA_DICTIONARY.md.
Khoảng dữ liệu theo từ điển: 22/07-15/09/2026; file gộp hai kỳ và hai khóa K3/K4.

## Tái lập

Chạy từ thư mục gốc dự án:

```powershell
python mining.py --csv eval/chatlog/tutor_turns.csv
```

Cần Python và pandas. Kết quả dưới đây là output thực tế, exit code 0. Chỉ lưu thống kê, không lưu nguyên log hội thoại.

## Giới hạn diễn giải

- K4 gồm nhiều course_id; 448 là số học viên K4 có tương tác trong file, không phải số đã xác nhận pain hoặc riêng khóa K4P1.
- 114 người có một lượt hỏi chỉ là số quan sát trong cửa sổ dữ liệu; không chứng minh bỏ học, rời bỏ sản phẩm hoặc không hài lòng.
- Tiêu đề script "Khong co hoat dong nao cho hoc vien LAM" là diễn giải quá mạnh: danh sách cột chỉ cho thấy chưa có trường riêng ghi bài làm trong file này, không chứng minh toàn sản phẩm không có luyện tập.
- Các nhãn hoạt động ít xuất hiện không chứng minh cơ chế tương ứng không tồn tại ở nơi khác. understanding_level gần rỗng phản ánh dữ liệu được ghi.
- Rating chỉ có ở 12 lượt K4; không suy ra mức hài lòng chung. has_citation không kiểm chứng nguồn đúng nghĩa.
- Hai kỳ history/live đo reply_ms khác nhau; không so latency tuyệt đối như cùng phép đo. Ngày 30/07 có hoạt động lớp bất thường, không dùng trung bình toàn file làm tần suất đại diện.
- Bộ lọc ứng viên trong extract_cases.py mặc định chỉ K4P1, khác với nhóm K4 tổng hợp ở đây.
- Chưa có survey-log.md để đối chiếu pain; không thay khảo sát người dùng bằng các chỉ số này.

## Output nguyên văn

```text
Toan file: 13494 luot | K4: 3097 luot, 448 hoc vien

== 4 co che da thiet ke san nhung bo trong ==
understanding_level co du lieu : 20/13494 (0.15%)
suggest_next_topic    : 18/13494 (0.13%)
motivate              : 21/13494 (0.16%)
celebrate_progress    : 7/13494 (0.05%)

== Tutor gan nhu chi lam mot viec: giang ==
review_concept        : toan file 12127/13494 (89.9%) | K4 2767/3097 (89.34%)
ask_probing_question  : toan file 28/13494 (0.2%) | K4 6/3097 (0.19%)
give_hint             : toan file 39/13494 (0.3%) | K4 23/3097 (0.74%)
validate_understanding: toan file 22/13494 (0.2%) | K4 11/3097 (0.36%)

== Khong co hoat dong nao cho hoc vien LAM ==
19 cot: ['turn_id', 'period', 'cohort_hint', 'asked_at_vn', 'student', 'lecture_code', 'lecture_title', 'course_id', 'is_preset', 'q_len', 'student_question', 'tutor_reply', 'reply_len', 'move_used', 'understanding_level', 'has_citation', 'grade_missing', 'rating', 'reply_ms']

== Proxy roi bo ==
Hoc vien K4 chi hoi 1 lan: 114/448 (25.4%)

== Boi canh cho bang impact ==
K4 co rating          : 12/3097 (0.39%)
K4 khong trich dan    : 839/3097 (27.1%)
K4 la cau mau (preset): 542/3097 (17.5%)
```
