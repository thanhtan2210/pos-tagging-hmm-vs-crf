# Chạy lại toàn bộ project: `make all`. Tập test: `make final` (CHỈ MỘT LẦN, cuối dự án).
PY ?= python

.PHONY: all data test eda tune dev curve ablation analyze ga models final clean

all: data test eda tune dev curve ablation analyze

data:
	$(PY) scripts/download_data.py

test:
	$(PY) -m pytest -q

eda:
	$(PY) scripts/eda.py

tune:
	$(PY) scripts/tune.py

# Tiếng Việt: kết quả chính là 5-fold trên train (dev VTB lệch phân phối, docs/notes/GHI_CHU.md mục 2);
# dev của cả hai ngôn ngữ vẫn được chạy (với tiếng Việt là thí nghiệm phụ theo độ dài câu).
dev:
	$(PY) scripts/run_experiments.py
	$(PY) scripts/run_experiments.py --split cv --langs vi

curve:
	$(PY) scripts/learning_curve.py

ablation:
	$(PY) scripts/ablation.py

analyze: dev
	$(PY) scripts/analyze.py
	$(PY) scripts/analyze.py --split cv --langs vi

ga:
	$(PY) -m src.ga --lang vi

# Huấn luyện mô hình cuối trên toàn bộ train, lưu vào models/ (không nằm trong git).
models:
	$(PY) scripts/train_final.py

final:
	$(PY) scripts/run_experiments.py --split test

clean:
	rm -rf results/preds results/results_*.json .pytest_cache
