# Ablation đặc trưng CRF (vi), đánh giá trên dev

| Kiểu | Bộ đặc trưng | Token acc | Δ so với đầy đủ | OOV acc | Số đặc trưng ≠ 0 |
|---|---|---|---|---|---|
| leave-one-out | đầy đủ | 85.62% | +0.00% | 63.78% | 64446 |
| leave-one-out | - word | 85.25% | -0.37% | 63.20% | 60674 |
| leave-one-out | - affix | 85.36% | -0.26% | 64.61% | 52728 |
| leave-one-out | - shape | 84.40% | -1.22% | 58.71% | 64309 |
| leave-one-out | - context1 | 84.70% | -0.93% | 60.47% | 35712 |
| leave-one-out | - context2 | 85.90% | +0.28% | 64.05% | 49788 |
| leave-one-out | - syllable | 85.23% | -0.39% | 62.93% | 59035 |
| cumulative | word | 81.79% | -3.83% | 45.66% | 3789 |
| cumulative | word + affix | 83.95% | -1.67% | 55.39% | 15507 |
| cumulative | word + affix + shape | 84.98% | -0.64% | 60.80% | 15643 |
| cumulative | word + affix + shape + context1 | 85.76% | +0.14% | 63.39% | 44377 |
| cumulative | word + affix + shape + context1 + context2 | 85.23% | -0.39% | 62.93% | 59035 |
