import logging

import anyio
import click
from lagom import Container
from textual.logging import TextualHandler

from ynab_cli.adapters.ynab.client import AuthenticatedClient
from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX
from ynab_cli.host.textual.app import YnabCliApp
from ynab_cli.host.textual.container import containerize


@containerize
async def _tui(container: Container) -> None:
    async with container[AuthenticatedClient]:
        await container[YnabCliApp].run_async()


@click.command()
@click.option(
    "--access-token", default="", envvar=f"{ENV_PREFIX}_ACCESS_TOKEN", show_envvar=True, help="YNAB API access token."
)
@click.option("--budget-id", default="", envvar=f"{ENV_PREFIX}_BUDGET_ID", show_envvar=True, help="YNAB budget ID.")
@click.pass_context
def tui(
    ctx: click.Context,
    access_token: str,
    budget_id: str,
) -> None:
    """Run the Textual User Interface (TUI) for YNAB CLI."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    settings.ynab = YnabSettings(access_token=access_token, budget_id=budget_id)

    logging.basicConfig(
        level="DEBUG" if settings.debug else "WARNING",  # NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(message)s",
        datefmt="[%X]",
        handlers=[TextualHandler()],
    )

    anyio.run(
        _tui,
        settings,
        backend_options={"use_uvloop": True},
    )
