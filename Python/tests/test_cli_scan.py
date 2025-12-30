from typer.testing import CliRunner
from scanner.cli.main import app

runner = CliRunner()


def test_scan_help():
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
