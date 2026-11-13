"""Các độ đo đánh giá cho gán nhãn từ loại.

- token_acc : độ đo chuẩn của lĩnh vực, nhưng bị các nhãn phổ biến (NOUN, VERB...) chi phối
- oov_acc   : accuracy riêng trên từ không có trong tập train (phục vụ RQ2)
- macro_f1  : trung bình F1 các nhãn, mỗi nhãn có trọng số như nhau -> lộ ra nhãn hiếm bị đoán sai
- sent_acc  : tỷ lệ câu đúng hoàn toàn
"""

# TODO (mục 0, làm đầu tiên): tách "dự đoán" khỏi "tính metric"
# - [ ] predict_all(tagger, sentences) -> (records, predict_time_s)
#       records: list các (words, gold, pred) theo từng câu
# - [ ] metrics(records, train_vocab, mask=None) -> dict
#       mask: hàm/điều kiện chọn tập token con (OOV, từ mơ hồ, câu > 25 từ, ...)
# - [ ] evaluate() giữ nguyên chữ ký, chỉ còn là metrics(predict_all(...)) để test/script cũ vẫn chạy
# - [ ] save_records / load_records: results/preds/{lang}_{model}_{split}.jsonl

import time

from sklearn.metrics import classification_report, f1_score


def evaluate(tagger, sentences, train_vocab):
    gold, pred, is_oov = [], [], []
    n_sent_correct = 0
    start = time.perf_counter()
    for words, tags in sentences:
        p = tagger.predict(words)
        gold += tags
        pred += p
        is_oov += [w not in train_vocab for w in words]
        n_sent_correct += p == tags
    predict_time = time.perf_counter() - start

    correct = [g == p for g, p in zip(gold, pred)]
    oov = [c for c, o in zip(correct, is_oov) if o]
    labels = sorted(set(gold))
    return {
        "token_acc": sum(correct) / len(correct),
        "oov_acc": sum(oov) / len(oov) if oov else float("nan"),
        "oov_rate": sum(is_oov) / len(is_oov),
        "macro_f1": f1_score(gold, pred, labels=labels, average="macro", zero_division=0),
        "sent_acc": n_sent_correct / len(sentences),
        "predict_time_s": predict_time,
        "report": classification_report(gold, pred, labels=labels, zero_division=0),
    }
