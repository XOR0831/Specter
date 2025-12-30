"""
Human-readable table output using Rich.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from rich.console import Console
from rich.table import Table

from scanner.core.scanner import HostResult

console = Console()


# ----------------------------
# Public API
# ----------------------------


def render_table(
    results: Iterable[HostResult],
    output: Path | None = None,
) -> None:
    """
    Render scan results as a Rich table.

    If output is provided, write plain text to file.

    Args:
        results (Iterable[HostResult]): _description_
        output (Path | None, optional): _description_. Defaults to None.
    """

    tables: List[Table] = []

    for host_result in results:
        table = _build_host_table(host_result)
        tables.append(table)

    if output:
        _write_tables_to_file(tables, output)
    else:
        for table in tables:
            console.print(table)


# ----------------------------
# Table Builders
# ----------------------------


def _build_host_table(host_result: HostResult) -> Table:
    """
    Build a Rich table for a single host.

    Args:
        host_result (HostResult): _description_

    Returns:
        Table: _description_
    """

    table = Table(
        title=f"[bold cyan]Host: {host_result.host}[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
    )

    table.add_column("Port", style="bold")
    table.add_column("Proto")
    table.add_column("State")
    table.add_column("Service")
    table.add_column("Version")

    ports = sorted(
        host_result.ports,
        key=lambda p: (p.port, p.protocol),
    )

    if not ports:
        table.add_row("-", "-", "[yellow]no open ports[/yellow]", "-", "-")
        return table

    for pr in ports:
        table.add_row(
            str(pr.port),
            pr.protocol,
            _format_state(pr.state),
            pr.service or "-",
            pr.version or "-",
        )

    return table


# ----------------------------
# Helpers
# ----------------------------


def _format_state(state: str) -> str:
    """
    Colorize port state.

    Args:
        state (str): _description_

    Returns:
        str: _description_
    """

    match state:
        case "open":
            return "[green]open[/green]"
        case "closed":
            return "[red]closed[/red]"
        case "filtered":
            return "[yellow]filtered[/yellow]"
        case _:
            return state


def _write_tables_to_file(tables: List[Table], path: Path) -> None:
    """
    Write tables to a file (plain text).

    Args:
        tables (List[Table]): _description_
        path (Path): _description_
    """

    with path.open("w") as f:
        file_console = Console(file=f, force_terminal=False)
        for table in tables:
            file_console.print(table)
