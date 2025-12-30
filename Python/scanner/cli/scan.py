"""
Scan command for Specter.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from scanner.core.scanner import ScanConfig, scan_targets
from scanner.output.json import render_json
from scanner.output.table import render_table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.callback(invoke_without_command=True)
def scan(
    target: Annotated[
        str,
        typer.Argument(
            ...,
            help="Target to scan (IP, CIDR, hostname, or file path)",
        ),
    ],
    ports: Annotated[
        str,
        typer.Option(
            "--ports",
            "-p",
            help="Ports to scan (e.g. 22,80,443 or 1-1024)",
        ),
    ] = "1-1024",
    tcp: Annotated[
        bool,
        typer.Option(
            "--tcp/--no-tcp",
            help="Enable TCP scanning",
        ),
    ] = True,
    udp: Annotated[
        bool,
        typer.Option(
            "--udp",
            help="Enable UDP scanning",
        ),
    ] = False,
    syn: Annotated[
        bool,
        typer.Option(
            "--syn",
            help="Use TCP SYN (half-open) scan",
        ),
    ] = False,
    no_ping: Annotated[
        bool,
        typer.Option(
            "--no-ping",
            help="Skip host discovery",
        ),
    ] = False,
    service_detect: Annotated[
        bool,
        typer.Option(
            "--service-detect/--no-service-detect",
            help="Enable service fingerprinting",
        ),
    ] = True,
    rate_limit: Annotated[
        int,
        typer.Option(
            "--rate-limit",
            help="Packets per second limit",
            min=1,
        ),
    ] = 500,
    timeout: Annotated[
        float,
        typer.Option(
            "--timeout",
            help="Socket timeout in seconds",
        ),
    ] = 2.0,
    retries: Annotated[
        int,
        typer.Option(
            "--retries",
            help="Retry count per port",
            min=0,
        ),
    ] = 1,
    output: Annotated[
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="Write output to file",
        ),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            help="Output results as JSON",
        ),
    ] = False,
) -> None:
    """
    Scan targets for open ports and running services.

    Example:
      specter scan 192.168.1.1 -p 1-1000 --syn

    Args:
        target (str, optional): _description_. Defaults to typer.Argument( ..., help="Target to scan (IP, CIDR, hostname, or file path)", ).
        ports (str, optional): _description_. Defaults to typer.Option( "1-1024", "--ports", "-p", help="Ports to scan (e.g. 22,80,443 or 1-1024)", ).
        tcp (bool, optional): _description_. Defaults to typer.Option( True, "--tcp/--no-tcp", help="Enable TCP scanning", ).
        udp (bool, optional): _description_. Defaults to typer.Option( False, "--udp", help="Enable UDP scanning", ).
        syn (bool, optional): _description_. Defaults to typer.Option( False, "--syn", help="Use TCP SYN (half-open) scan", ).
        no_ping (bool, optional): _description_. Defaults to typer.Option( False, "--no-ping", help="Skip host discovery", ).
        service_detect (bool, optional): _description_. Defaults to typer.Option( True, "--service-detect/--no-service-detect", help="Enable service fingerprinting", ).
        rate_limit (int, optional): _description_. Defaults to typer.Option( 500, "--rate-limit", help="Packets per second limit", min=1, ).
        timeout (float, optional): _description_. Defaults to typer.Option( 2.0, "--timeout", help="Socket timeout in seconds", ).
        retries (int, optional): _description_. Defaults to typer.Option( 1, "--retries", help="Retry count per port", min=0, ).
        output (Optional[Path], optional): _description_. Defaults to typer.Option( None, "--output", "-o", help="Write output to file", ).
        json_output (bool, optional): _description_. Defaults to typer.Option( False, "--json", help="Output results as JSON", ).
    """

    console.print("[bold cyan]▶ Starting scan[/bold cyan]")

    config = ScanConfig(
        target=target,
        ports=ports,
        tcp=tcp,
        udp=udp,
        syn=syn,
        skip_discovery=no_ping,
        service_detect=service_detect,
        rate_limit=rate_limit,
        timeout=timeout,
        retries=retries,
    )

    results = scan_targets(config)

    if json_output:
        render_json(results, output)
    else:
        render_table(results, output)

    console.print("[bold green]✔ Scan completed[/bold green]")
