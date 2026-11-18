"""RQ3: ablation nhóm đặc trưng CRF trên vi và en.

Hai kiểu:
    leave-one-out : bộ đầy đủ bỏ đi đúng một nhóm -> nhóm nào mất đi làm tụt điểm nhiều nhất
    cumulative    : bắt đầu từ "word", thêm lần lượt từng nhóm theo thứ tự cố định
c1/c2 giữ cố định theo configs/best_params.json để chỉ có bộ đặc trưng thay đổi.
Mặc định đánh giá trên dev; --k > 0 thì dùng k-fold trên train để có thêm sai số.

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
from src.model_selection import cross_val_score  # noqa: E402


def configs():
    yield "leave-one-out", "đầy đủ", ALL_GROUPS
    for g in ALL_GROUPS:
        yield "leave-one-out", f"- {g}", tuple(x for x in ALL_GROUPS if x != g)
    for n in range(1, len(ALL_GROUPS)):  # bộ dài nhất (n = len) trùng "đầy đủ"
        yield "cumulative", " + ".join(ALL_GROUPS[:n]), ALL_GROUPS[:n]


def run(lang, k, seed):
    train, dev = load(lang, "train"), load(lang, "dev")
    vocab = vocabulary(train)
    _, params = load_params(lang, "crf")
    rows = []
    for kind, label, groups in configs():
        p = {**params, "groups": groups}
        if k > 0:
            scores = cross_val_score(CRFTagger, p, train, k=k, seed=seed)
            acc, std, oov = statistics.mean(scores), statistics.stdev(scores), float("nan")
            n_feat = None
        else:
            model = CRFTagger(**p).fit(train)
            records, _ = predict_all(model, dev)
            m = metrics(records, vocab)
            acc, std, oov, n_feat = m["token_acc"], 0.0, m["oov_acc"], model.n_active_features()
        rows.append({"kind": kind, "label": label, "acc": acc, "std": std, "oov": oov, "n_feat": n_feat})
        print(f"[{lang}] {kind:13s} {label:45s} acc={acc:.4f} oov={oov:.4f}")
    return rows


def write(lang, rows, k):
    full = rows[0]["acc"]
    where = f"{k}-fold trên train (TB ± std)" if k > 0 else "dev"
    lines = [f"# Ablation đặc trưng CRF ({lang}), đánh giá trên {where}", "",
             "| Kiểu | Bộ đặc trưng | Token acc | Δ so với đầy đủ | OOV acc | Số đặc trưng ≠ 0 |",
             "|---|---|---|---|---|---|"]
    for r in rows:
        acc = f"{r['acc']:.2%}" + (f" ± {r['std']:.2%}" if k > 0 else "")
        lines.append(f"| {r['kind']} | {r['label']} | {acc} | {r['acc'] - full:+.2%} | "
                     f"{r['oov']:.2%} | {r['n_feat'] if r['n_feat'] is not None else '-'} |")
    out = ROOT / "results" / "tables" / f"ablation_{lang}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    loo = [r for r in rows if r["kind"] == "leave-one-out"][1:]
    cum = [r for r in rows if r["kind"] == "cumulative"] + [rows[0]]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].barh([r["label"] for r in loo], [(r["acc"] - full) * 100 for r in loo])
    axes[0].set_xlabel("Δ token acc (điểm %) khi bỏ nhóm")
    axes[0].axvline(0, color="k", lw=0.8)
    axes[1].plot(range(len(cum)), [r["acc"] * 100 for r in cum], marker="o")
    axes[1].set_xticks(range(len(cum)), ["+" + g for g in ALL_GROUPS], rotation=30)
    axes[1].set_ylabel("token acc (%)")
    axes[1].grid(alpha=0.3)
    fig.suptitle(f"Ablation CRF ({lang})")
    fig.tight_layout()
    fig.savefig(ROOT / "results" / "figures" / f"ablation_{lang}.png", dpi=150)
    plt.close(fig)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--k", type=int, default=0, help="0 = đánh giá trên dev")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    for lang in args.langs:
        print("Đã ghi", write(lang, run(lang, args.k, args.seed), args.k).relative_to(ROOT))


if __name__ == "__main__":
    main()
