import asyncio
import json

import click

from ynab_cli.domain.models import rules
from ynab_cli.domain.use_cases import transactions as use_cases
from ynab_cli.host.cli.constants import CONTEXT_KEY_ACCESS_TOKEN, CONTEXT_KEY_BUDGET_ID, CONTEXT_KEY_DRY_RUN


@click.command()
@click.argument("rules-file", type=click.File())
@click.pass_context
def apply_rules(ctx: click.Context, rules_file: click.File) -> None:
    ctx.ensure_object(dict)

    transaction_rules = rules.TransactionRules.model_validate(json.load(rules_file))

    asyncio.run(
        use_cases.apply_rules(
            ctx.obj[CONTEXT_KEY_ACCESS_TOKEN],
            ctx.obj[CONTEXT_KEY_BUDGET_ID],
            ctx.obj[CONTEXT_KEY_DRY_RUN],
            transaction_rules,
        )
    )


@click.group()
@click.pass_context
def transactions(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


transactions.add_command(apply_rules)
