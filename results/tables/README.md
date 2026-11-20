# results/tables

Bảng kết quả cuối, được commit để người xem không cần chạy lại.

Tiếng Việt dùng 5-fold trên train thay cho dev (dev VTB lệch phân phối so với train/test,
xem `docs/notes/GHI_CHU.md` mục 2); tiếng Anh dùng dev.

| Bảng | Nội dung | Lệnh tạo |
|---|---|---|
| results_cv.md | Tiếng Việt: mọi mô hình, 5-fold trên train (TB ± std giữa các fold) | `python scripts/run_experiments.py --split cv --langs vi` |
| results_dev.md | Mọi mô hình trên dev, kèm tham số (với tiếng Việt chỉ là thí nghiệm phụ) | `python scripts/run_experiments.py` |
| tune_{lang}_{model}.md | Grid search k-fold trên train | `python scripts/tune.py` |
| learning_curve.csv | RQ1: điểm theo frac × seed (vi: seed là số thứ tự fold, cột `eval`) | `python scripts/learning_curve.py` |
| analysis_vi_cv.md | RQ2/RQ4 tiếng Việt: acc theo nhóm token, kiểm định cặp, cặp nhầm (out-of-fold) | `python scripts/analyze.py --split cv --langs vi` |
| analysis_{lang}_dev.md | Như trên, trên dev (vi: dùng cho accuracy theo độ dài câu) | `python scripts/analyze.py` |
| ablation_{lang}.md | RQ3: ablation nhóm đặc trưng CRF (vi: 5-fold, en: dev) | `python scripts/ablation.py` |
| ga_vi.md | GA chọn nhóm đặc trưng | `python -m src.ga --lang vi` |
