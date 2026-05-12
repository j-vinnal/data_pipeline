"""
dummy_ingest.py
-----
Logging demonstration module.

"""

import logging

logger = logging.getLogger(__name__)


def ingest() -> None:
    """Emit one log record at every standard level, then trigger an exception."""

    name = "Jüri"

    logger.debug("This is a debug message")
    logger.debug("name=%s", name)          # use % interpolation, not f-strings
    logger.info("This is an info message")
    logger.info("Data loaded", extra={"file": "data.csv", "rows": 150})
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    donuts = 5
    guests = 0
    try:
        donuts_per_guest = donuts / guests
    except ZeroDivisionError:
        # logger.exception logs at ERROR level and appends the full traceback
        logger.exception("An exception occurred while trying to divide by zero.")
