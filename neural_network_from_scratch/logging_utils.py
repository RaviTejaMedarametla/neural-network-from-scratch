"""Centralized logging configuration helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """Configure application-wide logging handlers.

    Args:
        level: Logging level for the root logger.
        log_file: Optional file path for a file handler.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        root_logger.addHandler(console_handler)

    if log_file and not any(isinstance(h, logging.FileHandler) for h in root_logger.handlers):
        file_path = Path(log_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a module logger and lazily configure default console logging."""
    if not logging.getLogger().handlers:
        configure_logging()
    return logging.getLogger(name)
