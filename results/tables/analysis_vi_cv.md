# Phân tích lỗi: vi (UD_Vietnamese-VTB), 5-fold trên train (dự đoán out-of-fold)

Mỗi câu train được gán nhãn bởi mô hình học trên các fold còn lại. OOV và từ mơ hồ tính theo phần học của fold chứa câu đó; accuracy theo nhóm gộp token của mọi fold. Nhóm không có token nào thì bỏ qua.

## Token accuracy theo nhóm

| Nhóm | Số token | baseline | hmm | maxent | memm | crf |
|---|---|---|---|---|---|---|
| tất cả | 20,215 | 86.07% | 85.15% | 90.37% | 90.60% | 90.45% |
| OOV | 2,405 | 38.00% | 48.65% | 66.15% | 67.69% | 67.32% |
| trong từ vựng | 17,810 | 92.56% | 90.08% | 93.64% | 93.69% | 93.58% |
| gặp đúng 1 lần trong train | 1,325 | 91.02% | 49.21% | 87.25% | 86.49% | 87.02% |
| từ mơ hồ | 3,266 | 69.63% | 73.33% | 77.43% | 78.57% | 78.20% |
| nhiều âm tiết | 4,535 | 74.97% | 71.22% | 83.20% | 83.70% | 83.20% |
| ngữ pháp hóa | 827 | 60.58% | 71.46% | 76.18% | 79.93% | 79.81% |
| câu <=10 từ | 3,007 | 86.30% | 84.50% | 90.79% | 90.89% | 90.85% |
| câu 11-25 từ | 17,208 | 86.03% | 85.27% | 90.30% | 90.55% | 90.38% |

## Kiểm định từng cặp (A - B, token accuracy)

| A | B | Hiệu | CI 95% (bootstrap theo câu) | McNemar b / c | p-value |
|---|---|---|---|---|---|
| baseline | hmm | +0.92% | [+0.40%, +1.40%] | 1271 / 1086 | 0.00015 |
| baseline | maxent | -4.30% | [-4.68%, -3.91%] | 420 / 1289 | 7e-98 |
| baseline | memm | -4.53% | [-4.90%, -4.12%] | 461 / 1376 | 6.6e-101 |
| baseline | crf | -4.38% | [-4.83%, -3.96%] | 536 / 1422 | 5.5e-89 |
| hmm | maxent | -5.21% | [-5.68%, -4.71%] | 560 / 1614 | 6.2e-113 |
| hmm | memm | -5.44% | [-5.90%, -4.98%] | 488 / 1588 | 1.5e-128 |
| hmm | crf | -5.30% | [-5.79%, -4.80%] | 532 / 1603 | 1.2e-118 |
| maxent | memm | -0.23% | [-0.45%, -0.01%] | 233 / 279 | 0.047 |
| maxent | crf | -0.08% | [-0.32%, +0.15%] | 294 / 311 | 0.52 |
| memm | crf | +0.14% | [-0.09%, +0.36%] | 276 / 247 | 0.22 |

## baseline: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_baseline_cv.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 805 |
| ADJ | NOUN | 376 |
| PROPN | NOUN | 222 |
| VERB | ADP | 193 |
| NUM | NOUN | 101 |
| ADV | VERB | 87 |
| ADP | VERB | 74 |
| VERB | ADV | 71 |
| ADV | AUX | 66 |
| NOUN | VERB | 66 |

## hmm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_hmm_cv.png`

| gold | dự đoán | số lần |
|---|---|---|
| NOUN | VERB | 420 |
| VERB | NOUN | 394 |
| ADJ | VERB | 219 |
| ADJ | NOUN | 189 |
| NOUN | ADJ | 160 |
| NOUN | PROPN | 148 |
| VERB | ADJ | 135 |
| VERB | ADP | 115 |
| ADV | VERB | 106 |
| PROPN | NOUN | 98 |

## maxent: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_maxent_cv.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 270 |
| ADJ | NOUN | 196 |
| NOUN | VERB | 180 |
| ADJ | VERB | 142 |
| VERB | ADP | 106 |
| ADV | VERB | 95 |
| PROPN | NOUN | 86 |
| NOUN | ADJ | 65 |
| VERB | ADJ | 54 |
| ADP | VERB | 53 |

## memm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_memm_cv.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 251 |
| ADJ | NOUN | 187 |
| NOUN | VERB | 182 |
| ADJ | VERB | 156 |
| VERB | ADP | 93 |
| PROPN | NOUN | 85 |
| ADV | VERB | 80 |
| ADP | VERB | 61 |
| VERB | ADJ | 60 |
| NOUN | ADJ | 57 |

## crf: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_crf_cv.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 267 |
| NOUN | VERB | 199 |
| ADJ | NOUN | 183 |
| ADJ | VERB | 145 |
| VERB | ADP | 88 |
| ADV | VERB | 83 |
| PROPN | NOUN | 74 |
| NOUN | ADJ | 72 |
| VERB | ADJ | 67 |
| ADP | VERB | 52 |

## Ví dụ: hmm sai, crf đúng cả câu (5 câu ngắn nhất)

| từ | gold | hmm | crf |
|---|---|---|---|
| Tiếp cận | VERB | **PROPN** | VERB |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Vì sao | X | **PROPN** | X |
| ? | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Nữ sinh | NOUN | **PROPN** | NOUN |
| mất tích | VERB | VERB | VERB |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Tháo | VERB | **NOUN** | VERB |
| ngòi nổ | NOUN | **ADJ** | NOUN |
| ... | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Lửa | NOUN | **PROPN** | NOUN |
| hận | VERB | VERB | VERB |
| . | PUNCT | PUNCT | PUNCT |


## Ví dụ: crf sai, hmm đúng cả câu (5 câu ngắn nhất)

| từ | gold | crf | hmm |
|---|---|---|---|
| Chàng | NOUN | NOUN | NOUN |
| thám tử | NOUN | NOUN | NOUN |
| thư sinh | ADJ | **NOUN** | ADJ |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Nhóm | NOUN | NOUN | NOUN |
| Hiểm họa | NOUN | **PROPN** | NOUN |
| khó | ADJ | ADJ | ADJ |
| tránh | VERB | VERB | VERB |
| ! | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Công ty | NOUN | NOUN | NOUN |
| không | ADV | ADV | ADV |
| ai | PRON | PRON | PRON |
| dòm ngó | VERB | **NOUN** | VERB |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Người | NOUN | NOUN | NOUN |
| lao động | NOUN | **VERB** | NOUN |
| cũng | ADV | ADV | ADV |
| vậy | PRON | PRON | PRON |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Cả | PRON | **PART** | PRON |
| trạm | NOUN | NOUN | NOUN |
| 20 | NUM | NUM | NUM |
| bị | AUX | AUX | AUX |
| khám xét | VERB | VERB | VERB |
| . | PUNCT | PUNCT | PUNCT |

