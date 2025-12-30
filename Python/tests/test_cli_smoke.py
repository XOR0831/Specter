from typer.testing import CliRunner

from scanner.cli.main import app


runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_scan_help():
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0


def test_discover_help():
    result = runner.invoke(app, ["discover", "--help"])
    assert result.exit_code == 0
