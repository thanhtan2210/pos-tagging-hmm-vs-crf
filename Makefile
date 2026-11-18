# Chạy lại toàn bộ project: `make all`. Tập test: `make final` (CHỈ MỘT LẦN, cuối dự án).
PY ?= python

.PHONY: all data test eda tune dev curve ablation analyze ga final clean

all: data test eda tune dev curve ablation analyze

data:
	$(PY) scripts/download_data.py

test:
	$(PY) -m pytest -q

eda:
	$(PY) scripts/eda.py

tune:
	$(PY) scripts/tune.py

dev:
	$(PY) scripts/run_experiments.py

curve:
	$(PY) scripts/learning_curve.py

ablation:
	$(PY) scripts/ablation.py

analyze: dev
	$(PY) scripts/analyze.py

ga:
	$(PY) -m src.ga --lang vi

final:
	$(PY) scripts/run_experiments.py --split test

clean:
	rm -rf results/preds results/results_*.json .pytest_cache
