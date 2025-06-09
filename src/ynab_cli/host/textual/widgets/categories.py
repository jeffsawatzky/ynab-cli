from textual.app import ComposeResult
from textual.widgets import DataTable, Log, ProgressBar, TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.use_cases import categories as use_cases
from ynab_cli.host.textual.widgets.common.base_command import BaseCommand
from ynab_cli.host.textual.widgets.common.runnable_widget import RunnableWidget


class CategoriesTabs(RunnableWidget):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Unused", id="unused"):
                yield CategoriesListUnusedCommand().data_bind(settings=CategoriesTabs.settings)
            with TabPane("All", id="all"):
                yield CategoriesListAllCommand().data_bind(settings=CategoriesTabs.settings)

    @override
    async def run_command(self) -> None:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "unused":
                await self.query_one(CategoriesListUnusedCommand).run_command()
            elif tabbed_content.active_pane.id == "all":
                await self.query_one(CategoriesListAllCommand).run_command()


class CategoriesListUnusedCommand(BaseCommand[use_cases.ListUnusedParams]):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Category Group Id",
            "Category Group Name",
            "Category Id",
            "Category Name",
        )

    @override
    async def run_command(self) -> None:
        params: use_cases.ListUnusedParams = {}
        self._run_command_worker(params)

    @override
    async def _run_command(self, use_case_params: use_cases.ListUnusedParams) -> None:
        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for category in use_cases.list_unused(
            self.settings, TextualIO(self.app, log, progress_bar), use_case_params
        ):
            table.add_row(
                category.category_group_id,
                category.category_group_name,
                category.id,
                category.name,
            )


class CategoriesListAllCommand(BaseCommand[use_cases.ListAllParams]):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Category Group Id",
            "Category Group Name",
            "Category Id",
            "Category Name",
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

        async for category in use_cases.list_all(
            self.settings, TextualIO(self.app, log, progress_bar), use_case_params
        ):
            table.add_row(
                category.category_group_id,
                category.category_group_name,
                category.id,
                category.name,
            )
