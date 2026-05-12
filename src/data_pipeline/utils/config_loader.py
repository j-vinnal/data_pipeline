"""
Pipeline configuration loader.

This module loads and validates the pipeline configuration from a TOML file
and exposes it as typed dataclasses.
"""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_PIPELINE_CONFIG = _PROJECT_ROOT / "config" / "pipeline.toml"


@dataclass(frozen=True)
class SourceConfig:
    """Configuration for a single data source.

    Attributes:
        name: The source identifier key (e.g. 'gps', 'gtfs').
        url: The URL to fetch data from.
        format: The file format of the source data (e.g. 'csv', 'zip').
        description: Human-readable description of the source.
    """

    name: str
    url: str
    format: str
    description: str


@dataclass(frozen=True)
class PipelineConfig:
    """Top-level pipeline configuration.

    Attributes:
        sources: A mapping of source name to its configuration.
    """

    sources: dict[str, SourceConfig]

    def get_source(self, name: str) -> SourceConfig:
        """Retrieve a source configuration by name.

        Args:
            name: The source identifier (e.g. 'gps', 'gtfs').

        Returns:
            The matching SourceConfig.
    
        Raises:
            ValueError: If the source name is not found in the configuration.
        """
        if name not in self.sources:
            available = ", ".join(self.sources)
            raise ValueError(f"Unknown source '{name}'. Available: {available}")
        return self.sources[name]


def load_pipeline_config(
    config_path: Path = _DEFAULT_PIPELINE_CONFIG,
) -> PipelineConfig:
    """Load and parse the pipeline configuration from a TOML file.

    Args:
        config_path: Path to the pipeline TOML configuration file.

    Returns:
        A populated PipelineConfig instance.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Pipeline config not found: {config_path}")

    with config_path.open("rb") as f:
        raw: dict[str, Any] = tomllib.load(f)

    sources = {
        name: SourceConfig(name=name, **values)
        for name, values in raw.get("sources", {}).items()
    }

    return PipelineConfig(sources=sources)
