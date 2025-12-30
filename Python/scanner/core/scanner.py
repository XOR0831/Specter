"""
Core scanning orchestration logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from scanner.core.discovery import discover_hosts
from scanner.core.rate_limit import RateLimiter
from scanner.fingerprint.banners import grab_banner
from scanner.fingerprint.signatures import match_service
from scanner.protocols.tcp import tcp_connect_scan
from scanner.protocols.udp import udp_scan
from scanner.utils.ports import parse_ports
from scanner.utils.targets import expand_targets

# ----------------------------
# Data Models
# ----------------------------


@dataclass(frozen=True)
class ScanConfig:
    target: str
    ports: str
    tcp: bool = True
    udp: bool = False
    syn: bool = False
    skip_discovery: bool = False
    service_detect: bool = True
    rate_limit: int = 500
    timeout: float = 2.0
    retries: int = 1


@dataclass
class PortResult:
    port: int
    protocol: str
    state: str
    service: str | None = None
    version: str | None = None
    banner: str | None = None


@dataclass
class HostResult:
    host: str
    ports: List[PortResult]


# ----------------------------
# Public API
# ----------------------------


def scan_targets(config: ScanConfig) -> List[HostResult]:
    """
    Entry point for scanning targets.

    Args:
        config (ScanConfig): _description_

    Returns:
        List[HostResult]: _description_
    """

    targets = expand_targets(config.target)
    ports = parse_ports(config.ports)

    limiter = RateLimiter(config.rate_limit)

    # Host discovery
    if config.skip_discovery:
        live_hosts = targets
    else:
        live_hosts = discover_hosts(targets)

    results: List[HostResult] = []

    for host in live_hosts:
        port_results: List[PortResult] = []

        for port in ports:
            if config.tcp:
                limiter.acquire()
                state = tcp_connect_scan(
                    host,
                    port,
                    timeout=config.timeout,
                    retries=config.retries,
                )

                pr = PortResult(
                    port=port,
                    protocol="tcp",
                    state=state,
                )

                if state == "open" and config.service_detect:
                    banner = grab_banner(host, port, "tcp", config.timeout)
                    pr.banner = banner

                    if banner:
                        svc = match_service(banner)
                        if svc:
                            pr.service = svc.name
                            pr.version = svc.version

                port_results.append(pr)

            if config.udp:
                limiter.acquire()
                state = udp_scan(
                    host,
                    port,
                    timeout=config.timeout,
                )

                port_results.append(
                    PortResult(
                        port=port,
                        protocol="udp",
                        state=state,
                    )
                )

        results.append(
            HostResult(
                host=host,
                ports=port_results,
            )
        )

    return results
