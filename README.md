# data-pipeline

## Description

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
pip install -e .
python -m data_pipeline
```

```bash
python -m data_pipeline --source gps
python -m data_pipeline --source gtfs
python -m data_pipeline --source unknown  # → selge viga: "Unknown source 'unknown'. Available: gps, gtfs"
```
