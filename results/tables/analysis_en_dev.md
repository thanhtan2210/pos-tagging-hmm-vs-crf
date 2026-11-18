# Phân tích lỗi: en (UD_English-EWT), dev

## Token accuracy theo nhóm

| Nhóm | Số token | baseline | hmm | crf |
|---|---|---|---|---|
| tất cả | 25,148 | 86.13% | 90.74% | 94.78% |
| OOV | 2,087 | 29.56% | 64.25% | 79.44% |
| trong từ vựng | 23,061 | 91.25% | 93.14% | 96.17% |
| từ mơ hồ | 4,526 | 66.70% | 78.86% | 88.78% |
| câu <=10 từ | 5,549 | 83.89% | 88.70% | 94.22% |
| câu 11-25 từ | 11,713 | 86.63% | 91.13% | 95.01% |
| câu 26-50 từ | 7,182 | 86.93% | 91.76% | 95.07% |
| câu >50 từ | 704 | 87.36% | 89.91% | 92.61% |

## Kiểm định từng cặp (A - B, token accuracy)

| A | B | Hiệu | CI 95% (bootstrap theo câu) | McNemar b / c | p-value |
|---|---|---|---|---|---|
| baseline | hmm | -4.61% | [-5.03%, -4.20%] | 798 / 1957 | 7.3e-108 |
| baseline | crf | -8.65% | [-9.08%, -8.21%] | 400 / 2576 | 0 |
| hmm | crf | -4.04% | [-4.40%, -3.68%] | 346 / 1363 | 2.2e-133 |

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

