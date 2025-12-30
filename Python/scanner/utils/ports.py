"""
Port parsing utilities.
"""

from __future__ import annotations

from typing import List, Set

MIN_PORT = 1
MAX_PORT = 65535


class PortParseError(ValueError):
    pass


def parse_ports(port_spec: str) -> List[int]:
    """
    Parse a port specification string into a list of ports.

    Example inputs:
      - "22"
      - "22,80,443"
      - "1-1024"
      - "22,80-90,443"

    Args:
        port_spec (str): _description_

    Raises:
        PortParseError: _description_
        PortParseError: _description_

    Returns:
        List[int]: _description_
    """

    if not port_spec:
        raise PortParseError("Port specification cannot be empty")

    ports: Set[int] = set()

    parts = port_spec.split(",")

    for part in parts:
        part = part.strip()

        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start = _parse_port(start_str)
            end = _parse_port(end_str)

            if start > end:
                raise PortParseError(f"Invalid port range: {part}")

            for port in range(start, end + 1):
                ports.add(port)

        else:
            ports.add(_parse_port(part))

    return sorted(ports)


def _parse_port(value: str) -> int:
    """
    Parse and validate a single port number.

    Args:
        value (str): _description_

    Raises:
        PortParseError: _description_
        PortParseError: _description_

    Returns:
        int: _description_
    """

    try:
        port = int(value)
    except ValueError as err:
        raise PortParseError(f"Invalid port: {value}") from err

    if not (MIN_PORT <= port <= MAX_PORT):
        raise PortParseError(f"Port out of range: {port}")

    return port
