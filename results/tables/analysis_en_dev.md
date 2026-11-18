# Phân tích lỗi: en (UD_English-EWT), dev

## Token accuracy theo nhóm

| Nhóm | Số token | baseline | hmm | maxent | memm | crf |
|---|---|---|---|---|---|---|
| tất cả | 25,148 | 86.13% | 90.74% | 94.41% | 94.52% | 94.78% |
| OOV | 2,087 | 29.56% | 64.25% | 78.97% | 79.11% | 79.44% |
| trong từ vựng | 23,061 | 91.25% | 93.14% | 95.81% | 95.91% | 96.17% |
| từ mơ hồ | 4,526 | 66.70% | 78.86% | 87.27% | 88.14% | 88.78% |
| câu <=10 từ | 5,549 | 83.89% | 88.70% | 93.75% | 93.93% | 94.22% |
| câu 11-25 từ | 11,713 | 86.63% | 91.13% | 94.66% | 94.69% | 95.01% |
| câu 26-50 từ | 7,182 | 86.93% | 91.76% | 94.76% | 94.92% | 95.07% |
| câu >50 từ | 704 | 87.36% | 89.91% | 91.90% | 92.19% | 92.61% |

## Kiểm định từng cặp (A - B, token accuracy)

| A | B | Hiệu | CI 95% (bootstrap theo câu) | McNemar b / c | p-value |
|---|---|---|---|---|---|
| baseline | hmm | -4.61% | [-5.03%, -4.20%] | 798 / 1957 | 7.3e-108 |
| baseline | maxent | -8.28% | [-8.70%, -7.85%] | 364 / 2447 | 0 |
| baseline | memm | -8.39% | [-8.80%, -7.95%] | 405 / 2514 | 0 |
| baseline | crf | -8.65% | [-9.08%, -8.21%] | 400 / 2576 | 0 |
| hmm | maxent | -3.67% | [-4.01%, -3.32%] | 401 / 1325 | 2.4e-109 |
| hmm | memm | -3.78% | [-4.14%, -3.40%] | 393 / 1343 | 7.8e-115 |
| hmm | crf | -4.04% | [-4.40%, -3.68%] | 346 / 1363 | 2.2e-133 |
| maxent | memm | -0.10% | [-0.28%, +0.06%] | 220 / 246 | 0.25 |
| maxent | crf | -0.37% | [-0.55%, -0.19%] | 236 / 329 | 0.00011 |
| memm | crf | -0.27% | [-0.46%, -0.05%] | 247 / 314 | 0.0053 |

## baseline: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_baseline.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 911 |
| VERB | NOUN | 378 |
| ADJ | NOUN | 239 |
| ADP | PART | 198 |
| NOUN | VERB | 166 |
| SCONJ | ADP | 129 |
| ADV | ADP | 118 |
| VERB | AUX | 114 |
| NUM | NOUN | 109 |
| AUX | VERB | 97 |

## hmm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_hmm.png`

| gold | dự đoán | số lần |
|---|---|---|
| NOUN | PROPN | 228 |
| PROPN | NOUN | 221 |
| VERB | NOUN | 132 |
| ADJ | PROPN | 119 |
| VERB | AUX | 119 |
| NOUN | VERB | 99 |
| NOUN | ADJ | 89 |
| SCONJ | ADP | 78 |
| ADJ | VERB | 74 |
| ADJ | NOUN | 71 |

## maxent: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_maxent.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 200 |
| NOUN | PROPN | 140 |
| VERB | NOUN | 93 |
| SCONJ | ADP | 72 |
| ADV | ADP | 69 |
| NOUN | VERB | 63 |
| ADJ | VERB | 57 |
| ADJ | NOUN | 56 |
| NOUN | ADJ | 49 |
| ADV | ADJ | 38 |

## memm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_memm.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 205 |
| NOUN | PROPN | 136 |
| VERB | NOUN | 102 |
| SCONJ | ADP | 64 |
| ADJ | NOUN | 58 |
| ADJ | VERB | 54 |
| NOUN | VERB | 53 |
| ADV | ADP | 52 |
| NOUN | ADJ | 46 |
| ADV | ADJ | 45 |

## crf: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_crf.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 206 |
| NOUN | PROPN | 126 |
| VERB | NOUN | 84 |
| ADJ | NOUN | 61 |
| ADV | ADP | 60 |
| ADJ | VERB | 54 |
| NOUN | VERB | 54 |
| SCONJ | ADP | 50 |
| NOUN | ADJ | 48 |
| ADV | ADJ | 32 |

## Ví dụ: hmm sai, crf đúng cả câu (5 câu ngắn nhất)

| từ | gold | hmm | crf |
|---|---|---|---|
| Cheers | NOUN | **PROPN** | NOUN |

| từ | gold | hmm | crf |
|---|---|---|---|
| Thx | NOUN | **PROPN** | NOUN |

| từ | gold | hmm | crf |
|---|---|---|---|
| 4105SF | NOUN | **NUM** | NOUN |

| từ | gold | hmm | crf |
|---|---|---|---|
| ************************************************ | PUNCT | **SYM** | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| ************************************************ | PUNCT | **SYM** | PUNCT |


## Ví dụ: crf sai, hmm đúng cả câu (5 câu ngắn nhất)

| từ | gold | crf | hmm |
|---|---|---|---|
| GT | PROPN | **NOUN** | PROPN |

| từ | gold | crf | hmm |
|---|---|---|---|
| Visit | PROPN | **NOUN** | PROPN |

| từ | gold | crf | hmm |
|---|---|---|---|
| PIRAMAR | PROPN | **NOUN** | PROPN |

| từ | gold | crf | hmm |
|---|---|---|---|
| Visit | PROPN | **NOUN** | PROPN |
| , | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| \\ | SYM | **PUNCT** | SYM |
| // | SYM | **PUNCT** | SYM |

