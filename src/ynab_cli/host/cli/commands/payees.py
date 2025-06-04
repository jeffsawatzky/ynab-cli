import asyncio

import click

from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.cli.constants import CONTEXT_KEY_ACCESS_TOKEN, CONTEXT_KEY_BUDGET_ID, CONTEXT_KEY_DRY_RUN


@click.command()
@click.pass_context
def normalize_names(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(
        use_cases.normalize_names(
            ctx.obj[CONTEXT_KEY_ACCESS_TOKEN],
            ctx.obj[CONTEXT_KEY_BUDGET_ID],
            ctx.obj[CONTEXT_KEY_DRY_RUN],
        )
    )


@click.command()
@click.pass_context
def list_duplicates(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    asyncio.run(
        use_cases.list_duplicates(
            ctx.obj[CONTEXT_KEY_ACCESS_TOKEN],
            ctx.obj[CONTEXT_KEY_BUDGET_ID],
        )
    )


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


@click.group()
@click.pass_context
def payees(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


payees.add_command(normalize_names)
payees.add_command(list_duplicates)
payees.add_command(list_unused)
