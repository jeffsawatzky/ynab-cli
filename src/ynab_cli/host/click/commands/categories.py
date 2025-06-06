import asyncio

import click
from rich.table import Table

from ynab_cli.adapters.rich import io
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import categories as use_cases
from ynab_cli.host.click.commands.rich.progress_table import ProgressTable
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX


async def _list_unused(settings: Settings) -> None:
    params: use_cases.ListUnusedParams = {}

    table = Table(title="Unused Categories")
    table.add_column("Category Group ID")
    table.add_column("Category Group Name")
    table.add_column("Category ID")
    table.add_column("Category Name")

    console = None
    with ProgressTable(table) as progress:
        console = progress.console

        task_id = progress.add_task("Loading unused categories...")
        async for category in use_cases.list_unused(settings, io.RichIO((progress, task_id)), params):
            table.add_row(
                str(category.category_group_id),
                str(category.category_group_name),
                str(category.id),
                str(category.name),
            )

    if console:
        console.print(table)


async def _list_all(settings: Settings) -> None:
    params: use_cases.ListAllParams = {}

    table = Table(title="All Categories")
    table.add_column("Category Group ID")
    table.add_column("Category Group Name")
    table.add_column("Category ID")
    table.add_column("Category Name")

    console = None
    with ProgressTable(table) as progress:
        console = progress.console

        task_id = progress.add_task("Loading all categories...")
        async for category in use_cases.list_all(settings, io.RichIO((progress, task_id)), params):
            table.add_row(
                str(category.category_group_id),
                str(category.category_group_name),
                str(category.id),
                str(category.name),
            )

    if console:
        console.print(table)


@click.command()
@click.pass_context
def list_unused(ctx: click.Context) -> None:
    """List unused categories in the YNAB budget."""

    ctx.ensure_object(dict)
    asyncio.run(_list_unused(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())))


@click.command()
@click.pass_context
def list_all(ctx: click.Context) -> None:
    """List all categories in the YNAB budget."""

    ctx.ensure_object(dict)
    asyncio.run(_list_all(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())))


@click.group()
@click.option("--budget-id", prompt=True, envvar=f"{ENV_PREFIX}_BUDGET_ID", show_envvar=True, help="YNAB budget ID.")
@click.pass_context
def categories(ctx: click.Context, budget_id: str) -> None:
    """Manage YNAB categories in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    settings.ynab.budget_id = budget_id
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings


categories.add_command(list_all)
categories.add_command(list_unused)
