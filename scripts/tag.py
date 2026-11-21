"""Gán nhãn từ loại cho câu bằng một mô hình đã lưu (không cần huấn luyện lại).

Đầu vào là câu ĐÃ TÁCH TỪ, các từ cách nhau bởi dấu cách. Với tiếng Việt, nối các âm tiết của
một từ bằng dấu gạch dưới: "học_sinh" được hiểu là từ "học sinh" (đúng cách VTB tách từ).

Ví dụ:
    python scripts/tag.py --model models/vi_crf.joblib "Tôi là học_sinh ."
    python scripts/tag.py --model models/en_hmm.joblib "I want to book a flight ."
    python scripts/tag.py --model models/en_crf.joblib --file input.txt   # mỗi dòng một câu
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.model_io import load_model  # noqa: E402


def tokenize(line):
    return [w.replace("_", " ") for w in line.split()]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("sentence", nargs="?", help="câu đã tách từ; bỏ trống nếu dùng --file")
    parser.add_argument("--file", type=Path, help="file văn bản, mỗi dòng một câu đã tách từ")
    args = parser.parse_args()
    if not args.sentence and not args.file:
        parser.error("cần một câu hoặc --file")

    model, meta = load_model(args.model)
    print(f"# {meta['name']} ({meta['lang']}), tham số {meta['params']}", file=sys.stderr)
    lines = args.file.read_text(encoding="utf-8").splitlines() if args.file else [args.sentence]
    for line in lines:
        words = tokenize(line)
        if words:
            print(" ".join(f"{w.replace(' ', '_')}/{t}" for w, t in zip(words, model.predict(words))))


if __name__ == "__main__":
    main()
