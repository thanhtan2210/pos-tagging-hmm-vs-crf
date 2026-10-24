"""Huấn luyện và đánh giá các mô hình trên từng ngôn ngữ.

Ví dụ:
    python scripts/run_experiments.py                      # đánh giá trên dev
    python scripts/run_experiments.py --models baseline    # chỉ chạy baseline
    python scripts/run_experiments.py --split test         # CHỈ chạy một lần ở cuối dự án
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.baseline import MostFrequentTagger  # noqa: E402
from src.data import TREEBANKS, load, vocabulary  # noqa: E402
from src.evaluate import evaluate  # noqa: E402
from src.hmm import HMMTagger  # noqa: E402

MODELS = {
    "baseline": MostFrequentTagger,
    "hmm": HMMTagger,
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định không in được tiếng Việt
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--models", nargs="+", default=list(MODELS))
    parser.add_argument("--split", default="dev", choices=["dev", "test"])
    args = parser.parse_args()

    rows = []
    for lang in args.langs:
        train, evalset = load(lang, "train"), load(lang, args.split)
        train_vocab = vocabulary(train)
        for name in args.models:
            try:
                start = time.perf_counter()
                model = MODELS[name]().fit(train)
                fit_time = time.perf_counter() - start
                m = evaluate(model, evalset, train_vocab)
            except NotImplementedError as e:
                print(f"[{lang}] {name}: bỏ qua, chưa cài đặt ({e})")
                continue
            print(f"\n[{lang}] {name}\n{m.pop('report')}")
            rows.append({"lang": lang, "model": name, "split": args.split,
                         "fit_time_s": fit_time, **m})

    if not rows:
        return
    header = "| Ngôn ngữ | Mô hình | Token acc | OOV acc | Macro-F1 | Sent acc | Fit (s) | Predict (s) |"
    print("\n" + header + "\n" + "|---" * 8 + "|")
    for r in rows:
        print(f"| {r['lang']} | {r['model']} | {r['token_acc']:.2%} | {r['oov_acc']:.2%} | "
              f"{r['macro_f1']:.3f} | {r['sent_acc']:.2%} | {r['fit_time_s']:.2f} | {r['predict_time_s']:.2f} |")

    out = ROOT / "results" / f"results_{args.split}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nĐã ghi {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
