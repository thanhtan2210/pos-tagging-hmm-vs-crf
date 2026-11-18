# Mô hình sinh và mô hình phân biệt trong gán nhãn từ loại

So sánh **HMM** (mô hình sinh), **MaxEnt / MEMM** và **CRF** (mô hình phân biệt) cho bài toán gán nhãn từ loại (POS tagging) trên tiếng Việt và tiếng Anh, dùng dữ liệu [Universal Dependencies](https://universaldependencies.org/) với bộ nhãn UPOS (17 nhãn).

Bài tập lớn môn Học máy (CO3117), HK261, Trường ĐH Bách Khoa – ĐHQG-HCM. English: [README.md](README.md).

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

## Kết quả (tập dev)

Mọi tham số được chọn bằng 3-fold trên **train** (`scripts/tune.py`); tập test chỉ dùng một lần ở cuối.
Bảng đầy đủ: [results/tables/results_dev.md](results/tables/results_dev.md).

| Mô hình | vi token acc | vi OOV acc | en token acc | en OOV acc |
|---|---|---|---|---|
| Baseline nhãn phổ biến nhất | 81.29% | 43.74% | 86.13% | 29.56% |
| HMM (add-α, một UNK chung) | 76.12% | 13.23% | 87.47% | 25.68% |
| HMM (UNK theo hình thái, đã tune) | 80.95% | 50.26% | 90.74% | 64.25% |
| MaxEnt (từng từ) | 85.53% | 63.57% | 94.41% | 78.97% |
| MEMM | 85.74% | 64.15% | 94.52% | 79.11% |
| **CRF** | **85.62%** | **63.78%** | **94.78%** | **79.44%** |

Phát hiện chính:

- **RQ1**: CRF thắng HMM ở *mọi* lượng dữ liệu, kể cả 5% train; không thấy điểm giao nhau như Ng & Jordan
  dự đoán ([learning_curve_vi.png](results/figures/learning_curve_vi.png), [learning_curve_en.png](results/figures/learning_curve_en.png)).
- **RQ2**: cách xử lý OOV quyết định HMM: lớp UNK theo hình thái nâng OOV acc từ 13% lên 50% (vi) và 26% lên 64% (en).
  Mô hình phân biệt vẫn hơn ~14 điểm trên OOV nhờ đặc trưng tiền/hậu tố và hình thái. Trên tiếng Việt, HMM
  không hơn baseline có ý nghĩa thống kê (CI bootstrap chứa 0), xem [analysis_vi_dev.md](results/tables/analysis_vi_dev.md).
- **RQ3**: nhóm có ích nhất: *shape* và *ngữ cảnh ±1* (vi); *ngữ cảnh ±1* và *tiền/hậu tố* (en). Ngữ cảnh ±2 không giúp
  ở cả hai ngôn ngữ; GA cũng tự bỏ nhóm này ([ablation_vi.md](results/tables/ablation_vi.md),
  [ablation_en.md](results/tables/ablation_en.md), [ga_vi.md](results/tables/ga_vi.md)).
- **RQ4**: cùng bộ đặc trưng, MaxEnt, MEMM và CRF chênh nhau dưới 0.4 điểm; bộ đặc trưng quan trọng hơn nhiều so với
  việc mô hình hóa chuỗi trên dữ liệu này.

## Cấu trúc

```
src/
  data.py             đọc CoNLL-U
  baseline.py         baseline nhãn phổ biến nhất
  hmm.py              HMM bigram + Viterbi (numpy), các chiến lược UNK
  features.py         nhóm đặc trưng có tên cho CRF/MaxEnt
  crf.py              CRF (sklearn-crfsuite)
  memm.py             MaxEnt và MEMM (+ Viterbi)
  evaluate.py         predict_all / metrics(mask) / lưu-đọc dự đoán
  model_selection.py  k-fold theo câu, grid search, lấy tập con
  stats.py            paired bootstrap, McNemar
  ga.py               thuật toán di truyền chọn nhóm đặc trưng
scripts/              download_data, eda, tune, run_experiments, learning_curve, analyze, ablation
configs/              best_params.json (sinh bởi tune.py)
results/tables, results/figures   bảng và hình cuối (được commit)
tests/                pytest (không cần dữ liệu UD)
docs/notes/           kế hoạch, ghi chú
```

## Cài đặt và chạy

Yêu cầu Python 3.11.

```bash
python -m venv .venv
.venv\Scriptsctivate          # Windows; Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

make all          # dữ liệu, test, EDA, tune, kết quả dev, learning curve, ablation, phân tích
make final        # đánh giá trên TEST — chỉ chạy MỘT lần
```

Không có `make` (Windows): chạy lần lượt các lệnh trong [Makefile](Makefile).
Docker: `docker build -t pos-tagging . && docker run --rm -v "$PWD/results:/app/results" pos-tagging`.

## License

Code: MIT ([LICENSE](LICENSE)). Dữ liệu UD có license riêng.
