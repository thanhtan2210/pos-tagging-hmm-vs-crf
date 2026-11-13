"""Phân tích lỗi từ results/preds/ (không huấn luyện lại).

TODO:
- [ ] ma trận nhầm lẫn (chuẩn hóa theo hàng) + top-10 cặp nhầm gold -> pred
- [ ] accuracy theo độ dài câu: <=10, 11-25, 26-50, >50 (độ bền trên dev VTB)
- [ ] accuracy theo nhóm token: OOV, từ mơ hồ (định nghĩa trong scripts/eda.py), từ nhiều âm tiết,
      từ ngữ pháp hóa (được, đến, về, cho, vào, ở, để)
- [ ] liệt kê câu HMM sai / CRF đúng và ngược lại -> chọn tay ví dụ cho báo cáo
- [ ] gọi src/stats.py để so sánh từng cặp mô hình
"""
