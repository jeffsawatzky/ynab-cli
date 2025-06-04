import asyncio

import click

from ynab_cli.domain.use_cases import categories as use_cases
from ynab_cli.host.cli.constants import CONTEXT_KEY_ACCESS_TOKEN, CONTEXT_KEY_BUDGET_ID


@click.command()
@click.pass_context
def list_unused(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(
        use_cases.list_unused(
            ctx.obj[CONTEXT_KEY_ACCESS_TOKEN],
            ctx.obj[CONTEXT_KEY_BUDGET_ID],
        )
    )


@click.command()
@click.pass_context
def list_all(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(
        use_cases.list_all(
            ctx.obj[CONTEXT_KEY_ACCESS_TOKEN],
            ctx.obj[CONTEXT_KEY_BUDGET_ID],
        )
    )


@click.group()
@click.pass_context
def categories(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


categories.add_command(list_unused)
categories.add_command(list_all)
