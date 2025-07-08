import json
from typing import IO, Any

import anyio
import click
from lagom import Container

from ynab_cli.domain.models import rules
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import transactions as use_cases
from ynab_cli.host.click.commands.rich.progress_table import ProgressTable
from ynab_cli.host.click.container import containerize
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX


class ApplyRulesCommand:
    def __init__(self, use_case: use_cases.ApplyRules, progress_table: ProgressTable) -> None:
        self._use_case = use_case
        self._progress_table = progress_table

        self._progress_table.table.title = "Applying Transaction Rules"
        self._progress_table.table.add_column("Transaction Id")
        self._progress_table.table.add_column("Transaction Date")
        self._progress_table.table.add_column("Transaction Payee")
        self._progress_table.table.add_column("Transaction Category")
        self._progress_table.table.add_column("Transaction Memo")
        self._progress_table.table.add_column("Transaction Amount")
        self._progress_table.table.add_column("Transaction Changes")

    async def __call__(self, settings: Settings, transaction_rules: rules.TransactionRules) -> None:
        params: use_cases.ApplyRulesParams = {
            "transaction_rules": transaction_rules,
        }

        console = None
        with self._progress_table:
            console = self._progress_table.console

            async for transaction, save_transaction in self._use_case(settings, params):
                self._progress_table.table.add_row(
                    transaction.id,
                    transaction.date.isoformat(),
                    str(transaction.payee_name),
                    str(transaction.category_name),
                    str(transaction.memo),
                    str(transaction.amount),
                    str(save_transaction.to_dict()),
                )

        if console:
            console.print(self._progress_table.table)


@containerize
async def _apply_rules(container: Container, transaction_rules: rules.TransactionRules) -> None:
    await container[ApplyRulesCommand](container[Settings], transaction_rules)


@click.command()
@click.argument("rules-file", type=click.File())
@click.pass_context
def apply_rules(ctx: click.Context, rules_file: IO[Any]) -> None:
    """Apply transaction rules from a JSON RULES_FILE to transactions in the YNAB budget.

    RULES_FILE should be a JSON file containing transaction rules.
    """

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    transaction_rules = rules.TransactionRules.from_dict(json.load(rules_file))

    anyio.run(
        _apply_rules,
        settings,
        transaction_rules,
        backend_options={"use_uvloop": True},
    )


@click.group()
@click.option("--budget-id", prompt=True, envvar=f"{ENV_PREFIX}_BUDGET_ID", show_envvar=True, help="YNAB budget ID.")
@click.pass_context
def transactions(ctx: click.Context, budget_id: str) -> None:
    """Manage transactions in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    settings.ynab.budget_id = budget_id
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings


transactions.add_command(apply_rules)
