"""Các độ đo đánh giá cho gán nhãn từ loại.

- token_acc : độ đo chuẩn của lĩnh vực, nhưng bị các nhãn phổ biến (NOUN, VERB...) chi phối
- oov_acc   : accuracy riêng trên từ không có trong tập train (phục vụ RQ2)
- macro_f1  : trung bình F1 các nhãn, mỗi nhãn có trọng số như nhau -> lộ ra nhãn hiếm bị đoán sai
- sent_acc  : tỷ lệ câu đúng hoàn toàn
"""

# TODO (mục 0, làm đầu tiên): tách "dự đoán" khỏi "tính metric"
# - [x] predict_all(tagger, sentences) -> (records, predict_time_s)
#       records: list các (words, gold, pred) theo từng câu
# - [x] metrics(records, train_vocab, mask=None) -> dict
#       mask: hàm/điều kiện chọn tập token con (OOV, từ mơ hồ, câu > 25 từ, ...)
# - [x] evaluate() giữ nguyên chữ ký, chỉ còn là metrics(predict_all(...)) để test/script cũ vẫn chạy
# - [x] save_records / load_records: results/preds/{lang}_{model}_{split}.jsonl

import json
import time

from sklearn.metrics import classification_report, f1_score

NAN = float("nan")


def evaluate(tagger, sentences, train_vocab):
    records, predict_time = predict_all(tagger, sentences)
    result = metrics(records, train_vocab)
    result["predict_time_s"] = predict_time
    return result


def _ratio(num, den):
    return num / den if den else NAN


def metrics(records, train_vocab, mask=None):
    """Tính metric trên records; mask(words, i) -> bool chọn token nào được chấm."""
    gold, pred, is_oov = [], [], []
    n_sent, n_sent_correct = 0, 0
    for words, tags, p in records:
        selected = [i for i in range(
            len(words)) if mask is None or mask(words, i)]
        if not selected:
            continue
        n_sent += 1
        sent_ok = True
        for i in selected:
            gold.append(tags[i])
            pred.append(p[i])
            is_oov.append(words[i] not in train_vocab)
            sent_ok = sent_ok and tags[i] == p[i]
        n_sent_correct += sent_ok

    correct = [g == p for g, p in zip(gold, pred)]
    oov = [c for c, o in zip(correct, is_oov) if o]
    labels = sorted(set(gold))
    if not gold:
        return {"token_acc": NAN, "oov_acc": NAN, "oov_rate": NAN,
                "macro_f1": NAN, "sent_acc": NAN, "n_tokens": 0, "report": ""}
    return {
        "token_acc": _ratio(sum(correct), len(correct)),
        "oov_acc": _ratio(sum(oov), len(oov)),
        "oov_rate": _ratio(sum(is_oov), len(is_oov)),
        "macro_f1": f1_score(gold, pred, labels=labels, average="macro", zero_division=0),
        "sent_acc": _ratio(n_sent_correct, n_sent),
        "report": classification_report(gold, pred, labels=labels, zero_division=0),
        "n_tokens": len(gold),
    }


def predict_all(tagger, sentences):
    records = []
    start = time.perf_counter()
    for words, tags in sentences:
        p = tagger.predict(words)
        records.append((list(words), list(tags), list(p)))
    predict_time = time.perf_counter() - start
    return records, predict_time


def save_records(records, path):
    from pathlib import Path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for words, tags, p in records:
            f.write(json.dumps({"words": list(words), "gold": list(tags),
                                "pred": list(p)}, ensure_ascii=False) + "\n")


def load_records(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                records.append((r["words"], r["gold"], r["pred"]))
    return records
