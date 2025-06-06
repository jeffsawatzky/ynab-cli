import asyncio

import click
from rich.table import Table

from ynab_cli.adapters.rich import io
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.click.commands.rich.progress_table import ProgressTable
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX


async def _normalize_names(settings: Settings) -> None:
    params: use_cases.NormalizeNamesParams = {}

    table = Table(title="Normalized Payees")
    table.add_column("Payee Id")
    table.add_column("Payee Name")
    table.add_column("Normalized Name")

    console = None
    with ProgressTable(table) as progress:
        console = progress.console

        task_id = progress.add_task("Normalizing payee names...")
        async for payee, normalized_name in use_cases.normalize_names(settings, io.RichIO((progress, task_id)), params):
            table.add_row(
                str(payee.id),
                payee.name,
                normalized_name,
            )

    if console:
        console.print(table)


async def _list_duplicates(settings: Settings) -> None:
    params: use_cases.ListDuplicatesParams = {}

    table = Table(title="Duplicate Payees")
    table.add_column("Payee Id")
    table.add_column("Payee Name")
    table.add_column("Duplicate Payee Id")
    table.add_column("Duplicate Payee Name")

    console = None
    with ProgressTable(table) as progress:
        console = progress.console

        task_id = progress.add_task("Loading duplicate payees...")
        async for payee, duplicate_payee in use_cases.list_duplicates(settings, io.RichIO((progress, task_id)), params):
            table.add_row(
                str(payee.id),
                payee.name,
                str(duplicate_payee.id),
                duplicate_payee.name,
            )

    if console:
        console.print(table)


async def _list_unused(settings: Settings, prefix_unused: bool) -> None:
    params: use_cases.ListUnusedParams = {
        "prefix_unused": prefix_unused,
    }

    table = Table(title="Unused Payees")
    table.add_column("Payee Id")
    table.add_column("Payee Name")

    console = None
    with ProgressTable(table) as progress:
        console = progress.console

        task_id = progress.add_task("Loading unused payees...")
        async for payee in use_cases.list_unused(settings, io.RichIO((progress, task_id)), params):
            table.add_row(
                str(payee.id),
                payee.name,
            )

    if console:
        console.print(table)


async def _list_all(settings: Settings) -> None:
    params: use_cases.ListAllParams = {}

    table = Table(title="All Payees")
    table.add_column("Payee Id")
    table.add_column("Payee Name")

    console = None
    with ProgressTable(table) as progress:
        console = progress.console

        task_id = progress.add_task("Loading all payees...")
        async for payee in use_cases.list_all(settings, io.RichIO((progress, task_id)), params):
            table.add_row(
                str(payee.id),
                payee.name,
            )

    if console:
        console.print(table)


@click.command()
@click.pass_context
def normalize_names(ctx: click.Context) -> None:
    """Normalize payee names in the YNAB budget."""

    ctx.ensure_object(dict)
    asyncio.run(_normalize_names(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())))


@click.command()
@click.pass_context
def list_duplicates(ctx: click.Context) -> None:
    """List duplicate payees in the YNAB budget."""

    ctx.ensure_object(dict)
    asyncio.run(_list_duplicates(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())))


@click.command()
@click.option("--prefix-unused", is_flag=True, default=False, help="Add a prefix to the unused payee names.")
@click.pass_context
def list_unused(ctx: click.Context, prefix_unused: bool) -> None:
    """List unused payees in the YNAB budget."""

    ctx.ensure_object(dict)
    asyncio.run(_list_unused(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings()), prefix_unused))


@click.command()
@click.pass_context
def list_all(ctx: click.Context) -> None:
    """List all payees in the YNAB budget."""

    ctx.ensure_object(dict)
    asyncio.run(_list_all(ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())))


@click.group()
@click.option("--budget-id", prompt=True, envvar=f"{ENV_PREFIX}_BUDGET_ID", show_envvar=True, help="YNAB budget ID.")
@click.pass_context
def payees(ctx: click.Context, budget_id: str) -> None:
    """Manage payees in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    settings.ynab.budget_id = budget_id
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings


payees.add_command(list_all)
payees.add_command(list_duplicates)
payees.add_command(list_unused)
payees.add_command(normalize_names)
