"""
ICMP utilities for host discovery.
"""

from __future__ import annotations

from scanner.utils.logging import get_logger

logger = get_logger(__name__)

try:
    from scapy.all import ICMP, IP, sr1  # type: ignore
except ImportError:
    IP = ICMP = sr1 = None


def icmp_ping(
    host: str,
    timeout: float = 1.0,
) -> bool:
    """
    Perform an ICMP echo request (ping).

    Returns True if a reply is received.

    Args:
        host (str): _description_
        timeout (float, optional): _description_. Defaults to 1.0.

    Returns:
        bool: _description_
    """

    if IP is None or ICMP is None or sr1 is None:
        logger.debug("Scapy not available; skipping ICMP ping")
        return False

    try:
        packet = IP(dst=host) / ICMP()
        reply = sr1(
            packet,
            timeout=timeout,
            verbose=False,
        )

        if reply is not None:
            return True

    except PermissionError:
        logger.debug("ICMP ping requires elevated privileges")

    except Exception as e:
        logger.debug(f"ICMP error for {host}: {e}")

    return False
