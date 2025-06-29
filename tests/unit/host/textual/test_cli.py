from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.cli import cli
from ynab_cli.host.textual.app import YnabCliApp


class TestTui:
    def test_tui(self) -> None:
        runner = CliRunner()
        mock_app = MagicMock(spec=YnabCliApp)
        with patch("ynab_cli.host.textual.cli.YnabCliApp", return_value=mock_app) as mock_app_cls:
            result = runner.invoke(cli, ["tui", "--access-token", "test_token", "--budget-id", "test_budget"])

            assert result.exit_code == 0
            mock_app_cls.assert_called_once_with(
                Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget"))
            )
            mock_app.run_async.assert_called_once()
