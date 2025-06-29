from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ynab_cli.host.cli import cli, main
from ynab_cli.host.constants import ENV_PREFIX


class TestCli:
    def test_cli_version_option(self) -> None:
        """Test CLI version option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "version" in result.output.lower()

    def test_cli_help_option(self) -> None:
        """Test CLI help option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Main entrypoint." in result.output
        assert "--dry-run" in result.output
        assert "--debug" in result.output


class TestMain:
    @patch("ynab_cli.host.cli.cli")
    def test_main_function(self, mock_cli: MagicMock) -> None:
        """Test main function calls cli with correct parameters."""
        main()

        mock_cli.assert_called_once_with(auto_envvar_prefix=ENV_PREFIX, obj={})
