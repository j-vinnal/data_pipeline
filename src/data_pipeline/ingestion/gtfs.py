"""Ingestor implementation for GTFS Schedule data."""

from datetime import datetime
from pathlib import Path

import requests

from data_pipeline.ingestion.base import BaseIngestor, RAW_DATA_DIR


class GTFSIngestor(BaseIngestor, source_name="gtfs"):
    """Ingestor for fetching daily GTFS zip archives."""

    def fetch(self) -> bytes:
        """Fetch GTFS zip file via HTTP GET."""
        response = requests.get(self.config.url, timeout=30)
        response.raise_for_status()
        return response.content

    def save(self, data: bytes) -> Path:
        """Save GTFS data with a daily timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"{self.config.name}_{timestamp}.{self.config.format}"
        file_path = RAW_DATA_DIR / filename

        with file_path.open("wb") as f:
            f.write(data)

        return file_path
