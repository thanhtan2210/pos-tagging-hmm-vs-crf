# Chạy lại toàn bộ project trong môi trường cố định:
#   docker build -t pos-tagging .
#   docker run --rm -v "$PWD/results:/app/results" pos-tagging
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml Makefile ./
COPY src/ src/
COPY scripts/ scripts/
COPY tests/ tests/
COPY configs/ configs/
RUN mkdir -p results/tables results/figures results/preds

CMD ["make", "all"]
