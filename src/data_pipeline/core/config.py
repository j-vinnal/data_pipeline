"""Pipeline configuration loader."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from data_pipeline import PROJECT_ROOT

_DEFAULT_PIPELINE_CONFIG = PROJECT_ROOT / "config" / "pipeline.toml"


@dataclass(frozen=True)
class SourceConfig:
    """Configuration for a single data source.

    Attributes:
        name (str): The source identifier key (e.g. 'gps', 'gtfs').
        url (str): The URL to fetch data from.
        format (str): The file format of the source data (e.g. 'csv', 'zip').
        description (str): Human-readable description of the source.
    """

    name: str
    url: str
    format: str
    description: str


def load_pipeline_config(
    config_path: Path = _DEFAULT_PIPELINE_CONFIG,
) -> dict[str, SourceConfig]:
    """Load and parse the pipeline configuration from a TOML file.

    Args:
        config_path (Path): Path to the pipeline TOML configuration file.
    Returns:
        dict[str, SourceConfig]: A dictionary mapping source names to their configurations.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Pipeline config not found: {config_path}")

    with config_path.open("rb") as f:
        raw: dict[str, Any] = tomllib.load(f)

    return {
        name: SourceConfig(name=name, **values)
        for name, values in raw.get("sources", {}).items()
    }
