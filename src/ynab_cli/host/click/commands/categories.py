import asyncio

import click

from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import categories as use_cases
from ynab_cli.host.click.constants import (
    CONTEXT_KEY_QUIET,
    CONTEXT_KEY_SETTINGS,
)
from ynab_cli.host.textual.application import App
from ynab_cli.host.textual.widgets.categories import (
    CATEGORIES_LIST_ALL_TAB_ID,
    CATEGORIES_LIST_UNUSED_TAB_ID,
)


async def _list_unused(settings: Settings, quiet: bool) -> None:
    params: use_cases.ListUnusedParams = {}
    app = App(
        settings,
        quiet,
        (CATEGORIES_LIST_UNUSED_TAB_ID, params),
    )
    await app.run_async()


async def _list_all(settings: Settings, quiet: bool) -> None:
    params: use_cases.ListAllParams = {}
    app = App(
        settings,
        quiet,
        (CATEGORIES_LIST_ALL_TAB_ID, params),
    )
    await app.run_async()


@click.command()
@click.pass_context
def list_unused(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(_list_unused(ctx.obj[CONTEXT_KEY_SETTINGS], ctx.obj[CONTEXT_KEY_QUIET]))


@click.command()
@click.pass_context
def list_all(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(_list_all(ctx.obj[CONTEXT_KEY_SETTINGS], ctx.obj[CONTEXT_KEY_QUIET]))


@click.group()
@click.pass_context
def categories(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


categories.add_command(list_unused)
categories.add_command(list_all)
