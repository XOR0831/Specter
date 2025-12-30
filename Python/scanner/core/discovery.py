"""
Host discovery logic.
"""

from __future__ import annotations

from typing import Iterable, List

from scanner.protocols.icmp import icmp_ping
from scanner.protocols.tcp import tcp_ping
from scanner.utils.logging import get_logger

logger = get_logger(__name__)


# ----------------------------
# Public API
# ----------------------------


def discover_hosts(targets: Iterable[str]) -> List[str]:
    """
    Discover live hosts from a list of targets.

    Returns a list of hosts that appear to be up.

    Args:
        targets (Iterable[str]): _description_

    Returns:
        List[str]: _description_
    """

    live_hosts: List[str] = []

    for host in targets:
        logger.debug(f"Discovering host: {host}")

        # 1. ICMP ping
        if icmp_ping(host):
            logger.debug(f"Host up via ICMP: {host}")
            live_hosts.append(host)
            continue

        # 2. TCP ping fallback (common ports)
        if tcp_ping(host):
            logger.debug(f"Host up via TCP ping: {host}")
            live_hosts.append(host)
            continue

        logger.debug(f"Host appears down: {host}")

    return live_hosts
