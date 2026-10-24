"""Tải các treebank Universal Dependencies dùng trong project vào data/.

Mặc định lấy nhánh `master` (bản phát hành mới nhất của UD). Để tái hiện đúng
kết quả trong báo cáo, dùng --ref với tag phát hành đã ghi trong README, vd. --ref r2.15
"""
import argparse
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.data import DATA_DIR, TREEBANKS  # noqa: E402

URL = "https://raw.githubusercontent.com/UniversalDependencies/{folder}/{ref}/{prefix}-ud-{split}.conllu"


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định không in được tiếng Việt
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", nargs="+", default=list(TREEBANKS))
    parser.add_argument("--ref", default="master")
    args = parser.parse_args()

    for lang in args.langs:
        folder, prefix = TREEBANKS[lang]
        (DATA_DIR / folder).mkdir(parents=True, exist_ok=True)
        for split in ("train", "dev", "test"):
            dest = DATA_DIR / folder / f"{prefix}-ud-{split}.conllu"
            if dest.exists():
                print(f"đã có  {dest.relative_to(DATA_DIR.parent)}")
                continue
            url = URL.format(folder=folder, ref=args.ref, prefix=prefix, split=split)
            urllib.request.urlretrieve(url, dest)
            print(f"đã tải {dest.relative_to(DATA_DIR.parent)} ({dest.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
