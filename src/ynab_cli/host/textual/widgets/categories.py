import logging
from typing import ClassVar

from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import DataTable, Log, TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualWorkerIO
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import categories as use_cases
from ynab_cli.host.textual.types import (
    CategoriesListAllTabId,
    CategoriesListUnusedTabId,
    CategoriesTabId,
    CommandParams,
)
from ynab_cli.host.textual.widgets import BaseCommand, CommandRunnableWidget

log = logging.getLogger(__name__)

CATEGORIES_TAB_ID: CategoriesTabId = "categories"
CATEGORIES_LIST_UNUSED_TAB_ID: CategoriesListUnusedTabId = (CATEGORIES_TAB_ID, "list_unused")
CATEGORIES_LIST_ALL_TAB_ID: CategoriesListAllTabId = (CATEGORIES_TAB_ID, "list_all")


class CategoriesTabs(CommandRunnableWidget):
    settings: var[Settings] = var(Settings())

    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Unused", id=CATEGORIES_LIST_UNUSED_TAB_ID[1]):
                yield CategoriesListUnusedCommand().data_bind(settings=CategoriesTabs.settings)
            with TabPane("All", id=CATEGORIES_LIST_ALL_TAB_ID[1]):
                yield CategoriesListAllCommand().data_bind(settings=CategoriesTabs.settings)

    @override
    def run_command(self, params: CommandParams) -> None:
        active_tab_id, _ = params
        if active_tab_id == CATEGORIES_LIST_UNUSED_TAB_ID:
            self.query_one(TabbedContent).active = CATEGORIES_LIST_UNUSED_TAB_ID[1]
            self.query_one(CategoriesListUnusedCommand).run_command(params)
        elif active_tab_id == CATEGORIES_LIST_ALL_TAB_ID:
            self.query_one(TabbedContent).active = CATEGORIES_LIST_ALL_TAB_ID[1]
            self.query_one(CategoriesListAllCommand).run_command(params)


class CategoriesListUnusedCommand(BaseCommand[use_cases.ListUnusedParams]):
    ACTIVE_TAB_ID: ClassVar[CategoriesListUnusedTabId] = CATEGORIES_LIST_UNUSED_TAB_ID

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Category Group Id",
            "Category Group Name",
            "Category Id",
            "Category Name",
        )

    @override
    async def _run_command(self, use_case_params: use_cases.ListUnusedParams) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for category in use_cases.list_unused(self.settings, TextualWorkerIO(self.app, log), use_case_params):
            table.add_row(
                category.category_group_id,
                category.category_group_name,
                category.id,
                category.name,
            )


class CategoriesListAllCommand(BaseCommand[use_cases.ListAllParams]):
    ACTIVE_TAB_ID: ClassVar[CategoriesListAllTabId] = CATEGORIES_LIST_ALL_TAB_ID

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Category Group Id",
            "Category Group Name",
            "Category Id",
            "Category Name",
        )

    @override
    async def _run_command(self, use_case_params: use_cases.ListAllParams) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for category in use_cases.list_all(self.settings, TextualWorkerIO(self.app, log), use_case_params):
            table.add_row(
                category.category_group_id,
                category.category_group_name,
                category.id,
                category.name,
            )
