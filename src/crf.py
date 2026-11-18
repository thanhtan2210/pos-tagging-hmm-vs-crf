"""CRF chuỗi tuyến tính cho gán nhãn từ loại, bọc sklearn_crfsuite.CRF.

Huấn luyện bằng L-BFGS, phạt L1 (c1) và L2 (c2). c1/c2 lấy từ configs/best_params.json
(chọn bằng k-fold trên train trong scripts/tune.py), không chọn tay trên dev.
"""

# - [x] class CRFTagger(groups=None, c1, c2, max_iterations), giao diện fit/predict
# - [x] sent2features(words, groups) trong src/features.py
# - [x] c1/c2 lấy từ configs/best_params.json (scripts/run_experiments.py)
# - [x] với c1 > 0: n_active_features() đếm đặc trưng có trọng số khác 0
# - [x] đăng ký "crf" vào MODELS trong scripts/run_experiments.py

import sklearn_crfsuite

from src.features import ALL_GROUPS, sent2features


class CRFTagger:
    def __init__(self, groups=None, c1=0.1, c2=0.1, max_iterations=100):
        self.groups = tuple(groups) if groups is not None else ALL_GROUPS
        self.c1, self.c2, self.max_iterations = c1, c2, max_iterations

    def fit(self, sentences):
        X = [sent2features(words, self.groups) for words, _ in sentences]
        y = [list(tags) for _, tags in sentences]
        self.crf = sklearn_crfsuite.CRF(
            algorithm="lbfgs", c1=self.c1, c2=self.c2,
            max_iterations=self.max_iterations, all_possible_transitions=True,
        )
        self.crf.fit(X, y)
        return self

    def predict(self, words):
        if not words:
            return []
        return self.crf.predict_single(sent2features(words, self.groups))

    def n_active_features(self, eps=1e-8):
        """Số đặc trưng trạng thái có trọng số |w| > eps (L1 đẩy nhiều trọng số về 0)."""
        return sum(abs(w) > eps for w in self.crf.state_features_.values())
