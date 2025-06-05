import logging

import click
from rich.logging import RichHandler

from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.click.commands import categories, payees, transactions
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX


@click.group()
@click.option("--access-token", prompt=True, hide_input=True, envvar=f"{ENV_PREFIX}_ACCESS_TOKEN", show_envvar=True)
@click.option("--budget-id", prompt=True, envvar=f"{ENV_PREFIX}_BUDGET_ID", show_envvar=True)
@click.pass_context
def run(
    ctx: click.Context,
    access_token: str,
    budget_id: str,
) -> None:
    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    settings.ynab = YnabSettings(access_token=access_token, budget_id=budget_id)
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    logging.basicConfig(
        level="DEBUG" if settings.debug else "WARNING",  # NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()],
    )


run.add_command(payees.payees)
run.add_command(categories.categories)
run.add_command(transactions.transactions)
