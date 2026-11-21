"""Huấn luyện các mô hình cuối cùng trên TOÀN BỘ tập train với tham số đã chốt, rồi lưu ra models/.

Tham số lấy từ configs/best_params.json (giống hệt scripts/run_experiments.py), nên mô hình được lưu
chính là mô hình đã cho ra kết quả trong báo cáo. Sau khi lưu, script tải lại file và chấm trên dev để
kiểm tra; tập test KHÔNG được dùng.

Ví dụ:
    python scripts/train_final.py                         # mọi mô hình chính, vi + en
    python scripts/train_final.py --langs vi --models hmm crf

Đầu ra:
    models/{lang}_{model}.joblib     mô hình + metadata (src/model_io.py)
    models/manifest.json             tham số, accuracy dev, kích thước, SHA-256 của từng file
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.run_experiments import load_params  # noqa: E402
from src.data import TREEBANKS, load, vocabulary  # noqa: E402
from src.evaluate import evaluate  # noqa: E402
from src.model_io import load_model, save_model  # noqa: E402

MAIN_MODELS = ["baseline", "hmm", "maxent", "memm", "crf"]
OUT_DIR = ROOT / "models"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--models", nargs="+", default=MAIN_MODELS)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    manifest_path = args.out / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}

    for lang in args.langs:
        train, dev = load(lang, "train"), load(lang, "dev")
        vocab = vocabulary(train)
        for name in args.models:
            cls, params = load_params(lang, name)
            start = time.perf_counter()
            model = cls(**params).fit(train)
            fit_time = time.perf_counter() - start

            path = args.out / f"{lang}_{name}.joblib"
            save_model(model, path, lang=lang, name=name, params=params,
                       treebank=TREEBANKS[lang][0], n_train_sentences=len(train))

            loaded, _ = load_model(path)  # kiểm tra file đọc lại được và cho cùng kết quả
            dev_acc = evaluate(loaded, dev, vocab)["token_acc"]
            manifest[f"{lang}_{name}"] = {
                "file": path.name, "params": params, "dev_token_acc": round(dev_acc, 4),
                "fit_time_s": round(fit_time, 1), "size_mb": round(path.stat().st_size / 2**20, 2),
                "sha256": sha256(path),
            }
            print(f"[{lang}] {name:8s} dev acc {dev_acc:.2%}  {manifest[f'{lang}_{name}']['size_mb']} MB  -> {path.name}")
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Đã ghi {manifest_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
