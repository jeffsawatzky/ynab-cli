import asyncio

import click

from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import amazon as use_cases
from ynab_cli.host.click.constants import (
    CONTEXT_KEY_QUIET,
    CONTEXT_KEY_SETTINGS,
)
from ynab_cli.host.textual.application import App
from ynab_cli.host.textual.widgets.amazon import AMAZON_LIST_TRANSACTIONS_TAB_ID


async def _list_transactions(settings: Settings, quiet: bool) -> None:
    if not settings.amazon:
        raise click.UsageError("Amazon settings are missing")

    params: use_cases.ListTransactionsParams = {}

    app = App(
        settings,
        quiet,
        (AMAZON_LIST_TRANSACTIONS_TAB_ID, params),
    )
    await app.run_async()


@click.command()
@click.pass_context
def list_transactions(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(_list_transactions(ctx.obj[CONTEXT_KEY_SETTINGS], ctx.obj[CONTEXT_KEY_QUIET]))


@click.group()
@click.pass_context
def amazon(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


amazon.add_command(list_transactions)
