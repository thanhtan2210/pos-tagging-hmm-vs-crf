"""MaxEnt từng từ và MEMM (RQ4, vấn đề label bias).

Cả ba mô hình MaxEnt / MEMM / CRF dùng CÙNG bộ đặc trưng quan sát trong src/features.py:
    MaxEntTagger : P(t_i | x), mỗi từ phân loại độc lập, không dùng nhãn trước
    MEMMTagger   : P(t_i | t_{i-1}, x), chuẩn hóa CỤC BỘ tại từng vị trí, giải mã bằng Viterbi
    CRF          : chuẩn hóa TOÀN CỤC trên cả chuỗi -> không bị label bias
"""

# - [x] MaxEntTagger: LogisticRegression trên đặc trưng của src/features.py
# - [x] MEMMTagger: thêm đặc trưng nhãn trước t_{i-1}; huấn luyện với nhãn gold
# - [x] giải mã MEMM bằng Viterbi trên log P(t_i | t_{i-1}, x)
# - [x] so sánh MaxEnt vs MEMM vs CRF với CÙNG bộ đặc trưng (đăng ký trong run_experiments)

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from src.features import ALL_GROUPS, word2features

START = "<S>"


class MaxEntTagger:
    def __init__(self, groups=None, C=1.0, max_iter=200):
        self.groups = tuple(groups) if groups is not None else ALL_GROUPS
        self.C, self.max_iter = C, max_iter

    def _feats(self, words, i, prev=None):
        return word2features(words, i, self.groups)

    def _training_rows(self, sentences):
        X, y = [], []
        for words, tags in sentences:
            for i in range(len(words)):
                X.append(self._feats(words, i, tags[i - 1] if i else START))
                y.append(tags[i])
        return X, y

    def fit(self, sentences):
        X, y = self._training_rows(sentences)
        self.vec = DictVectorizer()
        self.clf = LogisticRegression(C=self.C, max_iter=self.max_iter)
        self.clf.fit(self.vec.fit_transform(X), y)
        self.tags = list(self.clf.classes_)
        return self

    def predict(self, words):
        if not words:
            return []
        X = self.vec.transform([self._feats(words, i) for i in range(len(words))])
        return list(self.clf.predict(X))


class MEMMTagger(MaxEntTagger):
    def _feats(self, words, i, prev=None):
        f = word2features(words, i, self.groups)
        f["prev_tag"] = prev
        f["prev_tag|word"] = f"{prev}|{words[i].lower()}"
        return f

    def predict(self, words):
        n = len(words)
        if n == 0:
            return []
        T = len(self.tags)
        prevs = [START] + self.tags
        # log_p[k, a, j] = log P(t_k = j | t_{k-1} = prevs[a], x)
        rows = [self._feats(words, k, p) for k in range(n) for p in prevs]
        log_p = self.clf.predict_log_proba(self.vec.transform(rows)).reshape(n, T + 1, T)

        delta = log_p[0, 0]  # vị trí đầu: nhãn trước là START
        back = np.zeros((n, T), dtype=int)
        for k in range(1, n):
            scores = delta[:, None] + log_p[k, 1:]  # (T nhãn trước, T nhãn hiện tại)
            back[k] = scores.argmax(axis=0)
            delta = scores.max(axis=0)
        path = [int(delta.argmax())]
        for k in range(n - 1, 0, -1):
            path.append(int(back[k, path[-1]]))
        return [self.tags[i] for i in reversed(path)]
