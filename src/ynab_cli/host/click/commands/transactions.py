import asyncio
import json
from typing import IO, Any

import click
from rich.table import Table

from ynab_cli.adapters.rich import io
from ynab_cli.domain.models import rules
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import transactions as use_cases
from ynab_cli.host.click.commands.rich.progress_table import ProgressTable
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX


async def _apply_rules(settings: Settings, transaction_rules: rules.TransactionRules) -> None:
    params: use_cases.ApplyRulesParams = {
        "transaction_rules": transaction_rules,
    }

    table = Table(title="Updated Transactions")
    table.add_column("Transaction Id")
    table.add_column("Transaction Date")
    table.add_column("Transaction Payee")
    table.add_column("Transaction Category")
    table.add_column("Transaction Memo")
    table.add_column("Transaction Amount")
    table.add_column("Transaction Changes")

    console = None
    with ProgressTable(table) as progress:
        console = progress.console

        task_id = progress.add_task("Updating transactions...")
        async for transaction, save_transaction in use_cases.apply_rules(
            settings, io.RichIO((progress, task_id)), params
        ):
            table.add_row(
                transaction.id,
                transaction.date.isoformat(),
                str(transaction.payee_name),
                str(transaction.category_name),
                str(transaction.memo),
                str(transaction.amount),
                str(save_transaction.to_dict()),
            )

    if console:
        console.print(table)


@click.command()
@click.argument("rules-file", type=click.File())
@click.pass_context
def apply_rules(ctx: click.Context, rules_file: IO[Any]) -> None:
    """Apply transaction rules from a JSON RULES_FILE to transactions in the YNAB budget.

    RULES_FILE should be a JSON file containing transaction rules.
    """

    ctx.ensure_object(dict)

    transaction_rules = rules.TransactionRules.from_dict(json.load(rules_file))

    asyncio.run(_apply_rules(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings()), transaction_rules))


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
