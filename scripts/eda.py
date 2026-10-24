"""Thống kê mô tả dữ liệu cho phần "Dữ liệu & thách thức" của báo cáo.

Ghi kết quả ra results/eda.md. Chỉ dùng train và dev; tập test để dành cho
lần đánh giá cuối cùng.
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.data import TREEBANKS, load, vocabulary  # noqa: E402


def describe(lang):
    train, dev = load(lang, "train"), load(lang, "dev")
    tokens = [(w, t) for words, tags in train for w, t in zip(words, tags)]
    tag_counts = Counter(t for _, t in tokens)
    tags_of_word = defaultdict(Counter)
    for w, t in tokens:
        tags_of_word[w][t] += 1
    word_counts = Counter(w for w, _ in tokens)
    train_vocab = vocabulary(train)
    dev_tokens = [w for words, _ in dev for w in words]
    lengths = sorted(len(words) for words, _ in train)

    lines = [
        f"## {lang} ({TREEBANKS[lang][0]})",
        "",
        "| Thống kê | Giá trị |",
        "|---|---|",
        f"| Số câu train / dev | {len(train):,} / {len(dev):,} |",
        f"| Số token train | {len(tokens):,} |",
        f"| Số từ khác nhau (train) | {len(train_vocab):,} |",
        f"| Độ dài câu train: trung bình / trung vị / max | "
        f"{len(tokens) / len(train):.1f} / {lengths[len(lengths) // 2]} / {lengths[-1]} |",
        f"| Số nhãn UPOS | {len(tag_counts)} |",
        f"| Từ chỉ xuất hiện 1 lần (hapax) / tổng số từ khác nhau | "
        f"{sum(c == 1 for c in word_counts.values()) / len(word_counts):.1%} |",
        f"| Token không mang nhãn đa số của từ đó (lỗi tối thiểu nếu chỉ tra từ điển) | "
        f"{sum(c.total() - c.most_common(1)[0][1] for c in tags_of_word.values()) / len(tokens):.1%} |",
        f"| Tỷ lệ token OOV trên dev | "
        f"{sum(w not in train_vocab for w in dev_tokens) / len(dev_tokens):.1%} |",
        f"| Token chứa dấu cách (từ nhiều âm tiết) | "
        f"{sum(' ' in w for w, _ in tokens) / len(tokens):.1%} |",
        "",
        "Phân bố nhãn (train):",
        "",
        "| Nhãn | Số token | Tỷ lệ |",
        "|---|---|---|",
    ]
    for tag, c in tag_counts.most_common():
        lines.append(f"| {tag} | {c:,} | {c / len(tokens):.1%} |")

    # Xếp theo số token KHÔNG mang nhãn đa số: đây là những từ mà ngữ cảnh thực sự
    # cần để gán đúng. Xếp theo số nhãn khác nhau sẽ bị nhiễu nhãn chi phối
    # (vd. "the" có vài lần bị gán nhầm PRON).
    ambiguous = sorted(
        tags_of_word,
        key=lambda w: -(word_counts[w] - tags_of_word[w].most_common(1)[0][1]),
    )[:15]
    lines += ["", "Các từ mơ hồ nhất (theo số token không mang nhãn đa số):", ""]
    lines += [
        f"- `{w}`: " + ", ".join(f"{t} {c}" for t, c in tags_of_word[w].most_common(4))
        for w in ambiguous
    ]

    # Chỉ dùng độ dài câu (không dùng nhãn) của cả 3 tập để kiểm tra lệch phân phối.
    lines += ["", "Độ dài câu theo từng tập:", "",
              "| Tập | Số câu | Trung bình | Max | Tỷ lệ câu > 25 từ |", "|---|---|---|---|---|"]
    for split in ("train", "dev", "test"):
        lens = [len(words) for words, _ in load(lang, split)]
        lines.append(f"| {split} | {len(lens):,} | {sum(lens) / len(lens):.1f} | {max(lens)} | "
                     f"{sum(n > 25 for n in lens) / len(lens):.1%} |")
    return "\n".join(lines)


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định không in được tiếng Việt
    out = ROOT / "results" / "eda.md"
    out.parent.mkdir(exist_ok=True)
    text = "# Thống kê dữ liệu\n\n" + "\n\n".join(describe(lang) for lang in TREEBANKS)
    out.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"\nĐã ghi {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
