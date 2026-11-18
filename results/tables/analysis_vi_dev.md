# Phân tích lỗi: vi (UD_Vietnamese-VTB), dev

## Token accuracy theo nhóm

| Nhóm | Số token | hmm | maxent | memm | crf |
|---|---|---|---|---|---|
| tất cả | 26,162 | 80.95% | 85.53% | 85.74% | 85.62% |
| OOV | 4,829 | 50.26% | 63.57% | 64.15% | 63.78% |
| trong từ vựng | 21,333 | 87.90% | 90.50% | 90.63% | 90.56% |
| từ mơ hồ | 4,469 | 68.72% | 69.70% | 71.07% | 71.22% |
| nhiều âm tiết | 5,497 | 66.25% | 77.90% | 77.92% | 77.92% |
| ngữ pháp hóa | 1,156 | 71.19% | 76.21% | 78.46% | 79.67% |
| câu <=10 từ | 749 | 79.17% | 86.52% | 86.78% | 86.65% |
| câu 11-25 từ | 12,104 | 81.63% | 86.00% | 86.12% | 86.24% |
| câu 26-50 từ | 10,973 | 80.52% | 85.25% | 85.58% | 85.34% |
| câu >50 từ | 2,336 | 79.97% | 84.12% | 84.20% | 83.43% |

## Kiểm định từng cặp (A - B, token accuracy)

| A | B | Hiệu | CI 95% (bootstrap theo câu) | McNemar b / c | p-value |
|---|---|---|---|---|---|
| hmm | maxent | -4.58% | [-5.00%, -4.14%] | 1033 / 2232 | 1.3e-97 |
| hmm | memm | -4.79% | [-5.19%, -4.38%] | 890 / 2144 | 1.5e-114 |
| hmm | crf | -4.67% | [-5.09%, -4.24%] | 920 / 2142 | 6.8e-108 |
| maxent | memm | -0.21% | [-0.42%, +0.00%] | 404 / 459 | 0.066 |
| maxent | crf | -0.09% | [-0.33%, +0.15%] | 499 / 522 | 0.49 |
| memm | crf | +0.12% | [-0.10%, +0.35%] | 442 / 410 | 0.29 |

## hmm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_hmm.png`

| gold | dự đoán | số lần |
|---|---|---|
| NOUN | VERB | 869 |
| VERB | NOUN | 528 |
| ADJ | VERB | 306 |
| NOUN | PROPN | 291 |
| PROPN | NOUN | 273 |
| NOUN | ADJ | 265 |
| ADJ | NOUN | 225 |
| VERB | ADV | 214 |
| VERB | ADP | 213 |
| PUNCT | NOUN | 158 |

## maxent: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_maxent.png`

| gold | dự đoán | số lần |
|---|---|---|
| NOUN | VERB | 460 |
| VERB | NOUN | 399 |
| ADJ | NOUN | 244 |
| ADJ | VERB | 232 |
| NOUN | PROPN | 228 |
| VERB | ADP | 203 |
| PROPN | NOUN | 200 |
| VERB | ADV | 185 |
| PUNCT | NOUN | 147 |
| NOUN | ADP | 133 |

## memm: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_memm.png`

| gold | dự đoán | số lần |
|---|---|---|
| NOUN | VERB | 452 |
| VERB | NOUN | 416 |
| ADJ | VERB | 244 |
| ADJ | NOUN | 235 |
| NOUN | PROPN | 219 |
| VERB | ADV | 215 |
| PROPN | NOUN | 203 |
| VERB | ADP | 184 |
| NOUN | ADP | 124 |
| ADJ | ADV | 110 |

## crf: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_crf.png`

| gold | dự đoán | số lần |
|---|---|---|
| NOUN | VERB | 463 |
| VERB | NOUN | 393 |
| ADJ | VERB | 236 |
| VERB | ADV | 226 |
| NOUN | PROPN | 221 |
| ADJ | NOUN | 214 |
| PROPN | NOUN | 213 |
| VERB | ADP | 166 |
| NOUN | ADP | 129 |
| NOUN | ADJ | 126 |

## Ví dụ: hmm sai, crf đúng cả câu (5 câu ngắn nhất)

| từ | gold | hmm | crf |
|---|---|---|---|
| Ở | ADP | **NOUN** | ADP |
| đâu | PRON | PRON | PRON |
| ? | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Lại | ADV | **PROPN** | ADV |
| giam | VERB | VERB | VERB |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Thổ chu | PROPN | PROPN | PROPN |
| rất | ADV | ADV | ADV |
| nhiều | ADJ | ADJ | ADJ |
| đồi mồi | NOUN | **VERB** | NOUN |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Hai | NUM | NUM | NUM |
| lần | NOUN | NOUN | NOUN |
| bà | NOUN | NOUN | NOUN |
| bỏ trốn | VERB | **ADJ** | VERB |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | hmm | crf |
|---|---|---|---|
| Vậy là | SCONJ | **NOUN** | SCONJ |
| chúng tôi | PRON | PRON | PRON |
| lại | ADV | ADV | ADV |
| ra | VERB | **ADV** | VERB |
| đi | VERB | VERB | VERB |
| ... | PUNCT | PUNCT | PUNCT |


## Ví dụ: crf sai, hmm đúng cả câu (5 câu ngắn nhất)

| từ | gold | crf | hmm |
|---|---|---|---|
| Hàm răng | NOUN | NOUN | NOUN |
| tôi | PRON | PRON | PRON |
| cũng | ADV | ADV | ADV |
| đánh | VERB | VERB | VERB |
| lập cập | ADJ | **VERB** | ADJ |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Cô | NOUN | NOUN | NOUN |
| gái | NOUN | NOUN | NOUN |
| Việt | PROPN | PROPN | PROPN |
| bên | ADP | **NOUN** | ADP |
| dòng | NOUN | NOUN | NOUN |
| sông | NOUN | NOUN | NOUN |
| Chao Phraya | PROPN | PROPN | PROPN |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Mẹ | NOUN | NOUN | NOUN |
| cô | NOUN | NOUN | NOUN |
| không | ADV | ADV | ADV |
| cảm thấy | VERB | VERB | VERB |
| Zaosheng | NOUN | **PROPN** | NOUN |
| là | AUX | AUX | AUX |
| nhà | NOUN | NOUN | NOUN |
| của | ADP | ADP | ADP |
| mình | PRON | PRON | PRON |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Bà | NOUN | NOUN | NOUN |
| thậm chí | ADV | ADV | ADV |
| còn | ADV | ADV | ADV |
| trồng | VERB | VERB | VERB |
| cải bắp | NOUN | **VERB** | NOUN |
| cho | ADP | ADP | ADP |
| những | DET | DET | DET |
| người | NOUN | NOUN | NOUN |
| hàng xóm | NOUN | NOUN | NOUN |
| . | PUNCT | PUNCT | PUNCT |

| từ | gold | crf | hmm |
|---|---|---|---|
| Nghe | VERB | VERB | VERB |
| báo cáo | VERB | **NOUN** | VERB |
| có | VERB | VERB | VERB |
| các | DET | DET | DET |
| anh | NOUN | NOUN | NOUN |
| Ba Bường | PROPN | PROPN | PROPN |
| , | PUNCT | PUNCT | PUNCT |
| Ba Hương | PROPN | PROPN | PROPN |
| , | PUNCT | PUNCT | PUNCT |
| Mười Thơ | PROPN | PROPN | PROPN |
| , | PUNCT | PUNCT | PUNCT |
| Vũ Đình Liệu | PROPN | PROPN | PROPN |
| . | PUNCT | PUNCT | PUNCT |

