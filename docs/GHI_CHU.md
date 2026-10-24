# Ghi chú phát hiện trong quá trình làm

Số liệu lấy từ `python scripts/eda.py` (bản UD tải ngày 24/10/2026, nhánh `master`).

## 1. Tiếng Việt có rất ít dữ liệu huấn luyện

| | VTB (vi) | EWT (en) |
|---|---|---|
| Câu train | 1.400 | 12.544 |
| Token train | 20.215 | 204.578 |
| Token OOV trên dev | **18,5%** | 8,3% |
| Từ chỉ xuất hiện 1 lần / tổng số từ khác nhau | 53,8% | 49,8% |

Ý nghĩa:
- Tập train tiếng Việt nhỏ hơn tiếng Anh khoảng 10 lần. Theo Ng & Jordan (2002), đây đúng là vùng mà mô hình sinh (HMM) có thể cạnh tranh được với mô hình phân biệt. Có thể kiểm chứng trực tiếp ở RQ1.
- Gần 1/5 token trên dev là từ chưa gặp, nên cách xử lý OOV (RQ2) ảnh hưởng lớn đến kết quả tiếng Việt.

## 2. Tập dev của VTB lệch phân phối so với train và test

| Tập | Số câu | Độ dài TB | Max | Câu > 25 từ |
|---|---|---|---|---|
| train | 1.400 | 14,4 | 25 | 0% |
| dev | 1.123 | 23,3 | 96 | **33%** |
| test | 800 | 14,6 | 25 | 0% |

Train và test chỉ gồm câu tối đa 25 từ, còn dev có nhiều câu dài hơn hẳn. Nếu chọn tham số theo dev, ta đang tối ưu cho một phân phối khác với phân phối của test.

**Cần quyết định** cách chọn mô hình cho tiếng Việt:
- (a) Lọc dev chỉ giữ câu ≤ 25 từ để khớp với test.
- (b) Dùng k-fold cross-validation trên train để chọn tham số; giữ nguyên dev đầy đủ làm thí nghiệm phụ "độ bền theo độ dài câu".
- (c) Giữ nguyên dev và ghi nhận đây là hạn chế.

Phương án (b) chặt chẽ nhất và tạo thêm một nội dung thảo luận (accuracy theo độ dài câu). Đây là câu hỏi tốt để hỏi thầy trong buổi trình bày.

## 3. Mức độ mơ hồ: đo thế nào cho đúng

Nếu đếm "token có từ mang > 1 nhãn trong train", tiếng Anh ra 56%. Con số này bị **nhiễu nhãn** thổi phồng: ví dụ `the` là DET 8.141 lần nhưng có 7 lần bị gán PRON, và chỉ vài lần nhầm như vậy đã biến mọi token `the` thành "mơ hồ".

Chỉ số chắc hơn là **tỷ lệ token không mang nhãn đa số của từ đó**: vi 5,7%, en 7,1%. Đây là mức lỗi tối thiểu nếu chỉ tra từ điển mà không nhìn ngữ cảnh (đo ngay trên train). Phần còn lại phải nhờ ngữ cảnh mới giải quyết được.

## 4. Đặc điểm ngôn ngữ học: dùng cho thảo luận RQ3

- **Tiếng Việt:** các từ mơ hồ nhất (`được`, `đến`, `về`, `cho`, `vào`, `ở`, `để`) đều vừa là động từ vừa là giới từ/phó từ. Đây là hiện tượng ngữ pháp hóa (thực từ chuyển thành hư từ) điển hình của ngôn ngữ đơn lập. Hình thái từ không phân biệt được các trường hợp này, chỉ ngữ cảnh mới phân biệt được, nên dự đoán đặc trưng hậu tố/tiền tố gần như vô ích với tiếng Việt.
- **Tiếng Việt:** 22,4% token là từ nhiều âm tiết (`chủ tịch`, `Bùi Văn Luyến`). Dữ liệu UD đã tách từ sẵn, nên kết quả **phụ thuộc vào việc tách từ đúng**. Đây là một hạn chế cần nêu.
- **Tiếng Anh:** mơ hồ tập trung ở từ chức năng (`to` PART/ADP, `that` SCONJ/PRON/DET, `have` VERB/AUX). Ngược lại, từ OOV tiếng Anh thường đoán được nhờ hình thái (`-ing`, `-ed`, `-ly`, viết hoa).
