"""Main entry point for the data pipeline application."""

import sys
import logging
import tomllib

from data_pipeline.utils.logging_setup import setup_logging

from data_pipeline.utils.config_loader import load_pipeline_config
from data_pipeline.ingestion.dummy_ingest import ingest
from data_pipeline.cli import parse_args

logger = logging.getLogger(__name__)


def main() -> int:
    """Executes the main application flow.

    Returns:
        int: 0 for successful execution, non-zero exit code for failure.
    """
    setup_logging()

    try:
        config = load_pipeline_config()
    except FileNotFoundError:
        logger.critical("Pipeline config missing")
        return 1
    except tomllib.TOMLDecodeError:
        logger.critical("Pipeline config is invalid TOML")
        return 1

    valid_sources = list(config.sources.keys())
    args = parse_args(valid_sources=valid_sources)

    if args.command == "run":
        sources_to_run = (
            [config.sources[args.source]]
            if args.source
            else list(config.sources.values())
        )

        overall_success = True

        for source in sources_to_run:
            logger.info("Pipeline started", extra={"source": source.name})
            try:
                ingest(source)
            except Exception as e:
                logger.error(
                    "Ingestion failed: %s",
                    e,
                    extra={"source": source.name},
                    exc_info=True,
                )
                overall_success = False
            finally:
                logger.info("Pipeline finished", extra={"source": source.name})

        # Return non-zero exit code if any source failed
        return 0 if overall_success else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
