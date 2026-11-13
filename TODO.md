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

## Nhánh làm việc: file nào ở nhánh nào

Làm theo thứ tự từ trên xuống. Mỗi nhánh xong (pytest xanh) thì merge vào `main`,
và nhánh sau nên tạo hoặc cập nhật từ `main` mới nhất (`git merge main`).

| # | Nhánh | File làm việc | Xong khi |
|---|---|---|---|
| 1 | `feat/eval-records` | src/evaluate.py, scripts/run_experiments.py (phần predict_all/records) | evaluate() cũ vẫn chạy; có file trong results/preds/ |
| 2 | `feat/hmm` | src/hmm.py (TODO 1–3, rồi biến thể UNK), src/baseline.py (tùy chọn) | 6/6 test HMM qua; HMM thắng baseline trên dev |
| 3 | `feat/crf` | src/features.py, src/crf.py, tests/test_crf.py, scripts/run_experiments.py (đăng ký "crf") | CRF chạy được trên vi và en |
| 4 | `feat/tuning` | src/model_selection.py, scripts/tune.py, configs/best_params.json, tests/test_model_selection.py, scripts/run_experiments.py (đọc config, --seed, cảnh báo test) | best_params.json được sinh tự động |
| 5 | `exp/learning-curve` | scripts/learning_curve.py, src/stats.py, tests/test_stats.py | Hình RQ1 có thanh sai số; bootstrap/McNemar chạy được |
| 6 | `exp/analysis` | scripts/analyze.py, scripts/eda.py (tách hàm độ mơ hồ) | Ma trận nhầm lẫn, acc theo độ dài câu và theo nhóm token (RQ2) |
| 7 | `exp/ablation` | scripts/ablation.py (có thể chỉnh src/features.py) | Bảng ablation vi/en (RQ3) |
| 8 | `exp/memm-ga` (nếu kịp) | src/memm.py, src/ga.py | RQ4; so GA với ablation và L1 |
| 9 | `chore/packaging` | Makefile, Dockerfile, .github/workflows/tests.yml, LICENSE, README.md, README.vi.md, notebooks/ | `make all` chạy lại được mọi thứ; CI xanh |

Không theo nhánh (làm song song bất cứ lúc nào, commit thẳng vào nhánh đang đứng):
docs/notes/KE_HOACH.md (bảng giả thuyết — điền TRƯỚC nhánh 5), docs/notes/GHI_CHU.md (hạn chế),
docs/report.pdf, docs/slides.pdf.

Lưu ý: nhánh 1 và 3, 4 cùng sửa scripts/run_experiments.py -> merge nhánh trước vào main
rồi `git merge main` vào nhánh sau trước khi sửa tiếp, để tránh conflict.
