"""Các nhóm đặc trưng (có tên) cho CRF / MaxEnt / MEMM, phục vụ ablation (RQ3) và GA.

TODO:
- [ ] FEATURE_GROUPS = {tên_nhóm: hàm(words, i) -> dict đặc trưng}
      gợi ý nhóm: word, affix (tiền/hậu tố), shape (hoa/số/gạch nối),
      context±1, context±2, syllable (riêng tiếng Việt: số âm tiết, âm tiết đầu/cuối)
- [ ] word2features(words, i, groups): gộp dict của các nhóm được chọn
- [ ] đảm bảo bỏ/thêm một nhóm không làm thay đổi các nhóm khác (ablation có kiểm soát)
"""
