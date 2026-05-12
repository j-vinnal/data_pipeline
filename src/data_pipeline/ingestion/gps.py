"""Ingestor implementation for Real-Time GPS data."""

from datetime import datetime
from pathlib import Path

import requests

from data_pipeline.ingestion.base import BaseIngestor, RAW_DATA_DIR


class GPSIngestor(BaseIngestor, source_name="gps"):
    """Ingestor for fetching real-time bus GPS locations."""

    def fetch(self) -> bytes:
        """Fetch GPS text data via HTTP GET."""
        # Timeout is important to avoid hanging pipelines
        response = requests.get(self.config.url, timeout=10)
        response.raise_for_status()
        return response.content

    def save(self, data: bytes) -> Path:
        """Save GPS data with a precise timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.config.name}_{timestamp}.{self.config.format}"
        file_path = RAW_DATA_DIR / filename

        with file_path.open("wb") as f:
            f.write(data)

        return file_path
