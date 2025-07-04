import anyio
import click
from lagom import Container

from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.click.commands.rich.progress_table import ProgressTable
from ynab_cli.host.click.container import containerize
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX


class NormalizeNamesCommand:
    def __init__(self, use_case: use_cases.NormalizeNames, progress_table: ProgressTable) -> None:
        self._use_case = use_case
        self._progress_table = progress_table

        self._progress_table.table.title = "Normalized Payees"
        self._progress_table.table.add_column("Payee Id")
        self._progress_table.table.add_column("Payee Name")
        self._progress_table.table.add_column("Normalized Name")

    async def __call__(self, settings: Settings) -> None:
        params: use_cases.NormalizeNamesParams = {}

        console = None
        with self._progress_table:
            console = self._progress_table.console

            async for payee, normalized_name in self._use_case(settings, params):
                self._progress_table.table.add_row(
                    str(payee.id),
                    payee.name,
                    normalized_name,
                )

        if console:
            console.print(self._progress_table.table)


class ListDuplicatesCommand:
    def __init__(self, use_case: use_cases.ListDuplicates, progress_table: ProgressTable) -> None:
        self._use_case = use_case
        self._progress_table = progress_table

        self._progress_table.table.title = "Duplicate Payees"
        self._progress_table.table.add_column("Payee Id")
        self._progress_table.table.add_column("Payee Name")
        self._progress_table.table.add_column("Duplicate Payee Id")
        self._progress_table.table.add_column("Duplicate Payee Name")

    async def __call__(self, settings: Settings) -> None:
        params: use_cases.ListDuplicatesParams = {}

        console = None
        with self._progress_table:
            console = self._progress_table.console

            async for payee, duplicate_payee in self._use_case(settings, params):
                self._progress_table.table.add_row(
                    str(payee.id),
                    payee.name,
                    str(duplicate_payee.id),
                    duplicate_payee.name,
                )

        if console:
            console.print(self._progress_table.table)


class ListUnusedCommand:
    def __init__(self, use_case: use_cases.ListUnused, progress_table: ProgressTable) -> None:
        self._use_case = use_case
        self._progress_table = progress_table

        self._progress_table.table.title = "Unused Payees"
        self._progress_table.table.add_column("Payee Id")
        self._progress_table.table.add_column("Payee Name")

    async def __call__(self, settings: Settings, prefix_unused: bool) -> None:
        params: use_cases.ListUnusedParams = {
            "prefix_unused": prefix_unused,
        }

        console = None
        with self._progress_table:
            console = self._progress_table.console

            async for payee in self._use_case(settings, params):
                self._progress_table.table.add_row(
                    str(payee.id),
                    payee.name,
                )

        if console:
            console.print(self._progress_table.table)


class ListAllCommand:
    def __init__(self, use_case: use_cases.ListAll, progress_table: ProgressTable) -> None:
        self._use_case = use_case
        self._progress_table = progress_table

        self._progress_table.table.title = "All Payees"
        self._progress_table.table.add_column("Payee Id")
        self._progress_table.table.add_column("Payee Name")

    async def __call__(self, settings: Settings) -> None:
        params: use_cases.ListAllParams = {}

        console = None
        with self._progress_table:
            console = self._progress_table.console

            async for payee in self._use_case(settings, params):
                self._progress_table.table.add_row(
                    str(payee.id),
                    payee.name,
                )

        if console:
            console.print(self._progress_table.table)


@containerize
async def _normalize_names(container: Container) -> None:
    await container[NormalizeNamesCommand](container[Settings])


@click.command()
@click.pass_context
def normalize_names(ctx: click.Context) -> None:
    """Normalize payee names in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    anyio.run(
        _normalize_names,
        settings,
        backend_options={"use_uvloop": True},
    )


@containerize
async def _list_duplicates(container: Container) -> None:
    await container[ListDuplicatesCommand](container[Settings])


@click.command()
@click.pass_context
def list_duplicates(ctx: click.Context) -> None:
    """List duplicate payees in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    anyio.run(
        _list_duplicates,
        settings,
        backend_options={"use_uvloop": True},
    )


@containerize
async def _list_unused(container: Container, prefix_unused: bool) -> None:
    await container[ListUnusedCommand](container[Settings], prefix_unused)


@click.command()
@click.option("--prefix-unused", is_flag=True, default=False, help="Add a prefix to the unused payee names.")
@click.pass_context
def list_unused(ctx: click.Context, prefix_unused: bool) -> None:
    """List unused payees in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings

    anyio.run(
        _list_unused,
        settings,
        prefix_unused,
        backend_options={"use_uvloop": True},
    )


@containerize
async def _list_all(container: Container) -> None:
    await container[ListAllCommand](container[Settings])


@click.command()
@click.pass_context
def list_all(ctx: click.Context) -> None:
    """List all payees in the YNAB budget."""

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
def payees(ctx: click.Context, budget_id: str) -> None:
    """Manage payees in the YNAB budget."""

    ctx.ensure_object(dict)
    settings: Settings = ctx.obj.get(CONTEXT_KEY_SETTINGS, Settings())
    settings.ynab.budget_id = budget_id
    ctx.obj[CONTEXT_KEY_SETTINGS] = settings


payees.add_command(list_all)
payees.add_command(list_duplicates)
payees.add_command(list_unused)
payees.add_command(normalize_names)
