"""
main.py

Entry point for the application.
Responsibilities:
1. Define custom formatters.
2. Initialize the logging configuration from a TOML file.
3. Ensure the log directory exists.
4. Run the application logic.
"""

import logging
from pathlib import Path

from src.data_pipeline.utils.logging_setup import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main execution function of the script.
    """
    # 1. Initialize logging before any other operations
    config_file = Path("config/logging_config.toml")
    setup_logging(config_file)

    # 2. Start the demo
    logger.info("Logging demo started")

    # 3. Import and run the custom log module
    # We import it here to ensure the root logger is configured beforehand.

    from src.data_pipeline.ingestion.dummy_ingest import run

    run()

    # 4. Finish the demo
    logger.info("Logging demo finished")


if __name__ == "__main__":
    main()
