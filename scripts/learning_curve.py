"""RQ1: learning curve HMM vs CRF (Ng & Jordan, 2002).

Mô hình sinh (HMM) được kỳ vọng hội tụ nhanh hơn khi ít dữ liệu, mô hình phân biệt (CRF)
có tiệm cận tốt hơn khi nhiều dữ liệu. Huấn luyện trên tập con của train, đánh giá trên dev.

Ví dụ:
    python scripts/learning_curve.py
    python scripts/learning_curve.py --langs vi --seeds 3
"""

# - [x] frac in [0.05, 0.1, 0.25, 0.5, 1.0], mỗi frac chạy 5 seed (frac = 1 chỉ cần 1)
# - [x] train_vocab tính theo TẬP CON đang dùng (OOV thay đổi theo frac)
# - [x] ghi CSV (lang, model, frac, seed, metrics) vào results/tables/
# - [x] vẽ trung bình ± độ lệch chuẩn -> results/figures/learning_curve_{lang}.png

import argparse
import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.run_experiments import load_params  # noqa: E402
from src.data import TREEBANKS, load, vocabulary  # noqa: E402
from src.evaluate import metrics, predict_all  # noqa: E402
from src.model_selection import subsample  # noqa: E402

FRACS = [0.05, 0.1, 0.25, 0.5, 1.0]
FIELDS = ["lang", "model", "frac", "seed", "n_train", "token_acc", "oov_acc", "oov_rate", "macro_f1"]


def plot(rows, lang, models):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for metric, ax in zip(("token_acc", "oov_acc"), axes):
        for name in models:
            pts = [r for r in rows if r["lang"] == lang and r["model"] == name]
            fracs = sorted({r["frac"] for r in pts})
            vals = [[r[metric] for r in pts if r["frac"] == f] for f in fracs]
            n = [np.mean([r["n_train"] for r in pts if r["frac"] == f]) for f in fracs]
            ax.errorbar(n, [np.mean(v) for v in vals], yerr=[np.std(v) for v in vals],
                        marker="o", capsize=3, label=name)
        ax.set_xscale("log")
        ax.set_xlabel("số câu train")
        ax.set_ylabel(metric)
        ax.grid(alpha=0.3)
        ax.legend()
    fig.suptitle(f"Learning curve ({lang}, đánh giá trên dev, TB ± độ lệch chuẩn)")
    fig.tight_layout()
    out = ROOT / "results" / "figures" / f"learning_curve_{lang}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--models", nargs="+", default=["hmm", "crf"])
    parser.add_argument("--fracs", nargs="+", type=float, default=FRACS)
    parser.add_argument("--seeds", type=int, default=5)
    args = parser.parse_args()

    rows = []
    for lang in args.langs:
        train, dev = load(lang, "train"), load(lang, "dev")
        for frac in args.fracs:
            for seed in range(1 if frac >= 1 else args.seeds):
                sub = subsample(train, frac, seed)
                vocab = vocabulary(sub)  # OOV tính theo tập con đang dùng
                for name in args.models:
                    cls, params = load_params(lang, name)
                    records, _ = predict_all(cls(**params).fit(sub), dev)
                    m = metrics(records, vocab)
                    row = {"lang": lang, "model": name, "frac": frac, "seed": seed,
                           "n_train": len(sub), **{k: m[k] for k in FIELDS[5:]}}
                    rows.append(row)
                    print(f"[{lang}] {name} frac={frac} seed={seed}: "
                          f"acc={m['token_acc']:.4f} oov={m['oov_acc']:.4f}")
        print("Đã vẽ", plot(rows, lang, args.models).relative_to(ROOT))

    out = ROOT / "results" / "tables" / "learning_curve.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print("Đã ghi", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
