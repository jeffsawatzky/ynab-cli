import anyio
import click
from lagom import Container

from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import budgets as use_cases
from ynab_cli.host.click.commands.rich.progress_table import ProgressTable
from ynab_cli.host.click.container import containerize
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS


class ListAllCommand:
    def __init__(self, use_case: use_cases.ListAll, progress_table: ProgressTable) -> None:
        self._use_case = use_case
        self._progress_table = progress_table

        self._progress_table.table.title = "All Budgets"
        self._progress_table.table.add_column("Budget ID")
        self._progress_table.table.add_column("Budget Name")

    async def __call__(self, settings: Settings) -> None:
        params: use_cases.ListAllParams = {}

        console = None
        with self._progress_table:
            console = self._progress_table.console

            async for budget in self._use_case(settings, params):
                self._progress_table.table.add_row(
                    str(budget.id),
                    str(budget.name),
                )

        if console:
            console.print(self._progress_table.table)


@containerize
async def _list_all(container: Container) -> None:
    await container[ListAllCommand](container[Settings])


@click.command()
@click.pass_context
def list_all(ctx: click.Context) -> None:
    """List all budgets in YNAB."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    anyio.run(
        _list_all,
        settings,
        backend_options={"use_uvloop": True},
    )


@click.group()
@click.pass_context
def budgets(ctx: click.Context) -> None:
    """Manage YNAB budgets in YNAB."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings


budgets.add_command(list_all)
