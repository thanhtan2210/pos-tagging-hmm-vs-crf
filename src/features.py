"""Các nhóm đặc trưng (có tên) cho CRF / MaxEnt / MEMM, phục vụ ablation (RQ3) và GA.

Mỗi nhóm là một hàm (words, i) -> dict, và mọi khóa của nhóm đều có tiền tố
"<tên nhóm>:". Vì vậy bỏ/thêm một nhóm chỉ xóa/thêm đúng các khóa của nhóm đó,
các nhóm khác giữ nguyên (ablation có kiểm soát).
"""

# - [x] FEATURE_GROUPS = {tên_nhóm: hàm(words, i) -> dict đặc trưng}
# - [x] word2features(words, i, groups): gộp dict của các nhóm được chọn
# - [x] đảm bảo bỏ/thêm một nhóm không làm thay đổi các nhóm khác


def _word(words, i):
    w = words[i]
    return {"word.lower": w.lower()}


def _affix(words, i):
    w = words[i].lower()
    f = {}
    for k in (1, 2, 3, 4):
        if len(w) >= k:
            f[f"pre{k}"] = w[:k]
            f[f"suf{k}"] = w[-k:]
    return f


def _shape(words, i):
    w = words[i]
    return {
        "is_title": w[:1].isupper(),
        "is_upper": w.isupper(),
        "has_digit": any(c.isdigit() for c in w),
        "is_digit": w.isdigit(),
        "has_hyphen": "-" in w,
        "is_punct": not any(c.isalnum() for c in w),
        "is_first": i == 0,
        "is_last": i == len(words) - 1,
    }


def _context(words, i, offsets):
    f = {}
    for d in offsets:
        j = i + d
        f[f"w[{d:+d}]"] = words[j].lower() if 0 <= j < len(words) else ("<BOS>" if j < 0 else "<EOS>")
    return f


def _context1(words, i):
    f = _context(words, i, (-1, 1))
    if i > 0:
        f["w[-1]|w"] = words[i - 1].lower() + "|" + words[i].lower()
    return f


def _context2(words, i):
    return _context(words, i, (-2, 2))


def _syllable(words, i):
    """Riêng tiếng Việt: trong UD VTB một từ có thể gồm nhiều âm tiết cách nhau bởi dấu cách."""
    syl = words[i].lower().split(" ")
    return {"n_syl": min(len(syl), 4), "syl_first": syl[0], "syl_last": syl[-1]}


FEATURE_GROUPS = {
    "word": _word,
    "affix": _affix,
    "shape": _shape,
    "context1": _context1,
    "context2": _context2,
    "syllable": _syllable,
}
ALL_GROUPS = tuple(FEATURE_GROUPS)


def word2features(words, i, groups=ALL_GROUPS):
    f = {"bias": 1.0}
    for g in groups:
        for k, v in FEATURE_GROUPS[g](words, i).items():
            f[f"{g}:{k}"] = v
    return f


def sent2features(words, groups=ALL_GROUPS):
    return [word2features(words, i, groups) for i in range(len(words))]
