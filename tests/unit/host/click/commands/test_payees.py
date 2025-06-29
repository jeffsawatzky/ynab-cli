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


def test_normalize_names(runner: CliRunner, empty_uuid: UUID) -> None:
    async def normalize_names(*args: Any, **kwargs: Any) -> AsyncIterator[tuple[models.Payee, str]]:
        yield (
            models.Payee(
                id=empty_uuid,
                name="Payee",
                deleted=False,
            ),
            "Payee",
        )

    with patch("ynab_cli.host.click.commands.payees.use_cases") as mock_use_cases:
        mock_use_cases.normalize_names = MagicMock(wraps=normalize_names)
        result = runner.invoke(
            cli, ["run", "--access-token", "test_token", "payees", "--budget-id", "test_budget", "normalize-names"]
        )

        assert result.exit_code == 0
        mock_use_cases.normalize_names.assert_called_once_with(
            Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")), ANY, {}
        )


def test_list_duplicates(runner: CliRunner, empty_uuid: UUID) -> None:
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

    with patch("ynab_cli.host.click.commands.payees.use_cases") as mock_use_cases:
        mock_use_cases.list_duplicates = MagicMock(wraps=list_duplicates)
        result = runner.invoke(
            cli, ["run", "--access-token", "test_token", "payees", "--budget-id", "test_budget", "list-duplicates"]
        )

        assert result.exit_code == 0
        mock_use_cases.list_duplicates.assert_called_once_with(
            Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")), ANY, {}
        )


def test_list_unused(runner: CliRunner, empty_uuid: UUID) -> None:
    async def list_unused(*args: Any, **kwargs: Any) -> AsyncIterator[models.Payee]:
        yield models.Payee(
            id=empty_uuid,
            name="Payee",
            deleted=False,
        )

    with patch("ynab_cli.host.click.commands.payees.use_cases") as mock_use_cases:
        mock_use_cases.list_unused = MagicMock(wraps=list_unused)
        result = runner.invoke(
            cli, ["run", "--access-token", "test_token", "payees", "--budget-id", "test_budget", "list-unused"]
        )

        assert result.exit_code == 0
        mock_use_cases.list_unused.assert_called_once_with(
            Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")),
            ANY,
            {"prefix_unused": False},
        )


def test_list_all(runner: CliRunner, empty_uuid: UUID) -> None:
    async def list_all(*args: Any, **kwargs: Any) -> AsyncIterator[models.Payee]:
        yield models.Payee(
            id=empty_uuid,
            name="Payee",
            deleted=False,
        )

    with patch("ynab_cli.host.click.commands.payees.use_cases") as mock_use_cases:
        mock_use_cases.list_all = MagicMock(wraps=list_all)
        result = runner.invoke(
            cli, ["run", "--access-token", "test_token", "payees", "--budget-id", "test_budget", "list-all"]
        )

        assert result.exit_code == 0
        mock_use_cases.list_all.assert_called_once_with(
            Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")), ANY, {}
        )
