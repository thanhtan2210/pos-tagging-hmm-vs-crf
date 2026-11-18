# GA chọn nhóm đặc trưng CRF (vi)

Tập con train frac=0.3, k=2, phạt 0.002/nhóm, seed=42

**Tốt nhất:** word, affix, shape, context1, syllable

| Thế hệ | Fitness tốt nhất | Acc của cá thể tốt nhất | TB quần thể | Nhóm |
|---|---|---|---|---|
| 0 | 0.8341 | 0.8461 | 0.6447 | word, affix, shape, context1, context2, syllable |
| 1 | 0.8341 | 0.8461 | 0.8172 | word, affix, shape, context1, context2, syllable |
| 2 | 0.8377 | 0.8477 | 0.8276 | word, affix, shape, context1, syllable |
| 3 | 0.8377 | 0.8477 | 0.8347 | word, affix, shape, context1, syllable |
| 4 | 0.8377 | 0.8477 | 0.8350 | word, affix, shape, context1, syllable |
| 5 | 0.8377 | 0.8477 | 0.8332 | word, affix, shape, context1, syllable |
