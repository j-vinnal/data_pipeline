"""Simulates data ingestion for a given source configuration."""

import logging

from data_pipeline.utils.config_loader import SourceConfig

logger = logging.getLogger(__name__)


def ingest(source: SourceConfig) -> None:
    """Simulates downloading and processing data from a given source.
    
    Args:
        source (SourceConfig): The configuration object for the target data source.
        
    Raises:
        ZeroDivisionError: Raised artificially to simulate an ingestion failure.
    """
    logger.info("Ingesting source", extra={"url": source.url, "format": source.format})

    donuts = 5
    guests = 0
    try:
        _ = donuts / guests
    except ZeroDivisionError:
        logger.exception("An exception occurred while trying to divide by zero.")
