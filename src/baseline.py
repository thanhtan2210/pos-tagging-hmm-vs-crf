"""Baseline: gán mỗi từ nhãn xuất hiện nhiều nhất của nó trong tập train."""

# TODO (mục 4, mốc so sánh cho RQ2):
# - [ ] (tùy chọn) với từ OOV: đoán theo hậu tố / chữ hoa / chữ số thay vì luôn trả self.default,
#       để so OOV accuracy công bằng hơn. Giữ bản gốc làm một dòng riêng trong bảng.

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
