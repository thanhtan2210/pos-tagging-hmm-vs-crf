# results/tables

Bảng kết quả cuối, được commit để người xem không cần chạy lại.

| Bảng | Nội dung | Lệnh tạo |
|---|---|---|
| results_dev.md | Mọi mô hình trên dev, kèm tham số | `python scripts/run_experiments.py` |
| tune_{lang}_{model}.md | Grid search k-fold trên train | `python scripts/tune.py` |
| learning_curve.csv | RQ1: điểm theo frac × seed | `python scripts/learning_curve.py` |
| analysis_{lang}_dev.md | RQ2/RQ4: acc theo nhóm token, độ dài câu, kiểm định cặp, cặp nhầm | `python scripts/analyze.py` |
| ablation_{lang}.md | RQ3: ablation nhóm đặc trưng CRF | `python scripts/ablation.py` |
| ga_vi.md | GA chọn nhóm đặc trưng | `python -m src.ga --lang vi` |
