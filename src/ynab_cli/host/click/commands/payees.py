import asyncio

import click

from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.click.constants import CONTEXT_KEY_QUIET, CONTEXT_KEY_SETTINGS
from ynab_cli.host.textual.application import App
from ynab_cli.host.textual.widgets.payees import (
    PAYEES_LIST_DUPLICATES_TAB_ID,
    PAYEES_LIST_UNUSED_TAB_ID,
    PAYEES_NORMALIZE_NAMES_TAB_ID,
)


async def _normalize_names(settings: Settings, quiet: bool) -> None:
    params: use_cases.NormalizeNamesParams = {}
    app = App(
        settings,
        quiet,
        (PAYEES_NORMALIZE_NAMES_TAB_ID, params),
    )
    await app.run_async()


async def _list_duplicates(settings: Settings, quiet: bool) -> None:
    params: use_cases.ListDuplicatesParams = {}
    app = App(
        settings,
        quiet,
        (PAYEES_LIST_DUPLICATES_TAB_ID, params),
    )
    await app.run_async()


async def _list_unused(settings: Settings, quiet: bool) -> None:
    params: use_cases.ListUnusedParams = {}
    app = App(
        settings,
        quiet,
        (PAYEES_LIST_UNUSED_TAB_ID, params),
    )
    await app.run_async()


@click.command()
@click.pass_context
def normalize_names(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(_normalize_names(ctx.obj[CONTEXT_KEY_SETTINGS], ctx.obj[CONTEXT_KEY_QUIET]))


@click.command()
@click.pass_context
def list_duplicates(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(_list_duplicates(ctx.obj[CONTEXT_KEY_SETTINGS], ctx.obj[CONTEXT_KEY_QUIET]))


@click.command()
@click.pass_context
def list_unused(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(_list_unused(ctx.obj[CONTEXT_KEY_SETTINGS], ctx.obj[CONTEXT_KEY_QUIET]))


@click.group()
@click.pass_context
def payees(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


payees.add_command(normalize_names)
payees.add_command(list_duplicates)
payees.add_command(list_unused)
