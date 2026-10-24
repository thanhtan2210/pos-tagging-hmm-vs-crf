"""Baseline: gán mỗi từ nhãn xuất hiện nhiều nhất của nó trong tập train."""
from collections import Counter, defaultdict


class MostFrequentTagger:
    """Từ chưa gặp (OOV) được gán nhãn phổ biến nhất của toàn tập train.

    Mọi mô hình trong báo cáo phải thắng baseline này mới chứng tỏ được việc
    dùng ngữ cảnh (nhãn/từ xung quanh) có ích.
    """

    def fit(self, sentences):
        counts = defaultdict(Counter)
        all_tags = Counter()
        for words, tags in sentences:
            for w, t in zip(words, tags):
                counts[w][t] += 1
                all_tags[t] += 1
        self.lexicon = {w: c.most_common(1)[0][0] for w, c in counts.items()}
        self.default = all_tags.most_common(1)[0][0]
        return self

    def predict(self, words):
        return [self.lexicon.get(w, self.default) for w in words]
