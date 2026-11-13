"""MaxEnt từng từ và MEMM (RQ4, vấn đề label bias). LÀM SAU CÙNG, nếu còn thời gian.

TODO:
- [ ] MaxEntTagger: LogisticRegression trên đặc trưng của src/features.py, không dùng nhãn trước
- [ ] MEMMTagger: thêm đặc trưng nhãn trước t_{i-1}; huấn luyện với nhãn gold
- [ ] giải mã MEMM bằng Viterbi trên log P(t_i | t_{i-1}, x) (tái sử dụng ý tưởng từ src/hmm.py)
- [ ] so sánh MaxEnt vs MEMM vs CRF với CÙNG bộ đặc trưng
"""
