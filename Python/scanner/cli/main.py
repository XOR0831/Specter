"""
Main CLI entry point for Specter (Port Scanner & Service Fingerprinter).
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from scanner.cli.discover import discover
from scanner.cli.scan import scan
from scanner.utils.logging import setup_logging

# Root Typer application
app = typer.Typer(
    name="specter",
    help="Port Scanner & Service Fingerprinter",
    add_completion=True,
    no_args_is_help=True,
)

console = Console()


@app.callback()
def main(
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable verbose output",
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logging",
        ),
    ] = False,
    config: Annotated[
        Optional[Path],
        typer.Option(
            "--config",
            "-c",
            help="Path to configuration file",
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
) -> None:
    """
    Specter — Port Scanner & Service Fingerprinter.

    Use this tool only on systems you own or are authorized to test.

    Args:
        verbose (bool, optional): _description_. Defaults to typer.Option( False, "--verbose", "-v", help="Enable verbose output", ).
        debug (bool, optional): _description_. Defaults to typer.Option( False, "--debug", help="Enable debug logging", ).
        config (Optional[Path], optional): _description_. Defaults to typer.Option( None, "--config", "-c", help="Path to configuration file", exists=True, readable=True, resolve_path=True, ).
    """
    setup_logging(verbose=verbose, debug=debug)

    if config:
        console.log(f"Using config file: [bold]{config}[/bold]")


# Register subcommands
app.command(
    help="Scan targets for open ports and services",
)(scan)

app.command(
    help="Discover live hosts",
)(discover)


def run() -> None:
    """
    Entry point for console_scripts.
    """
    app()


if __name__ == "__main__":
    run()
