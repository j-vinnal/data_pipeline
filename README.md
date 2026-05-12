# Data Pipeline Framework

## Description

A modular, configuration-driven Python data pipeline designed for real-time and scheduled data ingestion. Built to fetch Tallinn public transport data (GPS & GTFS), it serves as a robust boilerplate for various data engineering projects. **Work is still in progress.**

**Key Features:**

- **Configuration-Driven:** Add or modify data sources via TOML without touching the code.
- **Idempotency & Partitioning:** Safely downloads data into Hive-style partitioned directories (e.g., `data/raw/source=gps/date=2026-05-12/`).
- **Structured Logging:** Custom logging format designed for easy debugging and log parsing.

## Getting Started (Local Development)

### Prerequisites

- Python 3.11+

### Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux

# Install the package and its dependencies in editable mode
pip install -e .

```

## Usage

The pipeline is operated via a Command Line Interface (CLI). It features two main execution modes: `run` (one-off execution) and `daemon` (continuous background execution).

### 1. One-off Execution (`run`)

Fetch data immediately for the specified sources, completely ignoring the configured time windows.

```bash
# Run all configured sources at once
python -m data_pipeline run

# Run a specific source
python -m data_pipeline run --source gps
python -m data_pipeline run --source gtfs

# Invalid sources will return a clear error:
python -m data_pipeline run --source unknown
# -> "invalid choice: 'unknown' (choose from 'gps', 'gtfs')"

```

### 2. Continuous Execution (`daemon`)

Run the pipeline continuously. It will respect the `interval_seconds` and `window_start` / `window_end` settings defined in the configuration.

```bash
python -m data_pipeline daemon

```

## Docker Deployment

For long-running ingestion, deploying with Docker Compose is highly recommended. The container mounts your local `data`, `logs`, and `config` directories, meaning all downloaded files will appear instantly in your Windows/host file system.

```bash
# Build the image and start the daemon in the background
docker-compose up -d --build

# View real-time logs
docker-compose logs -f

# Stop the container safely
docker-compose down

```

## Configuration

All data sources and schedules are managed in `config/pipeline.toml`.

```toml
[sources.gps]
url = "[https://transport.tallinn.ee/readfile.php?name=gps.txt](https://transport.tallinn.ee/readfile.php?name=gps.txt)"
format = "csv"
description = "Real-time vehicle positions, updated every 30 seconds"
interval_seconds = 30
window_start = "07:00"
window_end = "10:00"
overwrite_existing = true

```

**Applying Configuration Changes:** Currently, the pipeline loads the configuration once at startup. If you modify `pipeline.toml` while the daemon is running via Docker, you need to restart the container for the changes to take effect:

```bash
docker-compose restart

```

**TODO:**

- [ ] Implement hot-reloading for the daemon mode to re-read the configuration dynamically on every loop without requiring a restart.
