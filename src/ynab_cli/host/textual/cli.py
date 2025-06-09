import asyncio
import logging

import click
from textual.logging import TextualHandler

from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX
from ynab_cli.host.textual.app import YnabCliApp


async def _tui(settings: Settings) -> None:
    app = YnabCliApp(settings)
    await app.run_async()


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
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    logging.basicConfig(
        level="DEBUG" if settings.debug else "WARNING",  # NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(message)s",
        datefmt="[%X]",
        handlers=[TextualHandler()],
    )

    asyncio.run(_tui(ctx.obj[CONTEXT_KEY_SETTINGS]))
