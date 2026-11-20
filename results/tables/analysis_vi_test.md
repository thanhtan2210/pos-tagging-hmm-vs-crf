# Phân tích lỗi: vi (UD_Vietnamese-VTB), test

## Token accuracy theo nhóm

| Nhóm | Số token | baseline | hmm | maxent | memm | crf |
|---|---|---|---|---|---|---|
| tất cả | 11,692 | 82.33% | 83.55% | 87.87% | 88.06% | 88.34% |
| OOV | 1,747 | 34.29% | 49.46% | 66.46% | 66.40% | 67.60% |
| trong từ vựng | 9,945 | 90.77% | 89.54% | 91.63% | 91.87% | 91.99% |
| từ mơ hồ | 2,051 | 67.77% | 72.55% | 73.87% | 75.38% | 76.01% |
| nhiều âm tiết | 2,079 | 66.09% | 66.57% | 78.98% | 79.37% | 79.17% |
| ngữ pháp hóa | 422 | 54.98% | 69.91% | 68.96% | 72.51% | 73.46% |
| câu <=10 từ | 1,655 | 81.99% | 82.11% | 87.19% | 86.40% | 86.83% |
| câu 11-25 từ | 10,037 | 82.39% | 83.79% | 87.98% | 88.33% | 88.59% |
| câu 26-50 từ | 0 | nan% | nan% | nan% | nan% | nan% |
| câu >50 từ | 0 | nan% | nan% | nan% | nan% | nan% |

## Kiểm định từng cặp (A - B, token accuracy)

| A | B | Hiệu | CI 95% (bootstrap theo câu) | McNemar b / c | p-value |
|---|---|---|---|---|---|
| baseline | hmm | -1.22% | [-1.88%, -0.54%] | 701 / 844 | 0.0003 |
| baseline | maxent | -5.54% | [-6.11%, -4.94%] | 274 / 922 | 4.2e-78 |
| baseline | memm | -5.73% | [-6.33%, -5.12%] | 288 / 958 | 4.2e-80 |
| baseline | crf | -6.01% | [-6.64%, -5.38%] | 311 / 1014 | 7.1e-83 |
| hmm | maxent | -4.32% | [-4.89%, -3.69%] | 423 / 928 | 8.6e-43 |
| hmm | memm | -4.51% | [-5.07%, -3.88%] | 371 / 898 | 2.4e-49 |
| hmm | crf | -4.79% | [-5.35%, -4.21%] | 353 / 913 | 1.3e-55 |
| maxent | memm | -0.19% | [-0.49%, +0.11%] | 147 / 169 | 0.24 |
| maxent | crf | -0.47% | [-0.83%, -0.11%] | 166 / 221 | 0.0061 |
| memm | crf | -0.28% | [-0.60%, +0.04%] | 164 / 197 | 0.092 |

## baseline: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_baseline_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 526 |
| PROPN | NOUN | 348 |
| ADJ | NOUN | 243 |
| VERB | ADP | 94 |
| ADP | VERB | 64 |
| ADV | VERB | 59 |
| ADV | AUX | 50 |
| NUM | NOUN | 42 |
| ADJ | ADP | 39 |
| PRON | NOUN | 38 |

## hmm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_hmm_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| NOUN | VERB | 247 |
| VERB | NOUN | 240 |
| ADJ | VERB | 147 |
| ADJ | NOUN | 117 |
| NOUN | ADJ | 111 |
| VERB | ADJ | 100 |
| PROPN | NOUN | 87 |
| VERB | ADP | 68 |
| NOUN | PROPN | 61 |
| ADV | VERB | 59 |

## maxent: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_maxent_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 175 |
| ADJ | NOUN | 141 |
| NOUN | VERB | 128 |
| ADJ | VERB | 98 |
| PROPN | NOUN | 89 |
| VERB | ADP | 70 |
| ADV | VERB | 64 |
| VERB | ADJ | 43 |
| ADP | VERB | 40 |
| PRON | NOUN | 36 |

## memm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_memm_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 168 |
| ADJ | NOUN | 146 |
| NOUN | VERB | 137 |
| ADJ | VERB | 100 |
| PROPN | NOUN | 96 |
| ADV | VERB | 58 |
| VERB | ADP | 56 |
| VERB | ADJ | 42 |
| PRON | NOUN | 38 |
| ADP | VERB | 37 |

## crf: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_crf_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 163 |
| NOUN | VERB | 131 |
| ADJ | NOUN | 125 |
| ADJ | VERB | 105 |
| PROPN | NOUN | 87 |
| VERB | ADP | 59 |
| ADV | VERB | 58 |
| VERB | ADJ | 46 |
| NOUN | ADJ | 38 |
| ADP | VERB | 34 |

## Ví dụ: hmm sai, crf đúng cả câu (5 câu ngắn nhất)

| từ | gold | hmm | crf |
|---|---|---|---|
| Nhận | VERB | **NOUN** | VERB |
| vợ | NOUN | NOUN | NOUN |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Kẻ | NOUN | **PROPN** | NOUN |
| khủng bố | VERB | VERB | VERB |
| xuất hiện | VERB | VERB | VERB |
| ! | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Hùng | PROPN | PROPN | PROPN |
| chờ | VERB | VERB | VERB |
| phản ứng | VERB | **ADJ** | VERB |
| ... | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Đất | NOUN | NOUN | NOUN |
| nóng | ADJ | **NOUN** | ADJ |
| Nhơn Trạch | PROPN | PROPN | PROPN |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Mũ bảo hiểm | NOUN | **PROPN** | NOUN |
| ... | PUNCT | PUNCT | PUNCT |
| 19 . 000 | NUM | NUM | NUM |
| đồng | NOUN | NOUN | NOUN |
| . | PUNCT | PUNCT | PUNCT |


## Ví dụ: crf sai, hmm đúng cả câu (5 câu ngắn nhất)

| từ | gold | crf | hmm |
|---|---|---|---|
| Thọ | PROPN | **NOUN** | PROPN |
| về | VERB | VERB | VERB |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Thọ | PROPN | **NOUN** | PROPN |
| quá | ADV | ADV | ADV |
| sốt ruột | VERB | VERB | VERB |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Thời gian | NOUN | NOUN | NOUN |
| đàm thoại | VERB | **NOUN** | VERB |
| 4 | NUM | NUM | NUM |
| giây | NOUN | NOUN | NOUN |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Những | DET | DET | DET |
| mẩu | NOUN | NOUN | NOUN |
| tin | NOUN | **VERB** | NOUN |
| quái ác | ADJ | **NOUN** | ADJ |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Bữa | NOUN | NOUN | NOUN |
| cơm | NOUN | NOUN | NOUN |
| kết thúc | VERB | VERB | VERB |
| chóng vánh | ADJ | **NOUN** | ADJ |
| . | PUNCT | PUNCT | PUNCT |

