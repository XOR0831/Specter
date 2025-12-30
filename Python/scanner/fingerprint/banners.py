"""
Service banner grabbing utilities.
"""

from __future__ import annotations

import socket
import ssl
from typing import Any, Optional

from scanner.utils.logging import get_logger

logger = get_logger(__name__)


# ----------------------------
# Public API
# ----------------------------


def grab_banner(
    host: str,
    port: int,
    protocol: str,
    timeout: float = 2.0,
) -> Optional[str]:
    """
    Grab a service banner from an open port.

    Args:
        host (str): _description_
        port (int): _description_
        protocol (str): _description_
        timeout (float, optional): _description_. Defaults to 2.0.

    Returns:
        Optional[str]: _description_
    """

    try:
        if port in (443, 8443):
            return _grab_tls_banner(host, port, timeout)

        return _grab_tcp_banner(host, port, timeout)

    except Exception as exc:
        logger.debug(f"Banner grab failed for {host}:{port} → {exc}")
        return None


# ----------------------------
# TCP Banner
# ----------------------------


def _grab_tcp_banner(
    host: str,
    port: int,
    timeout: float,
) -> Optional[str]:
    """
    Grab banner over plain TCP.

    Args:
        host (str): _description_
        port (int): _description_
        timeout (float): _description_

    Returns:
        Optional[str]: _description_
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))

        # Passive read
        try:
            data = sock.recv(4096)
            if data:
                return _normalize_banner(data)
        except socket.timeout:
            pass

        # Active probe
        probe = _protocol_probe(port)
        if probe:
            sock.sendall(probe)
            data = sock.recv(4096)
            if data:
                return _normalize_banner(data)

    return None


# ----------------------------
# TLS / HTTPS Banner
# ----------------------------


def _grab_tls_banner(
    host: str,
    port: int,
    timeout: float,
) -> Optional[str]:
    """
    Perform a TLS handshake and extract certificate info.

    Args:
        host (str): _description_
        port (int): _description_
        timeout (float): _description_

    Returns:
        Optional[str]: _description_
    """

    context = ssl.create_default_context()

    with socket.create_connection((host, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls_sock:
            cert: dict[str, Any] | None = tls_sock.getpeercert()
            if not cert:
                return None

            subject = _parse_cert_name(cert.get("subject"))
            issuer = _parse_cert_name(cert.get("issuer"))

            cn = subject.get("commonName", "")
            issuer_cn = issuer.get("commonName", "")

            return f"TLS CN={cn} Issuer={issuer_cn}"


def _parse_cert_name(name: Any) -> dict[str, str]:
    """
    Parse X.509 subject / issuer structure returned by ssl.getpeercert().

    Args:
        name (Any): _description_

    Returns:
        dict[str, str]: _description_
    """
    result: dict[str, str] = {}

    if not isinstance(name, tuple):
        return result

    # Expected shape:
    # tuple[tuple[tuple[str, str], ...], ...]
    for rdn in name:
        if not isinstance(rdn, tuple):
            continue

        for pair in rdn:
            if isinstance(pair, tuple) and len(pair) == 2 and isinstance(pair[0], str) and isinstance(pair[1], str):
                key, value = pair
                result[key] = value

    return result


# ----------------------------
# Helpers
# ----------------------------


def _protocol_probe(port: int) -> Optional[bytes]:
    """
    Return a protocol-aware probe payload for known ports.

    Args:
        port (int): _description_

    Returns:
        Optional[bytes]: _description_
    """

    probes: dict[int, bytes] = {
        80: b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n",
        8080: b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n",
        21: b"USER anonymous\r\n",
        25: b"EHLO scanner\r\n",
        6379: b"PING\r\n",
    }

    return probes.get(port)


def _normalize_banner(data: bytes) -> str:
    """
    Normalize banner data for fingerprinting.

    Args:
        data (bytes): _description_

    Returns:
        str: _description_
    """

    try:
        text = data.decode(errors="ignore")
    except UnicodeDecodeError:
        return ""

    return text.strip().replace("\r", "").replace("\n", " ")
