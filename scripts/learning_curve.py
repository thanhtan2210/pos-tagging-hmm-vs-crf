"""RQ1: learning curve HMM vs CRF (Ng & Jordan, 2002).

TODO:
- [ ] frac in [0.05, 0.1, 0.25, 0.5, 1.0], mỗi frac chạy 5 seed (frac = 1 chỉ cần 1)
- [ ] train_vocab tính theo TẬP CON đang dùng (OOV thay đổi theo frac)
- [ ] ghi CSV (lang, model, frac, seed, metrics) vào results/tables/
- [ ] vẽ trung bình ± độ lệch chuẩn -> results/figures/learning_curve_{lang}.png
"""
