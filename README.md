# Mô hình sinh và mô hình phân biệt trong gán nhãn từ loại

So sánh **HMM** (mô hình sinh), **MaxEnt / MEMM** và **CRF** (mô hình phân biệt) cho bài toán gán nhãn từ loại (POS tagging) trên tiếng Việt và tiếng Anh, dùng dữ liệu [Universal Dependencies](https://universaldependencies.org/) với bộ nhãn UPOS (17 nhãn).

Bài tập lớn môn Học máy (CO3117), HK261, Trường ĐH Bách Khoa – ĐHQG-HCM.

## Câu hỏi nghiên cứu

| | Câu hỏi | Thí nghiệm |
|---|---|---|
| RQ1 | Lượng dữ liệu huấn luyện ảnh hưởng thế nào đến mô hình sinh và mô hình phân biệt? (Ng & Jordan, 2002) | Learning curve trên 5% → 100% tập train |
| RQ2 | Mô hình nào xử lý từ chưa gặp (OOV) tốt hơn, và vì sao? | Accuracy riêng trên token OOV; các cách xử lý UNK của HMM |
| RQ3 | Đặc trưng nào có ích, và có phụ thuộc ngôn ngữ không? | Ablation nhóm đặc trưng CRF trên tiếng Việt và tiếng Anh |
| RQ4 | Mô hình hóa cả chuỗi có hơn phân loại từng từ không? | MaxEnt từng từ vs MEMM vs CRF (vấn đề label bias) |

## Dữ liệu

| Ngôn ngữ | Treebank |
|---|---|
| Tiếng Việt | [UD_Vietnamese-VTB](https://github.com/UniversalDependencies/UD_Vietnamese-VTB) |
| Tiếng Anh | [UD_English-EWT](https://github.com/UniversalDependencies/UD_English-EWT) |

Dữ liệu không nằm trong repo; tải bằng `scripts/download_data.py` (bản dùng trong project: nhánh `master` của UD, tải ngày 24/10/2026). Tập **test chỉ được dùng một lần** ở cuối dự án, mọi lựa chọn mô hình và tham số làm trên tập dev.

## Cấu trúc

```
src/
  data.py         đọc file CoNLL-U
  baseline.py     baseline: nhãn phổ biến nhất của mỗi từ
  hmm.py          HMM bigram + Viterbi (tự cài đặt bằng numpy)
  evaluate.py     token acc, OOV acc, macro-F1, sentence acc
scripts/
  download_data.py
  eda.py          thống kê dữ liệu -> results/eda.md
  run_experiments.py
tests/            kiểm thử (Viterbi so với vét cạn, đọc CoNLL-U, ...)
docs/             kế hoạch, ghi chú
```

## Cài đặt và chạy

Yêu cầu Python 3.11.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows; Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

python scripts/download_data.py
python -m pytest
python scripts/eda.py
python scripts/run_experiments.py
```
