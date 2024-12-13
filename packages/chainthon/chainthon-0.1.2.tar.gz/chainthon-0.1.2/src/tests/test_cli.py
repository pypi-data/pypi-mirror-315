"""CLI tests."""
import pytest
from click.testing import CliRunner
from chainthon.cli import cli

@pytest.fixture
def runner():
    """Provide a CLI runner."""
    return CliRunner()

def test_cli_version(runner):
    """Test the --version option."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "chainthon" in result.output

def test_cli_help(runner):
    """Test the --help option."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output

def test_run_command_help(runner):
    """Test the run command help."""
    result = runner.invoke(cli, ["run", "--help"])
    assert result.exit_code == 0
    assert "Start the chainthon server" in result.output
