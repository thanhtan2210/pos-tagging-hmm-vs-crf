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

Dữ liệu không nằm trong repo; tải bằng `scripts/download_data.py` (bản dùng trong project: nhánh `master` của UD, tải ngày 24/10/2026). Tập **test chỉ được dùng một lần** ở cuối dự án; mọi lựa chọn tham số làm bằng k-fold trên train, và các mô hình
được so sánh trên 5-fold trên train (tiếng Việt) hoặc dev (tiếng Anh).

## Kết quả (giai đoạn phát triển)

Mọi tham số được chọn bằng 3-fold trên **train** (`scripts/tune.py`); tập test chỉ dùng một lần ở cuối.
Các mô hình được so sánh bằng **5-fold trên train với tiếng Việt** và **trên dev với tiếng Anh**. Dev của VTB lệch
phân phối so với train và test: 1/3 số câu dài hơn 25 từ, trong khi train và test không có câu nào như vậy
([docs/notes/GHI_CHU.md](docs/notes/GHI_CHU.md), mục 2). Dev VTB đầy đủ chỉ còn dùng cho thí nghiệm phụ về độ dài câu
([analysis_vi_dev.md](results/tables/analysis_vi_dev.md)).
Bảng đầy đủ: [results_cv.md](results/tables/results_cv.md) (vi), [results_dev.md](results/tables/results_dev.md).

| Mô hình | vi token acc (CV) | vi OOV acc (CV) | en token acc (dev) | en OOV acc (dev) |
|---|---|---|---|---|
| Baseline nhãn phổ biến nhất | 86.07% | 37.96% | 86.13% | 29.56% |
| HMM (add-α, một UNK chung) | 83.62% | 13.25% | 87.47% | 25.68% |
| HMM (UNK theo hình thái, đã tune) | 85.15% | 48.61% | 90.74% | 64.25% |
| MaxEnt (từng từ) | 90.37% | 66.14% | 94.41% | 78.97% |
| MEMM | 90.60% | 67.65% | 94.52% | 79.11% |
| **CRF** | **90.45%** | **67.28%** | **94.78%** | **79.44%** |

Số tiếng Việt là trung bình 5 fold (độ lệch chuẩn giữa các fold 0,6–0,9 điểm). Chúng cao hơn accuracy trên dev hay
test vì câu của cùng một bài báo có thể nằm ở cả hai phía của một fold, nên chỉ so các mô hình trong cùng một cột.

Phát hiện chính:

- **RQ1**: CRF thắng HMM ở *mọi* lượng dữ liệu, kể cả 5% train (với tiếng Việt: ở mọi fold); không thấy điểm giao nhau
  như Ng & Jordan dự đoán. Với tiếng Việt, khoảng cách thu hẹp từ 11,4 điểm ở 5% train xuống 5,3 điểm ở 100%
  ([learning_curve_vi.png](results/figures/learning_curve_vi.png), [learning_curve_en.png](results/figures/learning_curve_en.png)).
- **RQ2**: cách xử lý OOV quyết định HMM: lớp UNK theo hình thái nâng OOV acc từ 13% lên 49% (vi) và 26% lên 64% (en).
  CRF vẫn hơn HMM 19 điểm (vi) và 15 điểm (en) trên OOV nhờ đặc trưng tiền/hậu tố và hình thái. Trên tiếng Việt, HMM
  đã tune **thua** baseline 0,92 điểm (p < 0,001). Phần thua đến từ các từ chỉ gặp một lần trong train: HMM thay
  chúng bằng lớp UNK khi học, nên chỉ gán đúng 49% số từ này, còn baseline đúng 91%. Trên từ OOV và từ mơ hồ, HMM
  vẫn hơn baseline ([analysis_vi_cv.md](results/tables/analysis_vi_cv.md)).
- **RQ3**: tiếng Việt: bỏ bất kỳ nhóm nào trừ ngữ cảnh ±2 đều làm accuracy giảm, ở cả 5/5 fold. Giảm nhiều nhất khi bỏ
  ngữ cảnh ±1 (−0,61), tiền/hậu tố (−0,52) và shape (−0,43); ba mức này cách nhau dưới 0,2 điểm nên thứ tự giữa chúng
  không chắc chắn. Dev VTB từng cho thấy shape quan trọng nhất và tiền/hậu tố gần như vô ích. Tiếng Anh: *ngữ cảnh ±1*
  và *tiền/hậu tố*. Ngữ cảnh ±2 không giúp ở cả hai ngôn ngữ; GA cũng tự bỏ nhóm này
  ([ablation_vi.md](results/tables/ablation_vi.md), [ablation_en.md](results/tables/ablation_en.md),
  [ga_vi.md](results/tables/ga_vi.md)).
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
