"""Kiểm định ý nghĩa thống kê khi so sánh hai mô hình trên cùng một split.

Đầu vào: records (words, gold, pred) theo từng câu, đọc từ results/preds/.
Hai danh sách records phải cùng thứ tự câu (cùng split).
"""

# - [x] paired_bootstrap(records_a, records_b, n=1000, seed) -> (hiệu trung bình, CI 95%)
# - [x] mcnemar(records_a, records_b) -> (b, c, p-value)

import numpy as np
from scipy.stats import binomtest, chi2


def _per_sentence_correct(records_a, records_b):
    if len(records_a) != len(records_b):
        raise ValueError("hai bộ records phải cùng số câu")
    ca, cb, n = [], [], []
    for (wa, ga, pa), (wb, gb, pb) in zip(records_a, records_b):
        if list(wa) != list(wb) or list(ga) != list(gb):
            raise ValueError("hai bộ records không cùng câu/đáp án")
        ca.append(sum(g == p for g, p in zip(ga, pa)))
        cb.append(sum(g == p for g, p in zip(gb, pb)))
        n.append(len(ga))
    return np.array(ca), np.array(cb), np.array(n)


def paired_bootstrap(records_a, records_b, n=1000, seed=42):
    """Hiệu token accuracy (A - B) và CI 95% bằng bootstrap theo CÂU.

    Lấy mẫu có hoàn lại các câu (token trong một câu không độc lập), cùng một mẫu
    cho cả A và B (ghép cặp). Trả về (hiệu trên dữ liệu gốc, (cận dưới, cận trên)).
    """
    ca, cb, ntok = _per_sentence_correct(records_a, records_b)
    diff = (ca.sum() - cb.sum()) / ntok.sum()
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(ntok), size=(n, len(ntok)))
    boot = (ca[idx].sum(axis=1) - cb[idx].sum(axis=1)) / ntok[idx].sum(axis=1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return float(diff), (float(lo), float(hi))


def mcnemar(records_a, records_b, exact_below=25):
    """b = số token A đúng B sai, c = B đúng A sai.

    b + c nhỏ: kiểm định nhị thức chính xác; ngược lại: chi bình phương có hiệu chỉnh liên tục.
    """
    b = c = 0
    for (_, g, pa), (_, _, pb) in zip(records_a, records_b):
        for gi, ai, bi in zip(g, pa, pb):
            b += ai == gi and bi != gi
            c += bi == gi and ai != gi
    if b + c == 0:
        return b, c, 1.0
    if b + c < exact_below:
        p = binomtest(b, b + c, 0.5).pvalue
    else:
        p = chi2.sf((abs(b - c) - 1) ** 2 / (b + c), df=1)
    return b, c, float(p)
