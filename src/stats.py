"""Kiểm định ý nghĩa thống kê khi so sánh hai mô hình trên cùng một split.

Đầu vào: records (words, gold, pred) theo từng câu, đọc từ results/preds/.

TODO:
- [ ] paired_bootstrap(records_a, records_b, n=1000, seed) -> (hiệu trung bình, CI 95%)
      lấy mẫu có hoàn lại theo CÂU (token trong một câu không độc lập)
- [ ] mcnemar(records_a, records_b) -> (b, c, p-value), b = A đúng B sai, c = B đúng A sai
"""
