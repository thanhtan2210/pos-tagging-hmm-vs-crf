"""Chọn tham số không rò rỉ: k-fold theo câu trên train.

TODO:
- [ ] kfold_sentences(sentences, k, seed) -> list[(train_i, val_i)]  (chia theo CÂU, không theo token)
- [ ] grid_search(model_cls, grid, sentences, k, metric="token_acc") -> (best_params, bảng điểm)
- [ ] subsample(sentences, frac, seed) cho learning curve (RQ1)
"""
