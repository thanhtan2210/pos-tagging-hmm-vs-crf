"""RQ1: learning curve HMM vs CRF (Ng & Jordan, 2002).

Mô hình sinh (HMM) được kỳ vọng hội tụ nhanh hơn khi ít dữ liệu, mô hình phân biệt (CRF)
có tiệm cận tốt hơn khi nhiều dữ liệu. Huấn luyện trên tập con của train, rồi chấm theo
src/model_selection.EVAL_SPLIT:
    dev (en): lấy tập con của train với nhiều seed, chấm trên dev
    cv  (vi): trong mỗi fold của 5-fold trên train, lấy tập con phần học (seed = số thứ tự fold),
              chấm trên fold giữ lại -> 5 điểm đo mỗi mức (dev VTB lệch phân phối, xem GHI_CHU mục 2)

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
from src.model_selection import CV_K, CV_SEED, EVAL_SPLIT, kfold_sentences, subsample  # noqa: E402

FRACS = [0.05, 0.1, 0.25, 0.5, 1.0]
METRICS = ["token_acc", "oov_acc", "oov_rate", "macro_f1"]
# eval: dev hoặc cv; với cv, cột seed là số thứ tự fold
FIELDS = ["lang", "eval", "model", "frac", "seed", "n_train", *METRICS]
OUT = ROOT / "results" / "tables" / "learning_curve.csv"


def runs(lang, frac, n_seeds):
    """Các lần đo ở một mức dữ liệu: list (seed, tập con để học, tập để chấm)."""
    train = load(lang, "train")
    if EVAL_SPLIT[lang] == "cv":
        return [(f, subsample(tr, frac, f), va)
                for f, (tr, va) in enumerate(kfold_sentences(train, CV_K, CV_SEED))]
    dev = load(lang, "dev")
    return [(seed, subsample(train, frac, seed), dev) for seed in range(1 if frac >= 1 else n_seeds)]


def keep_other_langs(langs):
    """Giữ các dòng của ngôn ngữ không chạy lại (CSV dùng chung cho mọi ngôn ngữ)."""
    if not OUT.exists():
        return []
    with open(OUT, newline="", encoding="utf-8") as f:
        return [{"eval": "dev", **r} for r in csv.DictReader(f) if r["lang"] not in langs]


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
        ax.set_xlabel("số câu train" + (" (phần học của mỗi fold)" if EVAL_SPLIT[lang] == "cv" else ""))
        ax.set_ylabel(metric)
        ax.grid(alpha=0.3)
        ax.legend()
    where = f"{CV_K}-fold trên train" if EVAL_SPLIT[lang] == "cv" else "đánh giá trên dev"
    fig.suptitle(f"Learning curve ({lang}, {where}, TB ± độ lệch chuẩn)")
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
        for frac in args.fracs:
            for seed, sub, evalset in runs(lang, frac, args.seeds):
                vocab = vocabulary(sub)  # OOV tính theo tập con đang dùng
                for name in args.models:
                    cls, params = load_params(lang, name)
                    records, _ = predict_all(cls(**params).fit(sub), evalset)
                    m = metrics(records, vocab)
                    row = {"lang": lang, "eval": EVAL_SPLIT[lang], "model": name, "frac": frac, "seed": seed,
                           "n_train": len(sub), **{k: m[k] for k in METRICS}}
                    rows.append(row)
                    print(f"[{lang}] {name} frac={frac} seed={seed}: "
                          f"acc={m['token_acc']:.4f} oov={m['oov_acc']:.4f}")
        print("Đã vẽ", plot(rows, lang, args.models).relative_to(ROOT))

    order = list(TREEBANKS)
    rows = sorted(keep_other_langs(args.langs) + rows, key=lambda r: order.index(r["lang"]))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print("Đã ghi", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
