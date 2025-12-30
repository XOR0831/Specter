"""
JSON output renderer.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

from scanner.core.scanner import HostResult, PortResult

# ----------------------------
# Public API
# ----------------------------


def render_json(
    results: Iterable[HostResult],
    output: Path | None = None,
) -> None:
    """
    Render scan results as JSON.

    If output is provided, write to file.
    Otherwise, print to stdout.

    Args:
        results (Iterable[HostResult]): _description_
        output (Path | None, optional): _description_. Defaults to None.
    """

    data = [_host_to_dict(host) for host in results]

    if output:
        with output.open("w") as f:
            json.dump(data, f, indent=2)
    else:
        print(json.dumps(data, indent=2))


# ----------------------------
# Serialization Helpers
# ----------------------------


def _host_to_dict(host: HostResult) -> Dict[str, Any]:
    """
    Format hosts and ports as dictionary.

    Args:
        host (HostResult): _description_

    Returns:
        Dict[str, Any]: _description_
    """
    return {
        "host": host.host,
        "ports": [_port_to_dict(p) for p in host.ports],
    }


def _port_to_dict(port: PortResult) -> Dict[str, Any]:
    """
    Format ports as dictionary.

    Args:
        port (PortResult): _description_

    Returns:
        Dict[str, Any]: _description_
    """
    return {
        "port": port.port,
        "protocol": port.protocol,
        "state": port.state,
        "service": port.service,
        "version": port.version,
        "banner": port.banner,
    }
