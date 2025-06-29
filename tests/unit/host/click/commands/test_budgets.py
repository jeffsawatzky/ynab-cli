from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import ANY, MagicMock, patch
from uuid import UUID

import pytest
from click.testing import CliRunner

from ynab_cli.adapters.ynab import models
from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_list_all(runner: CliRunner, empty_uuid: UUID) -> None:
    async def list_all(*args: Any, **kwargs: Any) -> AsyncIterator[models.BudgetSummary]:
        yield models.BudgetSummary(id=empty_uuid, name="Test Budget")

    with patch("ynab_cli.host.click.commands.budgets.use_cases") as mock_use_cases:
        mock_use_cases.list_all = MagicMock(wraps=list_all)
        result = runner.invoke(cli, ["run", "--access-token", "test_token", "budgets", "list-all"])

        assert result.exit_code == 0
        mock_use_cases.list_all.assert_called_once_with(Settings(ynab=YnabSettings(access_token="test_token")), ANY, {})
