"""
Discover command for Specter.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, List, Optional

import typer
from rich.console import Console
from rich.table import Table

from scanner.core.discovery import discover_hosts
from scanner.utils.targets import expand_targets

console = Console()


def discover(
    target: Annotated[
        str,
        typer.Argument(
            ...,
            help="Target to discover (IP, CIDR, hostname, or file)",
        ),
    ],
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            help="Output results as JSON",
        ),
    ] = False,
    output: Annotated[
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="Write output to file",
        ),
    ] = None,
) -> None:
    """
    Discover live hosts without scanning ports.

    Args:
        target (str, optional): _description_. Defaults to typer.Argument( ..., help="Target to discover (IP, CIDR, hostname, or file)", ).
        json_output (bool, optional): _description_. Defaults to typer.Option( False, "--json", help="Output results as JSON", ).
        output (Optional[Path], optional): _description_. Defaults to typer.Option( None, "--output", "-o", help="Write output to file", ).
    """

    console.print("[bold cyan]▶ Starting host discovery[/bold cyan]")

    targets = expand_targets(target)
    live_hosts = discover_hosts(targets)

    if json_output:
        _render_json(live_hosts, output)
    else:
        _render_table(live_hosts, output)


# ----------------------------
# Output Helpers
# ----------------------------


def _render_table(hosts: List[str], output: Optional[Path]) -> None:
    """
    Render as Table.

    Args:
        hosts (List[str]): _description_
        output (Optional[Path]): _description_
    """
    table = Table(
        title="[bold cyan]Live Hosts[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
    )

    table.add_column("Host", style="bold green")

    if not hosts:
        table.add_row("[yellow]No live hosts found[/yellow]")
    else:
        for host in hosts:
            table.add_row(host)

    if output:
        with output.open("w") as f:
            file_console = Console(file=f, force_terminal=False)
            file_console.print(table)
    else:
        console.print(table)


def _render_json(hosts: List[str], output: Optional[Path]) -> None:
    """
    Render as JSON.

    Args:
        hosts (List[str]): _description_
        output (Optional[Path]): _description_
    """
    import json

    data = {"live_hosts": hosts}

    if output:
        with output.open("w") as f:
            json.dump(data, f, indent=2)
    else:
        print(json.dumps(data, indent=2))
