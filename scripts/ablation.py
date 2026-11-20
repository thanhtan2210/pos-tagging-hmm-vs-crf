"""RQ3: ablation nhóm đặc trưng CRF trên vi và en.

Hai kiểu:
    leave-one-out : bộ đầy đủ bỏ đi đúng một nhóm -> nhóm nào mất đi làm tụt điểm nhiều nhất
    cumulative    : bắt đầu từ "word", thêm lần lượt từng nhóm theo thứ tự cố định
c1/c2 giữ cố định theo configs/best_params.json để chỉ có bộ đặc trưng thay đổi.
Mặc định theo src/model_selection.EVAL_SPLIT: tiếng Việt dùng 5-fold trên train (dev VTB lệch
phân phối, xem docs/notes/GHI_CHU.md mục 2), tiếng Anh dùng dev. --k 0 ép dùng dev, --k N ép N-fold.

Ví dụ:
    python scripts/ablation.py
    python scripts/ablation.py --langs vi --k 3
"""

# - [x] kiểu "bỏ một nhóm" (leave-one-out) từ bộ đầy đủ
# - [x] kiểu "thêm dần" (cumulative) bắt đầu từ nhóm word
# - [x] giữ c1/c2 cố định; nếu kịp thì có sai số từ k-fold (--k)
# - [x] xuất bảng Markdown + hình vào results/tables/, results/figures/

import argparse
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.run_experiments import load_params  # noqa: E402
from src.crf import CRFTagger  # noqa: E402
from src.data import TREEBANKS, load, vocabulary  # noqa: E402
from src.evaluate import metrics, predict_all  # noqa: E402
from src.features import ALL_GROUPS  # noqa: E402
from src.model_selection import CV_K, CV_SEED, EVAL_SPLIT, cross_val_predict  # noqa: E402


def configs():
    yield "leave-one-out", "đầy đủ", ALL_GROUPS
    for g in ALL_GROUPS:
        yield "leave-one-out", f"- {g}", tuple(x for x in ALL_GROUPS if x != g)
    for n in range(1, len(ALL_GROUPS)):  # bộ dài nhất (n = len) trùng "đầy đủ"
        yield "cumulative", " + ".join(ALL_GROUPS[:n]), ALL_GROUPS[:n]


def run(lang, k, seed):
    train = load(lang, "train")
    dev = load(lang, "dev") if k == 0 else None
    _, params = load_params(lang, "crf")
    rows = []
    for kind, label, groups in configs():
        p = {**params, "groups": groups}
        if k > 0:
            # OOV theo phần học của từng fold; giữ điểm từng fold để so cặp với bộ đầy đủ
            ms = [metrics(f["records"], vocabulary(f["train"]))
                  for f in cross_val_predict(CRFTagger, p, train, k, seed)]
            fold_acc = [m["token_acc"] for m in ms]
            acc, std = statistics.mean(fold_acc), statistics.stdev(fold_acc)
            oov, n_feat = statistics.mean(m["oov_acc"] for m in ms), None
        else:
            model = CRFTagger(**p).fit(train)
            records, _ = predict_all(model, dev)
            m = metrics(records, vocabulary(train))
            acc, std, oov, n_feat = m["token_acc"], 0.0, m["oov_acc"], model.n_active_features()
            fold_acc = None
        rows.append({"kind": kind, "label": label, "acc": acc, "std": std, "oov": oov, "n_feat": n_feat,
                     "fold_acc": fold_acc})
        print(f"[{lang}] {kind:13s} {label:45s} acc={acc:.4f} oov={oov:.4f}")
    return rows


def fold_diffs(r, full):
    """Hiệu từng fold (cùng fold, cấu hình này trừ bộ đầy đủ)."""
    return [a - b for a, b in zip(r["fold_acc"], full["fold_acc"])]


def write(lang, rows, k):
    full = rows[0]["acc"]
    if k > 0:
        where = f"{k}-fold trên train (TB ± độ lệch chuẩn giữa các fold)"
        lines = [f"# Ablation đặc trưng CRF ({lang}), đánh giá bằng {where}", "",
                 "Dev VTB lệch phân phối so với train/test nên tiếng Việt dùng k-fold trên train "
                 "(docs/notes/GHI_CHU.md mục 2). Δ là hiệu trung bình so với bộ đầy đủ trên cùng fold; "
                 "cột cuối đếm số fold mà cấu hình thấp hơn bộ đầy đủ. OOV tính theo phần học của từng fold.", "",
                 "| Kiểu | Bộ đặc trưng | Token acc | Δ so với đầy đủ | OOV acc | Số fold thấp hơn đầy đủ |",
                 "|---|---|---|---|---|---|"]
        for i, r in enumerate(rows):
            below = "-" if i == 0 else f"{sum(d < 0 for d in fold_diffs(r, rows[0]))}/{k}"
            lines.append(f"| {r['kind']} | {r['label']} | {r['acc']:.2%} ± {r['std']:.2%} | "
                         f"{r['acc'] - full:+.2%} | {r['oov']:.2%} | {below} |")
    else:
        lines = [f"# Ablation đặc trưng CRF ({lang}), đánh giá trên dev", "",
                 "| Kiểu | Bộ đặc trưng | Token acc | Δ so với đầy đủ | OOV acc | Số đặc trưng ≠ 0 |",
                 "|---|---|---|---|---|---|"]
        for r in rows:
            lines.append(f"| {r['kind']} | {r['label']} | {r['acc']:.2%} | {r['acc'] - full:+.2%} | "
                         f"{r['oov']:.2%} | {r['n_feat'] if r['n_feat'] is not None else '-'} |")
    out = ROOT / "results" / "tables" / f"ablation_{lang}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    loo = [r for r in rows if r["kind"] == "leave-one-out"][1:]
    cum = [r for r in rows if r["kind"] == "cumulative"] + [rows[0]]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    xerr = [statistics.stdev(fold_diffs(r, rows[0])) * 100 for r in loo] if k > 0 else None
    axes[0].barh([r["label"] for r in loo], [(r["acc"] - full) * 100 for r in loo], xerr=xerr, capsize=3)
    axes[0].set_xlabel("Δ token acc (điểm %) khi bỏ nhóm" + (" (± std hiệu từng fold)" if k > 0 else ""))
    axes[0].axvline(0, color="k", lw=0.8)
    axes[1].plot(range(len(cum)), [r["acc"] * 100 for r in cum], marker="o")
    axes[1].set_xticks(range(len(cum)), ["+" + g for g in ALL_GROUPS], rotation=30)
    axes[1].set_ylabel("token acc (%)")
    axes[1].grid(alpha=0.3)
    fig.suptitle(f"Ablation CRF ({lang}, {f'{k}-fold trên train' if k > 0 else 'dev'})")
    fig.tight_layout()
    fig.savefig(ROOT / "results" / "figures" / f"ablation_{lang}.png", dpi=150)
    plt.close(fig)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--k", type=int, default=None,
                        help=f"0 = dev; mặc định: {CV_K}-fold nếu EVAL_SPLIT của ngôn ngữ là cv, ngược lại dev")
    parser.add_argument("--seed", type=int, default=CV_SEED)
    args = parser.parse_args()
    for lang in args.langs:
        k = args.k if args.k is not None else (CV_K if EVAL_SPLIT[lang] == "cv" else 0)
        print("Đã ghi", write(lang, run(lang, k, args.seed), k).relative_to(ROOT))


if __name__ == "__main__":
    main()
