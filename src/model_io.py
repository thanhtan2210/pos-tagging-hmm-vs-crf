"""Lưu và tải mô hình đã huấn luyện.

Mỗi file .joblib chứa một dict: mô hình (đối tượng tagger có fit/predict) kèm thông tin để biết nó
được tạo ra thế nào (ngôn ngữ, tên, tham số, số câu train, phiên bản thư viện). Nhờ vậy, khi tải lên
có thể kiểm tra đúng mô hình đã cho ra kết quả trong báo cáo.

Chỉ tải file .joblib từ nguồn tin cậy: joblib dùng pickle, có thể chạy code tùy ý khi tải.
"""

import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy
import sklearn

FORMAT_VERSION = 1


def save_model(model, path, **meta):
    """Ghi mô hình và metadata ra `path` (tự tạo thư mục). Trả về metadata đã ghi."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {
        **meta,
        "format_version": FORMAT_VERSION,
        "class": type(model).__name__,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "numpy": numpy.__version__,
        "scikit_learn": sklearn.__version__,
    }
    joblib.dump({"model": model, "meta": meta}, path, compress=3)
    return meta


def load_model(path):
    """Trả về (model, meta). Model dùng được ngay: model.predict(words)."""
    obj = joblib.load(path)
    if not isinstance(obj, dict) or "model" not in obj:
        raise ValueError(f"{path} không phải file mô hình của project")
    if obj["meta"].get("format_version") != FORMAT_VERSION:
        raise ValueError(f"{path}: format_version {obj['meta'].get('format_version')} không được hỗ trợ")
    return obj["model"], obj["meta"]
