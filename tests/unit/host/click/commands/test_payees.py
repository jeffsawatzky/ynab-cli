from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from click.testing import CliRunner
from lagom import Container

from ynab_cli.adapters.ynab import models
from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.domain.use_cases import payees as mock_use_cases
from ynab_cli.host.cli import cli


def test_normalize_names(runner: CliRunner, container: Container, empty_uuid: UUID) -> None:
    async def normalize_names(*args: Any, **kwargs: Any) -> AsyncIterator[tuple[models.Payee, str]]:
        yield (
            models.Payee(
                id=empty_uuid,
                name="Payee",
                deleted=False,
            ),
            "Payee",
        )

    use_case = MagicMock(wraps=normalize_names)
    container[mock_use_cases.NormalizeNames] = use_case

    result = runner.invoke(
        cli, ["run", "--access-token", "test_token", "payees", "--budget-id", "test_budget", "normalize-names"]
    )

    assert result.exit_code == 0

    use_case.assert_called_once_with(
        Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")), {}
    )


def test_list_duplicates(runner: CliRunner, container: Container, empty_uuid: UUID) -> None:
    async def list_duplicates(*args: Any, **kwargs: Any) -> AsyncIterator[tuple[models.Payee, models.Payee]]:
        yield (
            models.Payee(
                id=empty_uuid,
                name="Payee",
                deleted=False,
            ),
            models.Payee(
                id=empty_uuid,
                name="Payee",
                deleted=False,
            ),
        )

    use_case = MagicMock(wraps=list_duplicates)
    container[mock_use_cases.ListDuplicates] = use_case

    result = runner.invoke(
        cli, ["run", "--access-token", "test_token", "payees", "--budget-id", "test_budget", "list-duplicates"]
    )

    assert result.exit_code == 0
    use_case.assert_called_once_with(
        Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")), {}
    )


def test_list_unused(runner: CliRunner, container: Container, empty_uuid: UUID) -> None:
    async def list_unused(*args: Any, **kwargs: Any) -> AsyncIterator[models.Payee]:
        yield models.Payee(
            id=empty_uuid,
            name="Payee",
            deleted=False,
        )

    use_case = MagicMock(wraps=list_unused)
    container[mock_use_cases.ListUnused] = use_case

    result = runner.invoke(
        cli, ["run", "--access-token", "test_token", "payees", "--budget-id", "test_budget", "list-unused"]
    )

    assert result.exit_code == 0
    use_case.assert_called_once_with(
        Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")), {"prefix_unused": False}
    )


def test_list_all(runner: CliRunner, container: Container, empty_uuid: UUID) -> None:
    async def list_all(*args: Any, **kwargs: Any) -> AsyncIterator[models.Payee]:
        yield models.Payee(
            id=empty_uuid,
            name="Payee",
            deleted=False,
        )

    use_case = MagicMock(wraps=list_all)
    container[mock_use_cases.ListAll] = use_case

    result = runner.invoke(
        cli, ["run", "--access-token", "test_token", "payees", "--budget-id", "test_budget", "list-all"]
    )

    assert result.exit_code == 0
    use_case.assert_called_once_with(
        Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")), {}
    )
