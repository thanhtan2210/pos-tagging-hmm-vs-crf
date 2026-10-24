# Kế hoạch 2 tuần: trình bày sơ bộ cho thầy (~07/11/2026)

Mục tiêu buổi trình bày: thầy duyệt đề tài và hướng làm. Cần có bài toán, dữ liệu kèm thách thức (số liệu thật), các câu hỏi nghiên cứu, phương pháp, **kết quả sơ bộ** (baseline, HMM, CRF lần đầu) và kế hoạch phần còn lại.

## Tuần 1 (24/10 – 31/10): dữ liệu, baseline, HMM

| Ngày | Việc | Ai làm |
|---|---|---|
| 24–25/10 | Cài môi trường, tải dữ liệu, chạy test đọc dữ liệu, EDA, baseline | Claude dựng, bạn chạy và đọc `results/eda.md` |
| 26–28/10 | Ôn slide HMM (Ch.5), cài `HMMTagger.fit` (TODO 1–2) và `viterbi` (TODO 3) cho đến khi `python -m pytest` qua hết | **Bạn** (Claude gợi ý / review khi bí) |
| 29–31/10 | Chạy HMM trên vi/en; thử các giá trị `alpha`; ghi nhận xét đầu tiên về OOV (RQ2) | Bạn chạy, cùng phân tích |

## Tuần 2 (01/11 – 07/11): CRF, learning curve, slide

| Ngày | Việc | Ai làm |
|---|---|---|
| 01–03/11 | CRF với `sklearn-crfsuite`: Claude dựng khung, **bạn chọn và viết hàm đặc trưng**; chạy lần đầu trên dev | Cả hai |
| 04/11 | Learning curve sơ bộ HMM vs CRF (RQ1), vẽ biểu đồ | Cả hai |
| 05–06/11 | Làm slide (~10 trang) và tập trình bày | Bạn viết nội dung, Claude góp ý |
| 07/11 | Trình bày | Bạn |

## Dàn ý slide trình bày sơ bộ

1. Bài toán POS tagging: input/output, ví dụ một câu tiếng Việt
2. Vì sao cần học máy: từ mơ hồ (số liệu từ EDA), từ mới
3. Dữ liệu: hai treebank, bảng thống kê, thách thức chính
4. Câu hỏi nghiên cứu RQ1–RQ4
5. Phương pháp: HMM (sinh) vs MaxEnt/CRF (phân biệt): công thức, khác biệt cốt lõi
6. Thiết lập thực nghiệm: chia dữ liệu, metric và lý do chọn
7. Kết quả sơ bộ: bảng baseline / HMM / CRF
8. Nhận xét ban đầu (OOV, thời gian huấn luyện)
9. Kế hoạch phần còn lại: RQ3, RQ4, GA chọn đặc trưng
10. Câu hỏi cho thầy (vd. phạm vi đề tài, có cần thêm ngôn ngữ/dataset không)

## Sau buổi trình bày (phần còn lại)

- RQ3: ablation đặc trưng trên hai ngôn ngữ
- RQ4: MaxEnt từng từ vs MEMM vs CRF
- Nâng cao: GA chọn tổ hợp nhóm đặc trưng (Ch.4 Genetic Algorithms)
- Đánh giá cuối trên test (một lần), báo cáo, slide cuối, đóng gói nộp bài
