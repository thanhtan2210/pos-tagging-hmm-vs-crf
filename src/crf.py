"""CRF cho gán nhãn từ loại, bọc sklearn_crfsuite.CRF.

TODO:
- [ ] class CRFTagger(groups=None, c1=..., c2=..., max_iterations=...)
      cùng giao diện với các tagger khác: fit(sentences) -> self, predict(words) -> list[str]
- [ ] sent2features(words, groups): gọi các nhóm đặc trưng trong src/features.py
- [ ] c1 (L1) / c2 (L2) lấy từ configs/best_params.json, không chọn tay trên dev
- [ ] (nâng cao) với c1 > 0: đếm số đặc trưng có trọng số khác 0 -> phần "chọn đặc trưng bằng L1"
- [ ] đăng ký "crf" vào MODELS trong scripts/run_experiments.py
"""
