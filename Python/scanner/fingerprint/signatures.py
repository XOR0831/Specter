"""
Service fingerprinting via banner signature matching.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from scanner.utils.logging import get_logger

logger = get_logger(__name__)


# ----------------------------
# Data Models
# ----------------------------


@dataclass(frozen=True)
class ServiceInfo:
    name: str
    version: Optional[str] = None


@dataclass(frozen=True)
class Signature:
    name: str
    pattern: re.Pattern
    version_group: Optional[int] = None


# ----------------------------
# Signature Database
# ----------------------------

SIGNATURES: List[Signature] = [
    # SSH
    Signature(
        name="ssh",
        pattern=re.compile(r"^SSH-\d+\.\d+-OpenSSH[_-](\S+)", re.IGNORECASE),
        version_group=1,
    ),
    # HTTP servers
    Signature(
        name="nginx",
        pattern=re.compile(r"Server:\s*nginx/?([\d\.]+)?", re.IGNORECASE),
        version_group=1,
    ),
    Signature(
        name="apache",
        pattern=re.compile(r"Server:\s*Apache/?([\d\.]+)?", re.IGNORECASE),
        version_group=1,
    ),
    # FTP
    Signature(
        name="ftp",
        pattern=re.compile(r"FTP\s+server\s+\((.*?)\)", re.IGNORECASE),
    ),
    # SMTP
    Signature(
        name="smtp",
        pattern=re.compile(r"ESMTP\s+(\S+)", re.IGNORECASE),
        version_group=1,
    ),
    # Redis
    Signature(
        name="redis",
        pattern=re.compile(r"^\+PONG", re.IGNORECASE),
    ),
    # MySQL
    Signature(
        name="mysql",
        pattern=re.compile(r"mysql\s+ver\s+([\d\.]+)", re.IGNORECASE),
        version_group=1,
    ),
    # Generic HTTP fallback
    Signature(
        name="http",
        pattern=re.compile(r"HTTP/\d\.\d", re.IGNORECASE),
    ),
]

# ----------------------------
# Public API
# ----------------------------


def match_service(banner: str) -> Optional[ServiceInfo]:
    """
    Match a banner against known service signatures.

    Returns ServiceInfo if matched, else None.

    Args:
        banner (str): _description_

    Returns:
        Optional[ServiceInfo]: _description_
    """

    if not banner:
        return None

    for sig in SIGNATURES:
        match = sig.pattern.search(banner)
        if match:
            version = None
            if sig.version_group and match.lastindex:
                try:
                    version = match.group(sig.version_group)
                except IndexError:
                    pass

            logger.debug(f"Matched service {sig.name} version={version} banner={banner[:50]}")

            return ServiceInfo(
                name=sig.name,
                version=version,
            )

    return None
