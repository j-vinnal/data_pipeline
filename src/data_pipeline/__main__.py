"""Entry point for the data pipeline application.

This module initializes the core configuration, sets up the logging
environment, and triggers the main ingestion pipeline.
"""

import logging

from data_pipeline.utils.logging_setup import setup_logging
from data_pipeline.ingestion.dummy_ingest import ingest

logger = logging.getLogger(__name__)


def main() -> None:
    """Execute the main application flow.

    This function initializes logging and runs the data ingestion process.
    """
    setup_logging()

    logger.info("Logging demo started")
    ingest()
    logger.info("Logging demo finished")


if __name__ == "__main__":
    main()
