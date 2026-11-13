"""(Nâng cao, không bắt buộc) Thuật toán di truyền chọn tổ hợp nhóm đặc trưng cho CRF.

TODO:
- [ ] cá thể = vector bit, mỗi bit bật/tắt một nhóm trong FEATURE_GROUPS
- [ ] fitness = điểm k-fold trên train (KHÔNG dùng dev/test), có thể trừ phạt số nhóm
- [ ] chọn lọc, lai ghép, đột biến; ghi fitness theo thế hệ để vẽ hình
- [ ] so sánh kết quả GA với ablation thủ công và với L1
"""
