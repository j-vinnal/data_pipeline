"""Demonstration module for data ingestion and logging.

This module simulates data ingestion for a given source configuration
and showcases various logging levels, including exception handling.
"""

import logging

from data_pipeline.utils.config_loader import SourceConfig

logger = logging.getLogger(__name__)


def ingest(source: SourceConfig) -> None:
    """Simulate data ingestion for the given source and emit log records.

    Args:
        source: The data source configuration to ingest from.
    """
    logger.info("Ingesting source | [url: %s] | [format: %s]", source.url, source.format)

    donuts = 5
    guests = 0
    try:
        _ = donuts / guests
    except ZeroDivisionError:
        logger.exception("An exception occurred while trying to divide by zero.")
