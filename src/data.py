"""Đọc dữ liệu Universal Dependencies (định dạng CoNLL-U)."""
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# mã ngôn ngữ -> (thư mục treebank, tiền tố tên file)
TREEBANKS = {
    "vi": ("UD_Vietnamese-VTB", "vi_vtb"),
    "en": ("UD_English-EWT", "en_ewt"),
}


def read_conllu(path):
    """Trả về list các câu, mỗi câu là (words, tags) với tags là nhãn UPOS.

    Bỏ qua dòng chú thích (#), token gộp (id dạng 1-2, vd. "don't") và
    nút rỗng (id dạng 8.1), chỉ giữ các từ cú pháp có id nguyên.
    """
    sentences, words, tags = [], [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                if words:
                    sentences.append((words, tags))
                    words, tags = [], []
                continue
            if line.startswith("#"):
                continue
            cols = line.split("\t")
            if "-" in cols[0] or "." in cols[0]:
                continue
            words.append(cols[1])
            tags.append(cols[3])
    if words:
        sentences.append((words, tags))
    return sentences


def load(lang, split):
    """Đọc một tập (train/dev/test) của treebank ứng với ngôn ngữ `lang`."""
    folder, prefix = TREEBANKS[lang]
    return read_conllu(DATA_DIR / folder / f"{prefix}-ud-{split}.conllu")


def vocabulary(sentences):
    return {w for words, _ in sentences for w in words}
