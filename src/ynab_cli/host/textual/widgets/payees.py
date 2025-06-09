from textual.app import ComposeResult
from textual.widgets import DataTable, Log, ProgressBar, TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.textual.widgets.common.base_command import BaseCommand
from ynab_cli.host.textual.widgets.common.runnable_widget import RunnableWidget


class PayeesTabs(RunnableWidget):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Normalize", id="normalize"):
                yield PayeesNormalizeNamesCommand().data_bind(settings=PayeesTabs.settings)
            with TabPane("Duplicates", id="duplicates"):
                yield PayeesListDuplicatesCommand().data_bind(settings=PayeesTabs.settings)
            with TabPane("Unused", id="unused"):
                yield PayeesListUnusedCommand().data_bind(settings=PayeesTabs.settings)
            with TabPane("All", id="all"):
                yield PayeesListAllCommand().data_bind(settings=PayeesTabs.settings)

    @override
    async def run_command(self) -> None:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "normalize":
                await self.query_one(PayeesNormalizeNamesCommand).run_command()
            elif tabbed_content.active_pane.id == "duplicates":
                await self.query_one(PayeesListDuplicatesCommand).run_command()
            elif tabbed_content.active_pane.id == "unused":
                await self.query_one(PayeesListUnusedCommand).run_command()
            elif tabbed_content.active_pane.id == "all":
                await self.query_one(PayeesListAllCommand).run_command()


class PayeesNormalizeNamesCommand(BaseCommand[use_cases.NormalizeNamesParams]):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
            "Normalized Name",
        )

    @override
    async def run_command(self) -> None:
        params: use_cases.NormalizeNamesParams = {}
        self._run_command_worker(params)

    @override
    async def _run_command(self, use_case_params: use_cases.NormalizeNamesParams) -> None:
        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee, normalized_name in use_cases.normalize_names(
            self.settings, TextualIO(self.app, log, progress_bar), use_case_params
        ):
            table.add_row(
                payee.id,
                payee.name,
                normalized_name,
            )


class PayeesListDuplicatesCommand(BaseCommand[use_cases.ListDuplicatesParams]):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
            "Duplicate Payee Id",
            "Duplicate Payee Name",
        )

    @override
    async def run_command(self) -> None:
        params: use_cases.ListDuplicatesParams = {}
        self._run_command_worker(params)

    @override
    async def _run_command(self, use_case_params: use_cases.ListDuplicatesParams) -> None:
        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee, duplicate_payee in use_cases.list_duplicates(
            self.settings, TextualIO(self.app, log, progress_bar), use_case_params
        ):
            table.add_row(
                payee.id,
                payee.name,
                duplicate_payee.id,
                duplicate_payee.name,
            )


class PayeesListUnusedCommand(BaseCommand[use_cases.ListUnusedParams]):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
        )

    @override
    async def run_command(self) -> None:
        params: use_cases.ListUnusedParams = {
            "prefix_unused": False,  # Default to not prefixing unused payees
        }
        self._run_command_worker(params)

    @override
    async def _run_command(self, use_case_params: use_cases.ListUnusedParams) -> None:
        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee in use_cases.list_unused(
            self.settings, TextualIO(self.app, log, progress_bar), use_case_params
        ):
            table.add_row(
                payee.id,
                payee.name,
            )


class PayeesListAllCommand(BaseCommand[use_cases.ListAllParams]):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
        )

    @override
    async def run_command(self) -> None:
        params: use_cases.ListAllParams = {}
        self._run_command_worker(params)

    @override
    async def _run_command(self, use_case_params: use_cases.ListAllParams) -> None:
        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee in use_cases.list_all(self.settings, TextualIO(self.app, log, progress_bar), use_case_params):
            table.add_row(
                payee.id,
                payee.name,
            )
