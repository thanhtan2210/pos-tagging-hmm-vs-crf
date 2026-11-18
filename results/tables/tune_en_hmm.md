# Grid search hmm (en), 3-fold trên train, seed=42

| alpha | unk | token_acc (mean) | std |
|---|---|---|---|
| 0.001 | signature | 0.9215 | 0.0011 |
| 0.01 | signature | 0.9212 | 0.0013 |
| 0.1 | signature | 0.9172 | 0.0014 |
| 0.001 | rare | 0.9047 | 0.0008 |
| 0.01 | rare | 0.9045 | 0.0010 |
| 0.001 | add-alpha | 0.9026 | 0.0019 |
| 0.1 | rare | 0.9012 | 0.0011 |
| 0.01 | add-alpha | 0.9007 | 0.0019 |
| 0.1 | add-alpha | 0.8991 | 0.0006 |
| 1.0 | signature | 0.8859 | 0.0008 |
| 1.0 | rare | 0.8681 | 0.0008 |
| 1.0 | add-alpha | 0.8599 | 0.0003 |
