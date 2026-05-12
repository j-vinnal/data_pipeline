"""Ingestor implementation for GTFS Schedule data."""

from datetime import datetime
from pathlib import Path

import requests

from data_pipeline.ingestion.base import BaseIngestor


class GTFSIngestor(BaseIngestor, source_name="gtfs"):
    """Ingestor for fetching daily GTFS zip archives."""

    def fetch(self) -> bytes:
        """Fetch GTFS zip file via HTTP GET."""
        response = requests.get(self.config.url, timeout=30)
        response.raise_for_status()
        return response.content

    def get_target_path(self) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"{self.config.name}_{timestamp}.{self.config.format}"
        return self.get_save_dir() / filename

    def save(self, data: bytes) -> Path:
        """Save GTFS data with a daily timestamp."""
        file_path = self.get_target_path()
        with file_path.open("wb") as f:
            f.write(data)
        return file_path
