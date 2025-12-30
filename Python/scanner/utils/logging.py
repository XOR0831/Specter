"""
Centralized logging utilities.
"""

from __future__ import annotations

import sys
from typing import Optional

from loguru import logger

# ----------------------------
# Public API
# ----------------------------


def setup_logging(
    *,
    verbose: bool = False,
    debug: bool = False,
) -> None:
    """
    Configure global logging behavior.
    - verbose: Enable INFO-level logging
    - debug: Enable DEBUG-level logging

    Args:
        verbose (bool, optional): _description_. Defaults to False.
        debug (bool, optional): _description_. Defaults to False.
    """

    logger.remove()

    level = "WARNING"
    if debug:
        level = "DEBUG"
    elif verbose:
        level = "INFO"

    logger.add(
        sys.stderr,
        level=level,
        format=_log_format(debug),
        enqueue=True,
        backtrace=debug,
        diagnose=debug,
    )

    logger.debug(f"Logging initialized (level={level})")


def get_logger(name: Optional[str] = None):
    """
    Get a namespaced logger.

    Args:
        name (Optional[str], optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    if name:
        return logger.bind(module=name)
    return logger


# ----------------------------
# Helpers
# ----------------------------


def _log_format(debug: bool) -> str:
    """
    Return log format string based on verbosity.

    Args:
        debug (bool): _description_

    Returns:
        str: _description_
    """

    if debug:
        return "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    return "<level>{level}</level>: <level>{message}</level>"
