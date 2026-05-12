"""Abstract base class for data ingestors."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from data_pipeline import PROJECT_ROOT
from data_pipeline.core.config import SourceConfig

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


class BaseIngestor(ABC):
    """Abstract base class defining the interface for all data ingestors."""

    # All created subclasses are collected here
    _registry: dict[str, type["BaseIngestor"]] = {}

    def __init_subclass__(cls, source_name: str, **kwargs: Any) -> None:
        """Automatically registers subclasses when they are defined."""
        super().__init_subclass__(**kwargs)
        cls._registry[source_name] = cls

    @classmethod
    def get_ingestor(cls, source_config: SourceConfig) -> "BaseIngestor":
        """Factory method to get the correct ingestor instance."""
        ingestor_class = cls._registry.get(source_config.name)
        if not ingestor_class:
            raise ValueError(f"No ingestor registered for source: '{source_config.name}'")
        return ingestor_class(source_config)

    def __init__(self, source_config: SourceConfig) -> None:
        self.config = source_config
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def fetch(self) -> bytes:
        pass

    @abstractmethod
    def save(self, data: bytes) -> Path:
        pass

    def run(self) -> None:
        self.logger.info("Ingestion started", extra={"url": self.config.url})
        try:
            raw_data = self.fetch()
            saved_path = self.save(raw_data)
            self.logger.info(
                "Ingestion completed", 
                extra={"saved_to": str(saved_path), "size_bytes": len(raw_data)}
            )
        except Exception:
            self.logger.exception("Ingestion failed", extra={"source": self.config.name})
            raise
