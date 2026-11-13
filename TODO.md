# TODO: checklist hoàn thiện project

## Lõi BTL
- [ ] src/hmm.py: TODO(1) đếm, TODO(2) làm trơn + log, TODO(3) Viterbi -> qua 6/6 test
- [ ] src/hmm.py: các chiến lược xử lý UNK (RQ2)
- [ ] src/evaluate.py: tách predict_all() và metrics(records, train_vocab, mask); lưu records vào results/preds/
- [ ] src/features.py + src/crf.py
- [ ] src/model_selection.py + scripts/tune.py -> configs/best_params.json
- [ ] chốt cách xử lý dev VTB lệch độ dài câu
- [ ] scripts/learning_curve.py (RQ1), src/stats.py
- [ ] scripts/analyze.py (RQ2, phân tích lỗi)
- [ ] scripts/ablation.py (RQ3)
- [ ] (nếu kịp) src/memm.py (RQ4), src/ga.py
- [ ] đánh giá MỘT LẦN trên test

## Tái lập & đóng gói
- [ ] Makefile, Dockerfile, CI (.github/workflows/tests.yml)
- [ ] tests: test_crf.py, test_stats.py, test_model_selection.py
- [ ] commit bảng/hình cuối vào results/tables, results/figures

## Tài liệu
- [ ] docs/report.pdf, docs/slides.pdf (tự thêm)
- [ ] README.md tiếng Anh: tóm tắt, hình chính, bảng kết quả test, phát hiện chính, quick start, trích dẫn dữ liệu
- [ ] README.vi.md, LICENSE

## Trước khi công khai (sau khi có điểm)
- [ ] kiểm tra lịch sử git không có dữ liệu, file nặng hay thông tin nhạy cảm
- [ ] gắn tag v1.0 cho bản đã nộp
