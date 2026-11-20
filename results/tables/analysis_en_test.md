# Phân tích lỗi: en (UD_English-EWT), test

## Token accuracy theo nhóm

| Nhóm | Số token | baseline | hmm | maxent | memm | crf |
|---|---|---|---|---|---|---|
| tất cả | 25,094 | 86.20% | 91.18% | 94.62% | 94.72% | 94.92% |
| OOV | 2,292 | 30.80% | 64.35% | 78.75% | 79.19% | 80.32% |
| trong từ vựng | 22,802 | 91.77% | 93.87% | 96.21% | 96.28% | 96.39% |
| từ mơ hồ | 4,427 | 67.86% | 81.16% | 88.64% | 89.36% | 89.99% |
| câu <=10 từ | 5,874 | 82.79% | 88.41% | 93.29% | 93.68% | 93.60% |
| câu 11-25 từ | 11,306 | 87.48% | 92.21% | 95.39% | 95.27% | 95.64% |
| câu 26-50 từ | 6,940 | 86.89% | 91.76% | 94.44% | 94.64% | 94.86% |
| câu >50 từ | 974 | 87.06% | 91.79% | 94.87% | 95.07% | 95.07% |

## Kiểm định từng cặp (A - B, token accuracy)

| A | B | Hiệu | CI 95% (bootstrap theo câu) | McNemar b / c | p-value |
|---|---|---|---|---|---|
| baseline | hmm | -4.98% | [-5.49%, -4.43%] | 800 / 2049 | 6.6e-121 |
| baseline | maxent | -8.42% | [-8.93%, -7.90%] | 400 / 2512 | 0 |
| baseline | memm | -8.52% | [-9.01%, -8.00%] | 420 / 2557 | 0 |
| baseline | crf | -8.72% | [-9.25%, -8.21%] | 439 / 2628 | 0 |
| hmm | maxent | -3.44% | [-3.79%, -3.08%] | 394 / 1257 | 7e-100 |
| hmm | memm | -3.54% | [-3.89%, -3.16%] | 378 / 1266 | 4.4e-106 |
| hmm | crf | -3.75% | [-4.10%, -3.39%] | 323 / 1263 | 6.4e-123 |
| maxent | memm | -0.10% | [-0.25%, +0.07%] | 198 / 223 | 0.24 |
| maxent | crf | -0.31% | [-0.49%, -0.12%] | 217 / 294 | 0.00077 |
| memm | crf | -0.21% | [-0.38%, -0.02%] | 210 / 262 | 0.019 |

## baseline: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_baseline_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 970 |
| VERB | NOUN | 334 |
| ADJ | NOUN | 223 |
| ADP | PART | 209 |
| NUM | NOUN | 208 |
| SCONJ | ADP | 128 |
| NOUN | VERB | 127 |
| AUX | VERB | 100 |
| PRON | SCONJ | 95 |
| VERB | AUX | 95 |

## hmm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_hmm_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 259 |
| NOUN | PROPN | 248 |
| VERB | AUX | 106 |
| VERB | NOUN | 99 |
| ADJ | PROPN | 99 |
| NOUN | ADJ | 97 |
| NOUN | VERB | 89 |
| ADJ | VERB | 69 |
| ADJ | NOUN | 68 |
| SCONJ | ADP | 65 |

## maxent: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_maxent_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 224 |
| NOUN | PROPN | 174 |
| VERB | NOUN | 69 |
| SCONJ | ADP | 64 |
| ADJ | NOUN | 57 |
| NOUN | VERB | 48 |
| ADJ | VERB | 46 |
| NOUN | ADJ | 43 |
| ADV | ADP | 41 |
| ADV | ADJ | 38 |

## memm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_memm_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 229 |
| NOUN | PROPN | 176 |
| VERB | NOUN | 69 |
| SCONJ | ADP | 62 |
| ADJ | NOUN | 57 |
| NOUN | VERB | 45 |
| ADV | ADJ | 40 |
| NOUN | ADJ | 40 |
| ADV | ADP | 38 |
| ADJ | VERB | 37 |

## crf: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_en_crf_test.png`

| gold | dự đoán | số lần |
|---|---|---|
| PROPN | NOUN | 211 |
| NOUN | PROPN | 184 |
| VERB | NOUN | 65 |
| ADJ | NOUN | 58 |
| SCONJ | ADP | 50 |
| NOUN | VERB | 45 |
| ADJ | VERB | 42 |
| NOUN | ADJ | 41 |
| ADV | ADJ | 37 |
| ADV | ADP | 37 |

## Ví dụ: hmm sai, crf đúng cả câu (5 câu ngắn nhất)

| từ | gold | hmm | crf |
|---|---|---|---|
| M | PROPN | **NUM** | PROPN |

| từ | gold | hmm | crf |
|---|---|---|---|
| ------------------------------ | PUNCT | **SYM** | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| http://www.theadvocate.com/sports/story.asp?StoryID=16473 | PROPN | **NUM** | PROPN |

| từ | gold | hmm | crf |
|---|---|---|---|
| http://www.theadvocate.com/sports/story.asp?StoryID=16475 | PROPN | **NUM** | PROPN |

| từ | gold | hmm | crf |
|---|---|---|---|
| http://www.nola.com/lsu/t-p/football/index.ssf?/lsustory/lsunotes08.html | PROPN | **NUM** | PROPN |


## Ví dụ: crf sai, hmm đúng cả câu (5 câu ngắn nhất)

| từ | gold | crf | hmm |
|---|---|---|---|
| Move-Team@ENRON | PROPN | **X** | PROPN |

| từ | gold | crf | hmm |
|---|---|---|---|
| good | ADJ | **INTJ** | ADJ |

| từ | gold | crf | hmm |
|---|---|---|---|
| Relish | PROPN | **ADJ** | PROPN |

| từ | gold | crf | hmm |
|---|---|---|---|
| Clint | PROPN | **NOUN** | PROPN |
| : | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Fudruckers | PROPN | **NOUN** | PROPN |
| . | PUNCT | PUNCT | PUNCT |

