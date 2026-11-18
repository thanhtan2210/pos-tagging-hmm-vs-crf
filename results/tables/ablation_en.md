# Ablation đặc trưng CRF (en), đánh giá trên dev

| Kiểu | Bộ đặc trưng | Token acc | Δ so với đầy đủ | OOV acc | Số đặc trưng ≠ 0 |
|---|---|---|---|---|---|
| leave-one-out | đầy đủ | 94.78% | +0.00% | 79.44% | 118679 |
| leave-one-out | - word | 94.79% | +0.00% | 79.44% | 110302 |
| leave-one-out | - affix | 93.74% | -1.04% | 72.02% | 131109 |
| leave-one-out | - shape | 94.04% | -0.75% | 74.94% | 132243 |
| leave-one-out | - context1 | 93.53% | -1.25% | 78.01% | 90505 |
| leave-one-out | - context2 | 94.80% | +0.02% | 79.06% | 102410 |
| leave-one-out | - syllable | 94.74% | -0.04% | 79.30% | 101859 |
| cumulative | word | 90.27% | -4.51% | 54.19% | 19205 |
| cumulative | word + affix | 92.27% | -2.52% | 71.20% | 43362 |
| cumulative | word + affix + shape | 93.09% | -1.69% | 76.71% | 40131 |
| cumulative | word + affix + shape + context1 | 94.74% | -0.04% | 79.06% | 83620 |
| cumulative | word + affix + shape + context1 + context2 | 94.74% | -0.04% | 79.30% | 101859 |
