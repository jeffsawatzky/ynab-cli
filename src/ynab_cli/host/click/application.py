import logging

import click
from textual.logging import TextualHandler

from ynab_cli.adapters.amazon.constants import DEFAULT_AMAZON_HOST
from ynab_cli.domain.settings import AmazonSettings, Settings, YnabSettings
from ynab_cli.host.click.commands import amazon, categories, payees, transactions
from ynab_cli.host.click.constants import (
    CONTEXT_KEY_QUIET,
    CONTEXT_KEY_SETTINGS,
    ENV_PREFIX,
)


@click.group()
@click.option("--access-token", prompt=True, hide_input=True, show_envvar=True)
@click.option("--budget-id", prompt=True, show_envvar=True)
@click.option("--amazon-username", show_envvar=True)
@click.option("--amazon-password", hide_input=True, show_envvar=True)
@click.option("--amazon-host", show_envvar=True, default=DEFAULT_AMAZON_HOST, show_default=True)
@click.option("--quiet", is_flag=True, default=False)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--debug", is_flag=True, default=False)
@click.pass_context
def cli(
    ctx: click.Context,
    access_token: str,
    budget_id: str,
    amazon_username: str | None,
    amazon_password: str | None,
    amazon_host: str,
    quiet: bool,
    dry_run: bool,
    debug: bool,
) -> None:
    logging.basicConfig(
        level="DEBUG" if debug else "WARNING",  # NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(message)s",
        datefmt="[%X]",
        handlers=[TextualHandler()],
    )

    ctx.ensure_object(dict)

    ynab_settings = YnabSettings(access_token=access_token, budget_id=budget_id)
    amazon_settings = (
        AmazonSettings(username=amazon_username, password=amazon_password, host=amazon_host)
        if amazon_username and amazon_password and amazon_host
        else None
    )
    settings = Settings(dry_run=dry_run, ynab=ynab_settings, amazon=amazon_settings)

    ctx.obj[CONTEXT_KEY_SETTINGS] = settings
    ctx.obj[CONTEXT_KEY_QUIET] = quiet


cli.add_command(payees.payees)
cli.add_command(categories.categories)
cli.add_command(transactions.transactions)
cli.add_command(amazon.amazon)


def main() -> None:
    cli(
        auto_envvar_prefix=ENV_PREFIX,
        obj={},  # click context object
    )


if __name__ == "__main__":
    main()
