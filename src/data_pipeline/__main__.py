"""
__main__.py

Entry point for the application.
Responsibilities:
1. Define custom formatters.
2. Initialize the logging configuration from a TOML file.
3. Ensure the log directory exists.
4. Run the application logic.
"""

import logging

from data_pipeline.utils.logging_setup import setup_logging
from data_pipeline.ingestion.dummy_ingest import ingest

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main execution function of the script.
    """
    # 1. Initialize logging before any other operations
    setup_logging()

    # 2. Start the demo
    logger.info("Logging demo started")

    ingest()

    # 3. Finish the demo
    logger.info("Logging demo finished")


if __name__ == "__main__":
    main()
