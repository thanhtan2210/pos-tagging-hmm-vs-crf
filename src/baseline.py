"""Baseline: gán mỗi từ nhãn xuất hiện nhiều nhất của nó trong tập train."""

# TODO (mục 4, mốc so sánh cho RQ2):
# - [x] (tùy chọn) với từ OOV: đoán theo hậu tố / chữ hoa / chữ số thay vì luôn trả self.default,
#       để so OOV accuracy công bằng hơn. Giữ bản gốc làm một dòng riêng trong bảng.

from collections import Counter, defaultdict

from src.hmm import word_signature


class MostFrequentTagger:
    """Từ chưa gặp (OOV) được gán nhãn phổ biến nhất của toàn tập train.

    Mọi mô hình trong báo cáo phải thắng baseline này mới chứng tỏ được việc
    dùng ngữ cảnh (nhãn/từ xung quanh) có ích.
    """

    def __init__(self, oov="default"):
        # oov="default": luôn trả nhãn phổ biến nhất; oov="signature": nhãn phổ biến nhất
        # của lớp hình thái (số, viết hoa, hậu tố...), học từ các từ hiếm (xuất hiện 1 lần) trong train.
        self.oov = oov

    def fit(self, sentences):
        counts = defaultdict(Counter)
        all_tags = Counter()
        for words, tags in sentences:
            for w, t in zip(words, tags):
                counts[w][t] += 1
                all_tags[t] += 1
        self.lexicon = {w: c.most_common(1)[0][0] for w, c in counts.items()}
        self.default = all_tags.most_common(1)[0][0]
        sig_counts = defaultdict(Counter)
        for w, c in counts.items():
            if c.total() == 1:
                sig_counts[word_signature(w)].update(c)
        self.sig_lexicon = {s: c.most_common(1)[0][0] for s, c in sig_counts.items()}
        return self

    def _oov_tag(self, w):
        if self.oov == "signature":
            return self.sig_lexicon.get(word_signature(w), self.default)
        return self.default

    def predict(self, words):
        return [self.lexicon[w] if w in self.lexicon else self._oov_tag(w) for w in words]
