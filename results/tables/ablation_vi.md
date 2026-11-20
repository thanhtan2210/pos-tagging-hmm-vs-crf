# Ablation đặc trưng CRF (vi), đánh giá bằng 5-fold trên train (TB ± độ lệch chuẩn giữa các fold)

Dev VTB lệch phân phối so với train/test nên tiếng Việt dùng k-fold trên train (docs/notes/GHI_CHU.md mục 2). Δ là hiệu trung bình so với bộ đầy đủ trên cùng fold; cột cuối đếm số fold mà cấu hình thấp hơn bộ đầy đủ. OOV tính theo phần học của từng fold.

| Kiểu | Bộ đặc trưng | Token acc | Δ so với đầy đủ | OOV acc | Số fold thấp hơn đầy đủ |
|---|---|---|---|---|---|
| leave-one-out | đầy đủ | 90.45% ± 0.61% | +0.00% | 67.28% | - |
| leave-one-out | - word | 90.28% ± 0.63% | -0.17% | 67.08% | 5/5 |
| leave-one-out | - affix | 89.93% ± 0.78% | -0.52% | 66.90% | 5/5 |
| leave-one-out | - shape | 90.03% ± 0.78% | -0.43% | 64.02% | 5/5 |
| leave-one-out | - context1 | 89.85% ± 0.78% | -0.61% | 64.14% | 5/5 |
| leave-one-out | - context2 | 90.63% ± 0.39% | +0.18% | 67.23% | 1/5 |
| leave-one-out | - syllable | 90.17% ± 0.65% | -0.28% | 66.66% | 5/5 |
| cumulative | word | 87.94% ± 0.54% | -2.52% | 49.56% | 5/5 |
| cumulative | word + affix | 89.54% ± 0.61% | -0.91% | 60.74% | 5/5 |
| cumulative | word + affix + shape | 90.16% ± 0.54% | -0.30% | 64.39% | 4/5 |
| cumulative | word + affix + shape + context1 | 90.39% ± 0.49% | -0.07% | 66.55% | 3/5 |
| cumulative | word + affix + shape + context1 + context2 | 90.17% ± 0.65% | -0.28% | 66.66% | 5/5 |
