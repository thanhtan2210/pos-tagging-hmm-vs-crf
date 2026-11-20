# results/figures

| Hình | RQ | Lệnh tạo |
|---|---|---|
| learning_curve_{lang}.png | RQ1 (vi: 5-fold trên train, en: dev) | `python scripts/learning_curve.py` |
| confusion_vi_{model}_cv.png | RQ2, tiếng Việt (out-of-fold) | `python scripts/analyze.py --split cv --langs vi` |
| confusion_{lang}_{model}.png | RQ2, trên dev | `python scripts/analyze.py` |
| ablation_{lang}.png | RQ3 (vi: 5-fold trên train, en: dev) | `python scripts/ablation.py` |
| ga_vi.png | RQ3 (GA) | `python -m src.ga --lang vi` |
