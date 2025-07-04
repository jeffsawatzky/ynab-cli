from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from click.testing import CliRunner
from lagom import Container

from ynab_cli.adapters.ynab import models
from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.domain.use_cases import budgets as use_cases
from ynab_cli.host.cli import cli


def test_list_all(runner: CliRunner, container: Container, empty_uuid: UUID) -> None:
    async def list_all(*args: Any, **kwargs: Any) -> AsyncIterator[models.BudgetSummary]:
        yield models.BudgetSummary(id=empty_uuid, name="Test Budget")

    use_case = MagicMock(wraps=list_all)
    container[use_cases.ListAll] = use_case

    result = runner.invoke(cli, ["run", "--access-token", "test_token", "budgets", "list-all"])

    assert result.exit_code == 0
    use_case.assert_called_once_with(Settings(ynab=YnabSettings(access_token="test_token")), {})
