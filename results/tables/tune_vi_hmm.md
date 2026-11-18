# Grid search hmm (vi), 3-fold trên train, seed=42

| alpha | unk | token_acc (mean) | std |
|---|---|---|---|
| 0.01 | signature | 0.8439 | 0.0030 |
| 0.1 | signature | 0.8437 | 0.0018 |
| 0.001 | signature | 0.8436 | 0.0032 |
| 0.1 | rare | 0.8350 | 0.0019 |
| 0.01 | rare | 0.8343 | 0.0028 |
| 0.001 | rare | 0.8341 | 0.0018 |
| 0.1 | add-alpha | 0.8317 | 0.0034 |
| 1.0 | signature | 0.8288 | 0.0035 |
| 0.01 | add-alpha | 0.8255 | 0.0049 |
| 0.001 | add-alpha | 0.8216 | 0.0051 |
| 1.0 | rare | 0.8169 | 0.0052 |
| 1.0 | add-alpha | 0.8113 | 0.0047 |
