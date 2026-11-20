"""Chọn tham số không rò rỉ: k-fold theo câu trên train.

Dev và test không được dùng ở đây, nên chúng vẫn là ước lượng không thiên lệch.
"""

# - [x] kfold_sentences(sentences, k, seed) -> list[(train_i, val_i)]  (chia theo CÂU)
# - [x] grid_search(model_cls, grid, sentences, k, metric="token_acc") -> (best_params, bảng điểm)
# - [x] subsample(sentences, frac, seed) cho learning curve (RQ1)

import itertools
import random
import statistics
import time

from src.data import vocabulary
from src.evaluate import metrics, predict_all

# Giao thức đánh giá trong giai đoạn phát triển (docs/notes/GHI_CHU.md, mục 2).
# Dev của VTB lệch phân phối so với train/test (1/3 số câu dài hơn 25 từ, train/test
# không có câu nào như vậy), nên với tiếng Việt mọi so sánh dùng k-fold trên train;
# tiếng Anh dùng dev. Dev VTB đầy đủ chỉ còn dùng cho thí nghiệm phụ "accuracy theo độ dài câu".
EVAL_SPLIT = {"vi": "cv", "en": "dev"}
CV_K, CV_SEED = 5, 42


def _shuffled_indices(n, seed):
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    return idx


def kfold_sentences(sentences, k=5, seed=42):
    """Chia theo câu: token trong cùng một câu luôn nằm chung một fold."""
    idx = _shuffled_indices(len(sentences), seed)
    folds = [idx[f::k] for f in range(k)]
    splits = []
    for f in range(k):
        val_set = set(folds[f])
        train_i = [sentences[i] for i in idx if i not in val_set]
        val_i = [sentences[i] for i in folds[f]]
        splits.append((train_i, val_i))
    return splits


def subsample(sentences, frac, seed=42):
    n = max(1, round(len(sentences) * frac))
    idx = _shuffled_indices(len(sentences), seed)[:n]
    return [sentences[i] for i in sorted(idx)]


def param_grid(grid):
    """{"a": [1, 2], "b": [3]} -> [{"a": 1, "b": 3}, {"a": 2, "b": 3}]"""
    keys = list(grid)
    return [dict(zip(keys, vals)) for vals in itertools.product(*(grid[k] for k in keys))]


def cross_val_predict(model_cls, params, sentences, k=CV_K, seed=CV_SEED):
    """Dự đoán out-of-fold: mỗi câu được gán nhãn bởi mô hình không thấy câu đó lúc học.

    Trả về một dict cho mỗi fold: records (predict_all trên fold giữ lại), train (phần
    dùng để học, cần cho OOV/từ mơ hồ của fold đó), fit_time_s, predict_time_s.
    Nối records của các fold được đúng một lượt dự đoán cho toàn bộ `sentences`,
    theo thứ tự của kfold_sentences(sentences, k, seed).
    """
    folds = []
    for train_i, val_i in kfold_sentences(sentences, k, seed):
        start = time.perf_counter()
        model = model_cls(**params).fit(train_i)
        fit_time = time.perf_counter() - start
        records, predict_time = predict_all(model, val_i)
        folds.append({"records": records, "train": train_i,
                      "fit_time_s": fit_time, "predict_time_s": predict_time})
    return folds


def cross_val_score(model_cls, params, sentences, k=CV_K, seed=CV_SEED, metric="token_acc"):
    return [metrics(f["records"], vocabulary(f["train"]))[metric]
            for f in cross_val_predict(model_cls, params, sentences, k, seed)]


def grid_search(model_cls, grid, sentences, k=5, metric="token_acc", seed=42, log=None):
    """Trả về (best_params, bảng) với bảng là list dict {**params, mean, std, scores}."""
    table = []
    for params in param_grid(grid):
        scores = cross_val_score(model_cls, params, sentences, k, seed, metric)
        row = {**params, "mean": statistics.mean(scores),
               "std": statistics.stdev(scores) if len(scores) > 1 else 0.0, "scores": scores}
        table.append(row)
        if log:
            log(row)
    best = max(table, key=lambda r: r["mean"])
    return {key: best[key] for key in grid}, table
