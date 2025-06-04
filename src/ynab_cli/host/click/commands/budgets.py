import asyncio

import click
from rich.table import Table

from ynab_cli.adapters.rich import io
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import budgets as use_cases
from ynab_cli.host.click.commands.rich.progress_table import ProgressTable
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS


async def _list_all(settings: Settings) -> None:
    params: use_cases.ListAllParams = {}

    table = Table(title="All Budgets")
    table.add_column("Budget ID")
    table.add_column("Budget Name")

    console = None
    with ProgressTable(table) as progress:
        console = progress.console

        task_id = progress.add_task("Loading all budgets...")
        async for budget in use_cases.list_all(settings, io.RichIO((progress, task_id)), params):
            table.add_row(
                str(budget.id),
                str(budget.name),
            )

    if console:
        console.print(table)


@click.command()
@click.pass_context
def list_all(ctx: click.Context) -> None:
    """List all budgets in YNAB."""

    ctx.ensure_object(dict)
    asyncio.run(_list_all(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())))


@click.group()
@click.pass_context
def budgets(ctx: click.Context) -> None:
    """Manage YNAB budgets in YNAB."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings


budgets.add_command(list_all)
