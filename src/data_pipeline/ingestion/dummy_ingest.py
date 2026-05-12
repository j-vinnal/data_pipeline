"""Demonstration module for data ingestion and logging.

This module provides functionality to simulate data ingestion and showcases
various logging levels, including exception handling.
"""

import logging

logger = logging.getLogger(__name__)


def ingest() -> None:
    """Simulate data ingestion and emit log records."""

    name = "Jüri"

    logger.debug("This is a debug message")
    logger.debug("name=%s", name)
    logger.info("This is an info message")
    logger.info("Data loaded", extra={"file": "data.csv", "rows": 150})
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    donuts = 5
    guests = 0
    try:
        _ = donuts / guests
    except ZeroDivisionError:
        logger.exception("An exception occurred while trying to divide by zero.")
