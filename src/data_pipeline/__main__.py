"""Main entry point for the data pipeline application."""

import sys
import logging
import tomllib

from data_pipeline import ingestion
from data_pipeline.core.logger import setup_logging
from data_pipeline.core.config import load_pipeline_config, SourceConfig
import data_pipeline.ingestion as ingestion
from data_pipeline.cli import parse_args

logger = logging.getLogger(__name__)


def run_pipeline(
        sources_dict: dict[str, SourceConfig], source_name: str | None
) -> bool:
    """Executes the ingestion process for specified sources.
    
    Args:
        sources_dict (dict[str, SourceConfig]): The loaded pipeline sources configuration.
        source_name (str | None): The specific source to run, or None to run all.

    Returns:
        bool: True if all sources were successfully ingested, False otherwise.
    """
    sources_to_run = (
        [sources_dict[source_name]] if source_name else list(sources_dict.values())
    )

    source_names = [source.name for source in sources_to_run]
    sources_str = ", ".join(source_names)

    logger.info("Pipeline started", extra={"source": sources_str})

    overall_success = True

    for source in sources_to_run:
        try:
            ingestor = ingestion.BaseIngestor.get_ingestor(source)
            ingestor.run()
        except (OSError, RuntimeError, ValueError):
            logger.exception("Ingestion failed", extra={"source": source.name})
            overall_success = False

    logger.info(
        "Pipeline finished", extra={"source": sources_str, "success": overall_success}
    )
    return overall_success


def main() -> int:
    """Executes the main application flow.

    Returns:
        int: 0 for successful execution, non-zero exit code for failure.
    """
    setup_logging()

    try:
        sources_config = load_pipeline_config()
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        logger.critical("Pipeline config error")
        return 1

    valid_sources = list(sources_config.keys())
    args = parse_args(valid_sources=valid_sources)

    if args.command == "run":
        success = run_pipeline(sources_config, args.source)
        return 0 if success else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
