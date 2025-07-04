from unittest.mock import MagicMock

from click.testing import CliRunner
from lagom import Container

from ynab_cli.host.cli import cli
from ynab_cli.host.textual.app import YnabCliApp


class TestTui:
    def test_tui(self, runner: CliRunner, container: Container) -> None:
        mock_app = MagicMock(spec=YnabCliApp)
        container[YnabCliApp] = mock_app

        result = runner.invoke(cli, ["tui", "--access-token", "test_token", "--budget-id", "test_budget"])

        assert result.exit_code == 0

        mock_app.run_async.assert_called_once()
