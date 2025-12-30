from typer.testing import CliRunner
from scanner.cli.main import app

runner = CliRunner()


def test_discover_help():
    result = runner.invoke(app, ["discover", "--help"])
    assert result.exit_code == 0
