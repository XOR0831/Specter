"""
UDP scanning utilities.
"""

from __future__ import annotations

import socket

from scanner.utils.logging import get_logger

logger = get_logger(__name__)


# ----------------------------
# Public API
# ----------------------------


def udp_scan(
    host: str,
    port: int,
    timeout: float = 2.0,
) -> str:
    """
    Perform a UDP scan on a single port.

    Returns:
        - "open"
        - "closed"
        - "open|filtered"

    Args:
        host (str): _description_
        port (int): _description_
        timeout (float, optional): _description_. Defaults to 2.0.

    Returns:
        str: _description_
    """

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)

            # Send empty UDP packet (safe default)
            sock.sendto(b"", (host, port))

            try:
                data, _ = sock.recvfrom(4096)
                if data:
                    # Any response means the port is open
                    return "open"

            except socket.timeout:
                # No response is ambiguous in UDP
                return "open|filtered"

    except ConnectionRefusedError:
        # ICMP Port Unreachable
        return "closed"

    except OSError as e:
        logger.debug(f"UDP scan error on {host}:{port} → {e}")
        return "open|filtered"

    return "open|filtered"
