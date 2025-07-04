import anyio
import click
from lagom import Container

from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import categories as use_cases
from ynab_cli.host.click.commands.rich.progress_table import ProgressTable
from ynab_cli.host.click.container import containerize
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX


class ListUnusedCommand:
    def __init__(self, use_case: use_cases.ListUnused, progress_table: ProgressTable) -> None:
        self._use_case = use_case
        self._progress_table = progress_table

        self._progress_table.table.title = "Unused Categories"
        self._progress_table.table.add_column("Category Group ID")
        self._progress_table.table.add_column("Category Group Name")
        self._progress_table.table.add_column("Category ID")
        self._progress_table.table.add_column("Category Name")

    async def __call__(self, settings: Settings) -> None:
        params: use_cases.ListUnusedParams = {}

        console = None
        with self._progress_table:
            console = self._progress_table.console

            async for category in self._use_case(settings, params):
                self._progress_table.table.add_row(
                    str(category.category_group_id),
                    str(category.category_group_name),
                    str(category.id),
                    str(category.name),
                )

        if console:
            console.print(self._progress_table.table)


class ListAllCommand:
    def __init__(self, use_case: use_cases.ListAll, progress_table: ProgressTable) -> None:
        self._use_case = use_case
        self._progress_table = progress_table

        self._progress_table.table.title = "All Categories"
        self._progress_table.table.add_column("Category Group ID")
        self._progress_table.table.add_column("Category Group Name")
        self._progress_table.table.add_column("Category ID")
        self._progress_table.table.add_column("Category Name")

        self._progress = ProgressTable(self._progress_table.table)

    async def __call__(self, settings: Settings) -> None:
        params: use_cases.ListAllParams = {}

        console = None
        with self._progress:
            console = self._progress.console

            async for category in self._use_case(settings, params):
                self._progress_table.table.add_row(
                    str(category.category_group_id),
                    str(category.category_group_name),
                    str(category.id),
                    str(category.name),
                )

        if console:
            console.print(self._progress_table.table)


@containerize
async def _list_unused(container: Container) -> None:
    await container[ListUnusedCommand](container[Settings])


@click.command()
@click.pass_context
def list_unused(ctx: click.Context) -> None:
    """List unused categories in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    anyio.run(
        _list_unused,
        settings,
        backend_options={"use_uvloop": True},
    )


@containerize
async def _list_all(container: Container) -> None:
    await container[ListAllCommand](container[Settings])


@click.command()
@click.pass_context
def list_all(ctx: click.Context) -> None:
    """List all categories in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    anyio.run(
        _list_all,
        settings,
        backend_options={"use_uvloop": True},
    )


@click.group()
@click.option("--budget-id", prompt=True, envvar=f"{ENV_PREFIX}_BUDGET_ID", show_envvar=True, help="YNAB budget ID.")
@click.pass_context
def categories(ctx: click.Context, budget_id: str) -> None:
    """Manage YNAB categories in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    settings.ynab.budget_id = budget_id
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings


categories.add_command(list_all)
categories.add_command(list_unused)
