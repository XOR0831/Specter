"""
Target expansion utilities.
"""

from __future__ import annotations

import ipaddress
import socket
from pathlib import Path
from typing import Iterable, List, Set

from scanner.utils.logging import get_logger

logger = get_logger(__name__)


class TargetParseError(ValueError):
    pass


# ----------------------------
# Public API
# ----------------------------


def expand_targets(target: str) -> List[str]:
    """
    Expand a target specification into a list of hosts.

    Supported:
      - Single IP
      - CIDR (IPv4)
      - Hostname
      - File containing targets

    Args:
        target (str): _description_

    Raises:
        TargetParseError: _description_

    Returns:
        List[str]: _description_
    """

    expanded: Set[str] = set()

    path = Path(target)

    if path.exists() and path.is_file():
        logger.debug(f"Loading targets from file: {path}")
        lines = _load_target_file(path)
        for line in lines:
            expanded.update(expand_targets(line))
        return sorted(expanded)

    # CIDR
    if _is_cidr(target):
        expanded.update(_expand_cidr(target))
        return sorted(expanded)

    # IP address
    if _is_ip(target):
        return [target]

    # Hostname
    resolved = _resolve_hostname(target)
    if resolved:
        return [resolved]

    raise TargetParseError(f"Invalid target: {target}")


# ----------------------------
# Helpers
# ----------------------------


def _load_target_file(path: Path) -> Iterable[str]:
    """
    Load targets from a file, ignoring comments and blank lines.

    Args:
        path (Path): _description_

    Returns:
        Iterable[str]: _description_
    """

    targets: List[str] = []

    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            targets.append(line)

    return targets


def _is_ip(value: str) -> bool:
    """
    Checks if input is an IP address.

    Args:
        value (str): _description_

    Returns:
        bool: _description_
    """
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def _is_cidr(value: str) -> bool:
    """
    Checks if input is a CIDR range.

    Args:
        value (str): _description_

    Returns:
        bool: _description_
    """
    try:
        ipaddress.ip_network(value, strict=False)
        return "/" in value
    except ValueError:
        return False


def _expand_cidr(cidr: str) -> Iterable[str]:
    """
    Expand CIDR into individual IP addresses.

    Args:
        cidr (str): _description_

    Returns:
        Iterable[str]: _description_

    Yields:
        Iterator[Iterable[str]]: _description_
    """

    network = ipaddress.ip_network(cidr, strict=False)

    for ip in network.hosts():
        yield str(ip)


def _resolve_hostname(hostname: str) -> str | None:
    """
    Resolve hostname to an IP address.

    Args:
        hostname (str): _description_

    Returns:
        str | None: _description_
    """

    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        logger.debug(f"Failed to resolve hostname: {hostname}")
        return None
