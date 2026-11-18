"""HMM bigram cho gán nhãn từ loại.

Ký hiệu (khớp slide Ch.5 Graphical Models, phần HMM):
    pi[i]   = P(t_1 = i)                      xác suất nhãn đầu câu
    A[i, j] = P(t_k = j | t_{k-1} = i)        xác suất chuyển nhãn
    B[i, w] = P(w_k = w | t_k = i)            xác suất phát xạ từ
Mọi tính toán làm trong không gian log để tránh underflow với câu dài
(tích của hàng chục xác suất nhỏ sẽ về 0 khi dùng số thực).

Chiến lược xử lý từ chưa gặp (tham số `unk`, phục vụ RQ2):
    "add-alpha" : một UNK chung, chỉ nhận khối xác suất nhỏ từ làm trơn
    "rare"      : từ xuất hiện <= rare_k lần trong train được thay bằng UNK khi đếm,
                  nhờ đó UNK học được phân phối nhãn của "từ hiếm" thật sự
    "signature" : như "rare" nhưng thay bằng lớp UNK theo hình thái
                  (UNK-NUM, UNK-CAP, UNK-HYPHEN, ...)
"""

# TODO (mục 4, RQ2):
# - [x] HMMTagger(alpha, unk="...") với các lựa chọn add-alpha / rare / signature
# - [x] alpha và unk được chọn bằng scripts/tune.py, không chọn tay trên dev

import re
from collections import Counter

import numpy as np

UNK = "<UNK>"
UNK_STRATEGIES = ("add-alpha", "rare", "signature")


def word_signature(w):
    """Lớp UNK theo hình thái từ; dùng chung cho mọi ngôn ngữ."""
    if any(ch.isdigit() for ch in w):
        return "<UNK-NUM>"
    if not any(ch.isalpha() for ch in w):
        return "<UNK-PUNCT>"
    if "-" in w:
        return "<UNK-HYPHEN>"
    if " " in w:  # từ tiếng Việt nhiều âm tiết
        return "<UNK-MULTI-CAP>" if w[0].isupper() else "<UNK-MULTI>"
    if w.isupper():
        return "<UNK-ALLCAP>"
    if w[0].isupper():
        return "<UNK-CAP>"
    for suf in ("ing", "ed", "ly", "s", "tion", "er", "est", "al", "ous", "ive", "able"):
        if w.lower().endswith(suf) and len(w) > len(suf) + 2:
            return f"<UNK-{suf}>"
    return UNK


class HMMTagger:
    def __init__(self, alpha=1.0, unk="add-alpha", rare_k=1):
        if unk not in UNK_STRATEGIES:
            raise ValueError(f"unk phải thuộc {UNK_STRATEGIES}")
        self.alpha = alpha  # hệ số add-alpha (Laplace khi alpha = 1) smoothing
        self.unk = unk
        self.rare_k = rare_k

    def _unk_class(self, w):
        return word_signature(w) if self.unk == "signature" else UNK

    def _map_train_word(self, w, freq):
        if self.unk != "add-alpha" and freq[w] <= self.rare_k:
            return self._unk_class(w)
        return w

    def fit(self, sentences):
        freq = Counter(w for words, _ in sentences for w in words)
        sentences = [([self._map_train_word(w, freq) for w in words], tags)
                     for words, tags in sentences]

        self.tags = sorted({t for _, tags in sentences for t in tags})
        self.tag2id = {t: i for i, t in enumerate(self.tags)}
        vocab = sorted({w for words, _ in sentences for w in words} | {UNK})
        self.word2id = {w: i for i, w in enumerate(vocab)}
        T, V = len(self.tags), len(vocab)

        start = np.zeros(T)
        trans = np.zeros((T, T))
        emit = np.zeros((T, V))

        # (1) Đếm.
        for words, tags in sentences:
            t_ids = [self.tag2id[t] for t in tags]
            start[t_ids[0]] += 1
            for prev, cur in zip(t_ids, t_ids[1:]):
                trans[prev, cur] += 1
            for w, t in zip(words, t_ids):
                emit[t, self.word2id[w]] += 1

        # (2) Làm trơn add-alpha, chuẩn hóa từng hàng, lấy log.
        def log_normalize(counts):
            counts = counts + self.alpha
            return np.log(counts / counts.sum(axis=-1, keepdims=True))

        self.log_pi = log_normalize(start)
        self.log_A = log_normalize(trans)
        self.log_B = log_normalize(emit)
        return self

    def _word_id(self, w):
        if w in self.word2id:
            return self.word2id[w]
        return self.word2id.get(self._unk_class(w), self.word2id[UNK])

    def predict(self, words):
        ids = [self._word_id(w) for w in words]
        path = viterbi(self.log_pi, self.log_A, self.log_B[:, ids])
        return [self.tags[i] for i in path]


def viterbi(log_pi, log_A, log_emit):
    """Tìm chuỗi nhãn có xác suất hợp cao nhất.

    log_pi   : (T,)    log P(t_1 = i)
    log_A    : (T, T)  log P(t_k = j | t_{k-1} = i)
    log_emit : (T, n)  log_emit[i, k] = log P(w_k | t_k = i), n là độ dài câu
    Trả về list gồm n chỉ số nhãn.

    delta[k, j] = điểm (log) tốt nhất của mọi chuỗi nhãn dài k+1 kết thúc bằng nhãn j
    back[k, j]  = nhãn ở vị trí k-1 trên chuỗi tốt nhất đó
    Độ phức tạp O(n * T^2).
    """
    T, n = log_emit.shape
    delta = np.empty((n, T))
    back = np.zeros((n, T), dtype=int)
    delta[0] = log_pi + log_emit[:, 0]
    for k in range(1, n):
        scores = delta[k - 1][:, None] + log_A  # scores[i, j]: đi từ nhãn i sang j
        back[k] = scores.argmax(axis=0)
        delta[k] = scores.max(axis=0) + log_emit[:, k]

    path = [int(delta[-1].argmax())]
    for k in range(n - 1, 0, -1):
        path.append(int(back[k, path[-1]]))
    return path[::-1]
