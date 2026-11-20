"""Phân tích lỗi từ results/preds/ (không huấn luyện lại).

Cần chạy scripts/run_experiments.py trước để có results/preds/{lang}_{model}_{split}.jsonl.

Ví dụ:
    python scripts/analyze.py
    python scripts/analyze.py --models hmm crf --split dev
"""

# - [x] ma trận nhầm lẫn (chuẩn hóa theo hàng) + top-10 cặp nhầm gold -> pred
# - [x] accuracy theo độ dài câu: <=10, 11-25, 26-50, >50
# - [x] accuracy theo nhóm token: OOV, từ mơ hồ, từ nhiều âm tiết, từ ngữ pháp hóa
# - [x] liệt kê câu HMM sai / CRF đúng và ngược lại
# - [x] gọi src/stats.py để so sánh từng cặp mô hình

import argparse
import itertools
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.eda import ambiguous_words  # noqa: E402
from src.data import TREEBANKS, load, vocabulary  # noqa: E402
from src.evaluate import load_records, metrics  # noqa: E402
from src.stats import mcnemar, paired_bootstrap  # noqa: E402

LENGTH_BINS = [(1, 10, "<=10"), (11, 25, "11-25"), (26, 50, "26-50"), (51, 10**9, ">50")]
GRAMMATICALIZED = {"được", "đến", "về", "cho", "vào", "ở", "để"}


def token_groups(lang, train_vocab, ambiguous):
    groups = {
        "tất cả": None,
        "OOV": lambda w, i: w[i] not in train_vocab,
        "trong từ vựng": lambda w, i: w[i] in train_vocab,
        "từ mơ hồ": lambda w, i: w[i] in ambiguous,
    }
    if lang == "vi":
        groups["nhiều âm tiết"] = lambda w, i: " " in w[i]
        groups["ngữ pháp hóa"] = lambda w, i: w[i].lower() in GRAMMATICALIZED
    for lo, hi, label in LENGTH_BINS:
        groups[f"câu {label} từ"] = lambda w, i, lo=lo, hi=hi: lo <= len(w) <= hi
    return groups


def confusion(records, labels):
    idx = {t: i for i, t in enumerate(labels)}
    M = np.zeros((len(labels), len(labels)))
    for _, gold, pred in records:
        for g, p in zip(gold, pred):
            M[idx[g], idx[p]] += 1
    return M


def plot_confusion(M, labels, title, out):
    norm = M / np.maximum(M.sum(axis=1, keepdims=True), 1)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(labels)), labels, rotation=90)
    ax.set_yticks(range(len(labels)), labels)
    ax.set_xlabel("dự đoán")
    ax.set_ylabel("gold")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def top_confusions(records, k=10):
    c = Counter((g, p) for _, gold, pred in records for g, p in zip(gold, pred) if g != p)
    return c.most_common(k)


def disagreements(rec_a, rec_b, k=5):
    """Câu A sai mà B đúng hoàn toàn, ưu tiên câu ngắn để dễ đưa vào báo cáo."""
    out = [(w, g, pa, pb) for (w, g, pa), (_, _, pb) in zip(rec_a, rec_b) if pa != g and pb == g]
    return sorted(out, key=lambda x: len(x[0]))[:k]


def fmt_sentence(words, gold, pred_a, pred_b, name_a, name_b):
    rows = [f"| từ | gold | {name_a} | {name_b} |", "|---|---|---|---|"]
    for w, g, a, b in zip(words, gold, pred_a, pred_b):
        mark = lambda t: f"**{t}**" if t != g else t  # noqa: E731
        rows.append(f"| {w} | {g} | {mark(a)} | {mark(b)} |")
    return rows


def analyze(lang, models, split):
    train = load(lang, "train")
    train_vocab = vocabulary(train)
    ambiguous = ambiguous_words(train)
    recs = {}
    for name in models:
        path = ROOT / "results" / "preds" / f"{lang}_{name}_{split}.jsonl"
        if path.exists():
            recs[name] = load_records(path)
        else:
            print(f"[{lang}] thiếu {path.relative_to(ROOT)}, bỏ qua {name}")
    if not recs:
        return None
    names = list(recs)
    lines = [f"# Phân tích lỗi: {lang} ({TREEBANKS[lang][0]}), {split}", ""]

    # Accuracy theo nhóm token / độ dài câu.
    groups = token_groups(lang, train_vocab, ambiguous)
    lines += ["## Token accuracy theo nhóm", "",
              "| Nhóm | Số token | " + " | ".join(names) + " |", "|---" * (len(names) + 2) + "|"]
    for gname, mask in groups.items():
        ms = [metrics(recs[n], train_vocab, mask) for n in names]
        lines.append(f"| {gname} | {ms[0]['n_tokens']:,} | "
                     + " | ".join(f"{m['token_acc']:.2%}" for m in ms) + " |")

    # So sánh từng cặp mô hình.
    lines += ["", "## Kiểm định từng cặp (A - B, token accuracy)", "",
              "| A | B | Hiệu | CI 95% (bootstrap theo câu) | McNemar b / c | p-value |",
              "|---|---|---|---|---|---|"]
    for a, b in itertools.combinations(names, 2):
        diff, (lo, hi) = paired_bootstrap(recs[a], recs[b], n=1000, seed=42)
        nb, nc, p = mcnemar(recs[a], recs[b])
        lines.append(f"| {a} | {b} | {diff:+.2%} | [{lo:+.2%}, {hi:+.2%}] | {nb} / {nc} | {p:.2g} |")

    # Ma trận nhầm lẫn + top cặp nhầm.
    labels = sorted({t for r in recs.values() for _, g, p in r for t in g + p})
    suffix = "" if split == "dev" else f"_{split}"  # không ghi đè hình của dev
    for name in names:
        out = ROOT / "results" / "figures" / f"confusion_{lang}_{name}{suffix}.png"
        plot_confusion(confusion(recs[name], labels), labels, f"{name} ({lang}, {split})", out)
        lines += ["", f"## {name}: 10 cặp nhầm nhiều nhất (gold -> dự đoán)", "",
                  f"Ma trận nhầm lẫn chuẩn hóa theo hàng: `{out.relative_to(ROOT).as_posix()}`", "",
                  "| gold | dự đoán | số lần |", "|---|---|---|"]
        lines += [f"| {g} | {p} | {c} |" for (g, p), c in top_confusions(recs[name])]

    # Ví dụ câu mô hình này sai, mô hình kia đúng.
    if "hmm" in recs and "crf" in recs:
        for a, b in (("hmm", "crf"), ("crf", "hmm")):
            ex = disagreements(recs[a], recs[b])
            lines += ["", f"## Ví dụ: {a} sai, {b} đúng cả câu ({len(ex)} câu ngắn nhất)", ""]
            for w, g, pa, pb in ex:
                lines += fmt_sentence(w, g, pa, pb, a, b) + [""]

    text = "\n".join(lines) + "\n"
    out = ROOT / "results" / "tables" / f"analysis_{lang}_{split}.md"
    out.write_text(text, encoding="utf-8")
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--models", nargs="+", default=["baseline", "hmm", "crf"])
    parser.add_argument("--split", default="dev", choices=["dev", "test"])
    args = parser.parse_args()
    for lang in args.langs:
        out = analyze(lang, args.models, args.split)
        if out:
            print("Đã ghi", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
