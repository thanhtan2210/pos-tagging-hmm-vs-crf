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

**Đã chốt: phương án (b).** Các phương án đã cân nhắc:
- (a) Lọc dev chỉ giữ câu ≤ 25 từ để khớp với test: loại 1/3 dev, mất luôn dữ liệu để phân tích câu dài.
- (b) Dùng k-fold trên train để chọn tham số và so sánh mô hình; giữ dev đầy đủ làm thí nghiệm phụ theo độ dài câu.
- (c) Giữ nguyên dev và ghi nhận là hạn chế: kết luận tiếng Việt sẽ dựa trên phân phối khác test.

Cách làm cụ thể:
- Chọn tham số: 3-fold trên train (`scripts/tune.py`) cho cả hai ngôn ngữ.
- So sánh mô hình tiếng Việt: 5-fold trên train (`run_experiments.py --split cv`, `analyze.py --split cv`; ablation và learning curve tiếng Việt cũng chạy 5-fold). Tiếng Anh vẫn dùng dev vì dev EWT không lệch.
- Dev VTB đầy đủ: chỉ dùng cho bảng accuracy theo độ dài câu (`analysis_vi_dev.md`).
- Test: đánh giá một lần, đối chiếu cả ba cách.

Kết quả đối chiếu (CRF tiếng Việt): dev 85,62%, 5-fold 90,45%, test 88,34%.
- Dev bi quan vì 1/3 câu dài hơn mọi câu train; 5-fold lạc quan vì câu của cùng một bài báo có thể nằm ở cả phần học lẫn phần chấm (VTB không có mã văn bản nên không chia fold theo văn bản được); test nằm giữa.
- Mọi kết luận so sánh giữ nguyên qua cả ba cách, trừ HMM − baseline: dev −0,34 (không ý nghĩa), 5-fold −0,92, test +1,22. Chỉ kết luận "ngang ngửa".

## 3. Mức độ mơ hồ: đo thế nào cho đúng

Nếu đếm "token có từ mang > 1 nhãn trong train", tiếng Anh ra 56%. Con số này bị **nhiễu nhãn** thổi phồng: ví dụ `the` là DET 8.141 lần nhưng có 7 lần bị gán PRON, và chỉ vài lần nhầm như vậy đã biến mọi token `the` thành "mơ hồ".

Chỉ số chắc hơn là **tỷ lệ token không mang nhãn đa số của từ đó**: vi 5,7%, en 7,1%. Đây là mức lỗi tối thiểu nếu chỉ tra từ điển mà không nhìn ngữ cảnh (đo ngay trên train). Phần còn lại phải nhờ ngữ cảnh mới giải quyết được.

## 4. Đặc điểm ngôn ngữ học: dùng cho thảo luận RQ3

- **Tiếng Việt:** các từ mơ hồ nhất (`được`, `đến`, `về`, `cho`, `vào`, `ở`, `để`) đều vừa là động từ vừa là giới từ/phó từ. Đây là hiện tượng ngữ pháp hóa (thực từ chuyển thành hư từ) điển hình của ngôn ngữ đơn lập. Hình thái từ không phân biệt được các trường hợp này, chỉ ngữ cảnh mới phân biệt được, nên dự đoán đặc trưng hậu tố/tiền tố gần như vô ích với tiếng Việt.
- **Tiếng Việt:** 22,4% token là từ nhiều âm tiết (`chủ tịch`, `Bùi Văn Luyến`). Dữ liệu UD đã tách từ sẵn, nên kết quả **phụ thuộc vào việc tách từ đúng**. Đây là một hạn chế cần nêu.
- **Tiếng Anh:** mơ hồ tập trung ở từ chức năng (`to` PART/ADP, `that` SCONJ/PRON/DET, `have` VERB/AUX). Ngược lại, từ OOV tiếng Anh thường đoán được nhờ hình thái (`-ing`, `-ed`, `-ly`, viết hoa).

## TODO (mục 7): Hạn chế — ghi dần trong lúc làm, cuối cùng chép sang báo cáo

- [ ] dữ liệu tiếng Việt nhỏ (1.400 câu train)
- [ ] dùng tách từ có sẵn (gold), chưa đo ảnh hưởng của tách từ tự động
- [ ] dev VTB lệch độ dài câu so với train/test
- [ ] chỉ so sánh các mô hình cổ điển, không có mô hình học sâu
