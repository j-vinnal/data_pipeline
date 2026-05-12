import logging
import logging.config
import tomllib
from pathlib import Path
from typing import Any, List, Literal, Optional

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_LOGGING_CONFIG = _PROJECT_ROOT / "config" / "logging.toml"
_LOGS_DIR = _PROJECT_ROOT / "logs"


class ConditionalFormatter(logging.Formatter):
    """
    Custom formatter that appends dynamically specified extra fields
    to the log message if they are present in the LogRecord.
    """

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        extra_fields: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, **kwargs)
        # Store the fields we want to monitor dynamically
        self.extra_fields = extra_fields or []

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text and append extra fields.
        """
        # Capture the original exception info
        original_exc_info = record.exc_info

        # Temporarily clear the exception info to prevent automatic multi-line traceback printing
        record.exc_info = None
        record.exc_text = None

        # Format the base message using standard logic
        formatted_message = super().format(record)

        # Collect dynamic extra fields
        extra_parts = []
        for field in self.extra_fields:
            if hasattr(record, field):
                value = getattr(record, field)
                if value is not None:  # Only add if the value is not None/empty
                    extra_parts.append(f"[{field}: {value}]")

        # If there was an error, append the info in a clean, single-line format
        if original_exc_info and original_exc_info[0] is not None:
            exc_type, exc_value, _ = original_exc_info
            extra_parts.append(f"[Exception: {exc_type.__name__} - {exc_value}]")

        if extra_parts:
            formatted_message += " | " + " | ".join(extra_parts)

        # Restore the original exception info to its initial state
        record.exc_info = original_exc_info

        return formatted_message


def setup_logging(config_path: Path = _DEFAULT_LOGGING_CONFIG) -> None:
    """
    Load logging configuration from a TOML file and apply it.

    Args:
        config_path (Path): The path to the TOML configuration file.

    Raises:
        FileNotFoundError: If the configuration file is missing.
    """
    # Create the log output directory if it does not exist
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Read the TOML configuration file and apply settings
    if config_path.exists():
        with config_path.open("rb") as f:
            config = tomllib.load(f)

        # Dynamically overwrite the file handler path with an absolute path
        if "handlers" in config and "file_handler" in config["handlers"]:
            log_file = _LOGS_DIR / "app.log"
            config["handlers"]["file_handler"]["filename"] = str(log_file)

        logging.config.dictConfig(config)
    else:
        raise FileNotFoundError(f"Logging configuration file not found: {config_path}")
