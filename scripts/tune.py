"""Chọn tham số bằng k-fold trên train, ghi ra configs/best_params.json.

Ví dụ:
    python scripts/tune.py                       # mọi ngôn ngữ, HMM + CRF
    python scripts/tune.py --models hmm --k 5
    python scripts/tune.py --langs en --models crf --k 3
"""

# - [x] lưới HMM: alpha x chiến lược UNK
# - [x] lưới CRF: c1 x c2
# - [x] với mỗi ngôn ngữ: grid_search(...) -> lưu best_params + bảng điểm vào results/tables/
# - [x] tham số dòng lệnh --seed, --k

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.crf import CRFTagger  # noqa: E402
from src.data import TREEBANKS, load  # noqa: E402
from src.hmm import HMMTagger  # noqa: E402
from src.model_selection import grid_search  # noqa: E402

CONFIG = ROOT / "configs" / "best_params.json"
GRIDS = {
    "hmm": (HMMTagger, {"alpha": [0.001, 0.01, 0.1, 1.0], "unk": ["add-alpha", "rare", "signature"]}),
    "crf": (CRFTagger, {"c1": [0.0, 0.05, 0.25], "c2": [0.01, 0.1]}),
}


def write_table(lang, name, grid, table, k, seed):
    keys = list(grid)
    lines = [f"# Grid search {name} ({lang}), {k}-fold trên train, seed={seed}", "",
             "| " + " | ".join(keys) + " | token_acc (mean) | std |",
             "|" + "---|" * (len(keys) + 2)]
    for r in sorted(table, key=lambda r: -r["mean"]):
        lines.append("| " + " | ".join(str(r[x]) for x in keys) + f" | {r['mean']:.4f} | {r['std']:.4f} |")
    out = ROOT / "results" / "tables" / f"tune_{lang}_{name}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--models", nargs="+", default=list(GRIDS), choices=list(GRIDS))
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
    config.pop("_todo", None)
    config["_note"] = "Sinh tự động bởi scripts/tune.py (k-fold trên train). Không sửa tay theo kết quả dev."
    for lang in args.langs:
        train = load(lang, "train")
        for name in args.models:
            cls, grid = GRIDS[name]
            print(f"[{lang}] {name}: {args.k}-fold")
            best, table = grid_search(
                cls, grid, train, k=args.k, seed=args.seed,
                log=lambda r: print(f"   {({x: r[x] for x in grid})} -> {r['mean']:.4f} ± {r['std']:.4f}"))
            print(f"   => tốt nhất: {best}")
            config.setdefault(lang, {})[name] = {**best, "_cv": {"k": args.k, "seed": args.seed}}
            write_table(lang, name, grid, table, args.k, args.seed)
            CONFIG.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Đã ghi {CONFIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
