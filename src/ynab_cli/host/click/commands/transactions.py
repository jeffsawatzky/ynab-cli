import asyncio
import json
from typing import IO, Any

import click

from ynab_cli.domain.models import rules
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import transactions as use_cases
from ynab_cli.host.click.constants import (
    CONTEXT_KEY_QUIET,
    CONTEXT_KEY_SETTINGS,
)
from ynab_cli.host.textual.application import App
from ynab_cli.host.textual.widgets.transactions import TRANSACTIONS_APPLY_RULES_TAB_ID


async def _apply_rules(settings: Settings, quiet: bool, transaction_rules: rules.TransactionRules) -> None:
    params: use_cases.ApplyRulesParams = {
        "transaction_rules": transaction_rules,
    }

    app = App(
        settings,
        quiet,
        (TRANSACTIONS_APPLY_RULES_TAB_ID, params),
    )
    await app.run_async()


@click.command()
@click.argument("rules-file", type=click.File())
@click.pass_context
def apply_rules(
    ctx: click.Context, rules_file: IO[Any], amazon_username: str | None, amazon_password: str | None, amazon_host: str
) -> None:
    ctx.ensure_object(dict)

    transaction_rules = rules.TransactionRules.model_validate(json.load(rules_file))

    asyncio.run(_apply_rules(ctx.obj[CONTEXT_KEY_SETTINGS], ctx.obj[CONTEXT_KEY_QUIET], transaction_rules))


@click.group()
@click.pass_context
def transactions(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


transactions.add_command(apply_rules)
