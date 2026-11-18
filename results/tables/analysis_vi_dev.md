# Phân tích lỗi: vi (UD_Vietnamese-VTB), dev

## Token accuracy theo nhóm

| Nhóm | Số token | baseline | hmm | crf |
|---|---|---|---|---|
| tất cả | 26,162 | 81.29% | 80.95% | 85.62% |
| OOV | 4,829 | 43.74% | 50.26% | 63.78% |
| trong từ vựng | 21,333 | 89.80% | 87.90% | 90.56% |
| từ mơ hồ | 4,469 | 64.69% | 68.72% | 71.22% |
| nhiều âm tiết | 5,497 | 67.49% | 66.25% | 77.92% |
| ngữ pháp hóa | 1,156 | 63.41% | 71.19% | 79.67% |
| câu <=10 từ | 749 | 83.31% | 79.17% | 86.65% |
| câu 11-25 từ | 12,104 | 81.96% | 81.63% | 86.24% |
| câu 26-50 từ | 10,973 | 80.94% | 80.52% | 85.34% |
| câu >50 từ | 2,336 | 78.90% | 79.97% | 83.43% |

## Kiểm định từng cặp (A - B, token accuracy)

| A | B | Hiệu | CI 95% (bootstrap theo câu) | McNemar b / c | p-value |
|---|---|---|---|---|---|
| baseline | hmm | +0.34% | [-0.15%, +0.83%] | 2031 / 1941 | 0.16 |
| baseline | crf | -4.33% | [-4.78%, -3.87%] | 1172 / 2304 | 5.1e-82 |
| hmm | crf | -4.67% | [-5.09%, -4.24%] | 920 / 2142 | 6.8e-108 |

## baseline: 10 cặp nhầm nhiều nhất (gold -> dự đoán)

Ma trận nhầm lẫn chuẩn hóa theo hàng: `results/figures/confusion_vi_baseline.png`

| gold | dự đoán | số lần |
|---|---|---|
| VERB | NOUN | 1122 |
| PROPN | NOUN | 795 |
| ADJ | NOUN | 523 |
| VERB | ADV | 238 |
| VERB | ADP | 229 |
| NUM | NOUN | 210 |
| PUNCT | NOUN | 167 |
| NOUN | ADP | 150 |
| ADJ | ADV | 128 |
| ADV | AUX | 118 |

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

