import json
from collections.abc import AsyncIterator, Generator
from pathlib import Path
from typing import Any
from unittest.mock import ANY, MagicMock, patch

import pytest
from click.testing import CliRunner

from tests.factories import ynab
from ynab_cli.adapters.ynab import models
from ynab_cli.domain.models import rules
from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def transaction_rules() -> rules.TransactionRules:
    return rules.TransactionRules(transaction_rules=[])


@pytest.fixture
def transaction_rules_file(runner: CliRunner, transaction_rules: rules.TransactionRules) -> Generator[Path]:
    with runner.isolated_filesystem() as tmp_path:
        with open("rules.json", "w") as rules_file:
            json.dump(transaction_rules.to_dict(), rules_file)
        yield Path(tmp_path) / "rules.json"


def test_apply_rules(
    runner: CliRunner, transaction_rules: rules.TransactionRules, transaction_rules_file: Path
) -> None:
    async def apply_rules(
        *args: Any, **kwargs: Any
    ) -> AsyncIterator[tuple[models.TransactionDetail, models.SaveTransactionWithIdOrImportId]]:
        yield (
            ynab.TransactionDetailFactory.build(),
            models.SaveTransactionWithIdOrImportId(),
        )

    with patch("ynab_cli.host.click.commands.transactions.use_cases") as mock_use_cases:
        mock_use_cases.apply_rules = MagicMock(wraps=apply_rules)
        result = runner.invoke(
            cli,
            [
                "run",
                "--access-token",
                "test_token",
                "transactions",
                "--budget-id",
                "test_budget",
                "apply-rules",
                str(transaction_rules_file),
            ],
        )

        assert result.exit_code == 0
        mock_use_cases.apply_rules.assert_called_once_with(
            Settings(ynab=YnabSettings(access_token="test_token", budget_id="test_budget")),
            ANY,
            {"transaction_rules": transaction_rules},
        )
