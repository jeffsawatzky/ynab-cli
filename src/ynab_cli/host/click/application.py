import logging

import click
from rich.logging import RichHandler

from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.click.commands import categories, payees, transactions
from ynab_cli.host.click.constants import (
    CONTEXT_KEY_SETTINGS,
    ENV_PREFIX,
)


@click.group()
@click.option("--access-token", prompt=True, hide_input=True, show_envvar=True)
@click.option("--budget-id", prompt=True, show_envvar=True)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--debug", is_flag=True, default=False)
@click.pass_context
def cli(
    ctx: click.Context,
    access_token: str,
    budget_id: str,
    dry_run: bool,
    debug: bool,
) -> None:
    logging.basicConfig(
        level="DEBUG" if debug else "WARNING",  # NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()],
    )

    ctx.ensure_object(dict)

    ynab_settings = YnabSettings(access_token=access_token, budget_id=budget_id)

    settings = Settings(dry_run=dry_run, ynab=ynab_settings)

    ctx.obj[CONTEXT_KEY_SETTINGS] = settings


cli.add_command(payees.payees)
cli.add_command(categories.categories)
cli.add_command(transactions.transactions)


def main() -> None:
    cli(
        auto_envvar_prefix=ENV_PREFIX,
        obj={},  # click context object
    )


if __name__ == "__main__":
    main()
