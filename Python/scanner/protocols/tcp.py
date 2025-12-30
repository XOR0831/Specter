"""
TCP scanning utilities.
"""

from __future__ import annotations

import errno
import socket
from typing import Iterable

from scanner.utils.logging import get_logger

logger = get_logger(__name__)


# ----------------------------
# TCP CONNECT SCAN
# ----------------------------


def tcp_connect_scan(
    host: str,
    port: int,
    timeout: float = 2.0,
    retries: int = 1,
) -> str:
    """
    Perform a TCP connect scan on a single port and returns:
    - "open"
    - "closed"
    - "filtered"

    Args:
        host (str): _description_
        port (int): _description_
        timeout (float, optional): _description_. Defaults to 2.0.
        retries (int, optional): _description_. Defaults to 1.

    Returns:
        str: _description_
    """

    for _ in range(retries + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))

                if result == 0:
                    return "open"

                if result in (errno.ECONNREFUSED,):
                    return "closed"

        except socket.timeout:
            logger.debug(f"Timeout connecting to {host}:{port}")

        except OSError as exc:
            logger.debug(f"OS error on {host}:{port} → {exc}")

    return "filtered"


# ----------------------------
# TCP PING (HOST DISCOVERY)
# ----------------------------

COMMON_TCP_PING_PORTS: Iterable[int] = (
    80,
    443,
    22,
    3389,
)


def tcp_ping(
    host: str,
    timeout: float = 1.0,
) -> bool:
    """
    Check if host is alive by attempting TCP connections
    to common ports.

    Args:
        host (str): _description_
        timeout (float, optional): _description_. Defaults to 1.0.

    Returns:
        bool: _description_
    """

    for port in COMMON_TCP_PING_PORTS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))

                # open OR closed means host is reachable
                if result in (0, errno.ECONNREFUSED):
                    return True

        except OSError:
            continue

    return False
