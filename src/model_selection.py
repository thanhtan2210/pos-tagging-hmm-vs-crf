"""Chọn tham số không rò rỉ: k-fold theo câu trên train.

Dev và test không được dùng ở đây, nên chúng vẫn là ước lượng không thiên lệch.
"""

# - [x] kfold_sentences(sentences, k, seed) -> list[(train_i, val_i)]  (chia theo CÂU)
# - [x] grid_search(model_cls, grid, sentences, k, metric="token_acc") -> (best_params, bảng điểm)
# - [x] subsample(sentences, frac, seed) cho learning curve (RQ1)

import itertools
import random
import statistics

from src.data import vocabulary
from src.evaluate import metrics, predict_all


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


def cross_val_score(model_cls, params, sentences, k=5, seed=42, metric="token_acc"):
    scores = []
    for train_i, val_i in kfold_sentences(sentences, k, seed):
        model = model_cls(**params).fit(train_i)
        records, _ = predict_all(model, val_i)
        scores.append(metrics(records, vocabulary(train_i))[metric])
    return scores


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
