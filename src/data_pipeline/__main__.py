"""Entry point for the data pipeline application.

This module parses CLI arguments, initializes logging, loads the pipeline
configuration, and triggers the selected ingestion source.
"""

import argparse
import logging

from data_pipeline.utils.config_loader import load_pipeline_config
from data_pipeline.utils.logging_setup import setup_logging
from data_pipeline.ingestion.dummy_ingest import ingest

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        prog="data-pipeline",
        description="Run the data pipeline for a specified source.",
        epilog="Thanks for using %(prog)s! :)"
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Data source to ingest (e.g. 'gps', 'gtfs').",
    )
    return parser.parse_args()


def main() -> None:
    """Execute the main application flow."""

    setup_logging()

    args = parse_args()
    config = load_pipeline_config()
    source = config.get_source(args.source)

    logger.info("Pipeline started | [source: %s]", source.name)
    ingest(source)
    logger.info("Pipeline finished | [source: %s]", source.name)


if __name__ == "__main__":
    main()
