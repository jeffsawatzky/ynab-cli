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
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS


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
            progress.refresh()
    if console:
        console.print(table)


@click.command()
@click.argument("rules-file", type=click.File())
@click.pass_context
def apply_rules(ctx: click.Context, rules_file: IO[Any]) -> None:
    ctx.ensure_object(dict)

    transaction_rules = rules.TransactionRules.from_dict(json.load(rules_file))

    asyncio.run(_apply_rules(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings()), transaction_rules))


@click.group()
@click.pass_context
def transactions(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


transactions.add_command(apply_rules)
