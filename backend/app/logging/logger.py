"""
Custom logging module for application-wide structured and colored logging.

This module:
- Dynamically adjusts logging level based on configuration
- Supports per-module logging using a `Source` enum
- Outputs colored log lines for DEBUG, INFO, WARNING, and ERROR messages
- Formats logs with timestamp and module source
"""

import logging
import sys
from typing import Any

from app.logging import Source

logger = logging.getLogger("AppLogger") # Main logger
logger.setLevel((logging.INFO, logging.DEBUG)[True]) # Set output level

class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds ANSI colors to log output based on the log level.
    """

    COLOR_MAP = {
        logging.ERROR: '\033[31m', # Red for errors
        logging.WARNING: '\033[33m', # Yellow for warnings
        # No color for INFO - white as default
        # No color for DEBUG - white as default
    }

    def format(self, record):
        """
        Formats a log record with ANSI color codes if applicable.

        :param record: Log record.
        :return: Formatted log record.
        """
        color = self.COLOR_MAP.get(record.levelno, '') # Choose color depending on level
        reset = '\033[0m' # Reset color afterwards
        message = super().format(record) # Apply standard format
        return f'{color}{message}{reset}' # Return colored log

formatter = ColoredFormatter(
    fmt="%(asctime)s:%(msecs)03d [%(levelname)s] [%(source)s] - %(message)s", # log format -> time LEVEL SOURCE - message
    datefmt="%H:%M:%S" # date format
)

console_handler = logging.StreamHandler(sys.stdout) # create handler to send logs to stdout
console_handler.setFormatter(formatter) # set format
logger.addHandler(console_handler) # register handler for the logger

class SourceLoggerAdapter(logging.LoggerAdapter):
    """
    LoggerAdapter that injects a `source` field into log records for structured log output.
    """

    def process(self, msg: str, kwargs: dict) -> tuple[str, dict[str, Any]]:
        """
        Ensure that each log record contains the 'source' field.

        :param msg: Log message
        :param kwargs: Additional logging keyword arguments

        :return: Tuple of message and kwargs with the 'extra' dictionary populated
        """
        source = self.extra.get("source", "UNKNOWN")
        kwargs["extra"] = {"source": source}
        return msg, kwargs

# Cache adapter for every source so we don't have to create a new instance every time
_source_loggers: dict[Source, SourceLoggerAdapter] = {
    source: SourceLoggerAdapter(logger, {"source": source})
    for source in Source
}

def get_source_logger(source: Source) -> SourceLoggerAdapter:
    """
    Retrieves a logger adapter for the given source.

    :param source: Enum value indicating the source/module
    :return: A logger adapter that tags messages with the provided source.
    """
    return _source_loggers[source]

def log_debug(source: Source, message: str) -> None:
    """Log a debug message with the given source."""
    get_source_logger(source).debug(message)

def log_info(source: Source, message: str) -> None:
    """Log an info message with the given source."""
    get_source_logger(source).info(message)

def log_warning(source: Source, message: str) -> None:
    """Log a warning message with the given source."""
    get_source_logger(source).warning(message)

def log_error(source: Source, message: str) -> None:
    """Log an error message with the given source."""
    get_source_logger(source).error(message)

log_debug(Source.logger, "This is debug!")
log_info(Source.logger, "This is info!")
log_warning(Source.logger, "This is a warning!")
log_error(Source.logger, "This is an error!")
print("\n")