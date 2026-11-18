"""Huấn luyện và đánh giá các mô hình trên từng ngôn ngữ.

Ví dụ:
    python scripts/run_experiments.py                      # đánh giá trên dev
    python scripts/run_experiments.py --models baseline    # chỉ chạy baseline
    python scripts/run_experiments.py --split test         # CHỈ chạy một lần ở cuối dự án
"""

# - [x] (mục 2) params đọc từ configs/best_params.json theo (lang, model)
# - [x] (mục 4) đăng ký "crf" (và các biến thể HMM/baseline) vào MODELS
# - [x] (mục 0) dùng predict_all + metrics; lưu records vào results/preds/
# - [x] (mục 2) khi --split test: in cảnh báo và yêu cầu xác nhận (chỉ chạy một lần)
# - [x] (mục 8) tham số --seed (mặc định 42), lưu params + seed kèm kết quả
# - [x] (mục 9) ghi bảng Markdown vào results/tables/

import argparse
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.baseline import MostFrequentTagger  # noqa: E402
from src.crf import CRFTagger  # noqa: E402
from src.data import TREEBANKS, load, vocabulary  # noqa: E402
from src.evaluate import metrics, predict_all, save_records  # noqa: E402
from src.hmm import HMMTagger  # noqa: E402

CONFIG = ROOT / "configs" / "best_params.json"

# tên -> (lớp, khóa trong best_params.json hoặc None, tham số cố định ghi đè config)
MODELS = {
    "baseline": (MostFrequentTagger, None, {}),
    "baseline-sig": (MostFrequentTagger, None, {"oov": "signature"}),
    "hmm": (HMMTagger, "hmm", {}),  # alpha + unk theo k-fold
    "hmm-addalpha": (HMMTagger, "hmm", {"unk": "add-alpha"}),  # cùng alpha, chỉ đổi UNK (RQ2)
    "hmm-rare": (HMMTagger, "hmm", {"unk": "rare"}),
    "hmm-sig": (HMMTagger, "hmm", {"unk": "signature"}),
    "crf": (CRFTagger, "crf", {}),
}


def load_params(lang, name):
    cls, key, fixed = MODELS[name]
    config = json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
    tuned = config.get(lang, {}).get(key, {}) if key else {}
    params = {k: v for k, v in tuned.items() if not k.startswith("_")}
    if key and not params:
        print(f"[{lang}] {name}: CẢNH BÁO chưa có tham số trong {CONFIG.name}, dùng mặc định "
              "(chạy scripts/tune.py trước)")
    return cls, {**params, **fixed}


def confirm_test_split(yes):
    print("CẢNH BÁO: đánh giá trên TẬP TEST. Chỉ làm MỘT LẦN, sau khi đã chốt mọi lựa chọn trên train/dev.")
    if yes:
        return True
    if not sys.stdin.isatty():
        print("Không có terminal để xác nhận; thêm --yes nếu chắc chắn.")
        return False
    return input("Gõ 'test' để tiếp tục: ").strip() == "test"


def write_markdown(rows, split, seed):
    lines = [f"# Kết quả trên {split} (seed={seed})", "",
             "| Ngôn ngữ | Mô hình | Token acc | OOV acc | Macro-F1 | Sent acc | Fit (s) | Predict (s) | Tham số |",
             "|---" * 9 + "|"]
    for r in rows:
        lines.append(
            f"| {r['lang']} | {r['model']} | {r['token_acc']:.2%} | {r['oov_acc']:.2%} | "
            f"{r['macro_f1']:.3f} | {r['sent_acc']:.2%} | {r['fit_time_s']:.2f} | {r['predict_time_s']:.2f} | "
            f"{json.dumps(r['params'], ensure_ascii=False)} |")
    text = "\n".join(lines) + "\n"
    out = ROOT / "results" / "tables" / f"results_{split}.md"
    out.write_text(text, encoding="utf-8")
    return text, out


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định không in được tiếng Việt
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--models", nargs="+", default=list(MODELS), choices=list(MODELS))
    parser.add_argument("--split", default="dev", choices=["dev", "test"])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--yes", action="store_true", help="bỏ qua xác nhận khi --split test")
    args = parser.parse_args()
    if args.split == "test" and not confirm_test_split(args.yes):
        return
    random.seed(args.seed)
    np.random.seed(args.seed)

    rows = []
    for lang in args.langs:
        train, evalset = load(lang, "train"), load(lang, args.split)
        train_vocab = vocabulary(train)
        for name in args.models:
            cls, params = load_params(lang, name)
            start = time.perf_counter()
            model = cls(**params).fit(train)
            fit_time = time.perf_counter() - start
            records, predict_time = predict_all(model, evalset)
            save_records(records, ROOT / "results" / "preds" / f"{lang}_{name}_{args.split}.jsonl")
            m = metrics(records, train_vocab)
            m["predict_time_s"] = predict_time
            print(f"\n[{lang}] {name} {params}\n{m.pop('report')}")
            rows.append({"lang": lang, "model": name, "split": args.split, "seed": args.seed,
                         "params": params, "fit_time_s": fit_time, **m})

    text, md = write_markdown(rows, args.split, args.seed)
    print("\n" + text)
    out = ROOT / "results" / f"results_{args.split}.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Đã ghi {out.relative_to(ROOT)} và {md.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
