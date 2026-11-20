# Kết quả 5-fold trên train (seed chia fold=42)

Dùng cho tiếng Việt thay cho dev (dev VTB lệch phân phối so với train/test, xem docs/notes/GHI_CHU.md mục 2). Metric là trung bình các fold (± độ lệch chuẩn giữa các fold); OOV tính theo phần học của từng fold; Fit/Predict là thời gian trung bình mỗi fold.

| Ngôn ngữ | Mô hình | Token acc | OOV acc | Macro-F1 | Sent acc | Fit (s) | Predict (s) | Tham số |
|---|---|---|---|---|---|---|---|---|
| vi | baseline | 86.07% ± 0.69% | 37.96% | 0.773 | 16.50% | 0.01 | 0.00 | {} |
| vi | baseline-sig | 86.15% ± 0.74% | 38.69% | 0.776 | 17.71% | 0.01 | 0.00 | {"oov": "signature"} |
| vi | hmm | 85.15% ± 0.85% | 48.61% | 0.757 | 15.36% | 0.01 | 0.02 | {"alpha": 0.01, "unk": "signature"} |
| vi | hmm-addalpha | 83.62% ± 0.72% | 13.25% | 0.686 | 13.43% | 0.01 | 0.02 | {"alpha": 0.01, "unk": "add-alpha"} |
| vi | hmm-rare | 84.31% ± 0.82% | 43.83% | 0.752 | 14.71% | 0.02 | 0.02 | {"alpha": 0.01, "unk": "rare"} |
| vi | hmm-sig | 85.15% ± 0.85% | 48.61% | 0.757 | 15.36% | 0.02 | 0.02 | {"alpha": 0.01, "unk": "signature"} |
| vi | crf | 90.45% ± 0.61% | 67.28% | 0.814 | 30.00% | 2.54 | 0.07 | {"c1": 0.0, "c2": 0.1} |
| vi | maxent | 90.37% ± 0.63% | 66.14% | 0.803 | 29.00% | 5.72 | 0.15 | {} |
| vi | memm | 90.60% ± 0.68% | 67.65% | 0.810 | 30.86% | 7.06 | 1.62 | {} |
