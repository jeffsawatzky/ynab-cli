import logging
from typing import ClassVar

from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import DataTable, Log, TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualWorkerIO
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.textual.types import (
    CommandParams,
    PayeesListDuplicatesTabId,
    PayeesListUnusedTabId,
    PayeesNormalizeNamesTabId,
    PayeesTabId,
)
from ynab_cli.host.textual.widgets import BaseCommand, CommandRunnableWidget

log = logging.getLogger(__name__)

PAYEES_TAB_ID: PayeesTabId = "payees"
PAYEES_NORMALIZE_NAMES_TAB_ID: PayeesNormalizeNamesTabId = (PAYEES_TAB_ID, "normalize_names")
PAYEES_LIST_DUPLICATES_TAB_ID: PayeesListDuplicatesTabId = (PAYEES_TAB_ID, "list_duplicates")
PAYEES_LIST_UNUSED_TAB_ID: PayeesListUnusedTabId = (PAYEES_TAB_ID, "list_unused")


class PayeesTabs(CommandRunnableWidget):
    settings: var[Settings] = var(Settings())

    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Normalize", id=PAYEES_NORMALIZE_NAMES_TAB_ID[1]):
                yield PayeesNormalizeNamesCommand().data_bind(settings=PayeesTabs.settings)
            with TabPane("Duplicates", id=PAYEES_LIST_DUPLICATES_TAB_ID[1]):
                yield PayeesListDuplicatesCommand().data_bind(settings=PayeesTabs.settings)
            with TabPane("Unused", id=PAYEES_LIST_UNUSED_TAB_ID[1]):
                yield PayeesListUnusedCommand().data_bind(settings=PayeesTabs.settings)

    @override
    def run_command(self, params: CommandParams) -> None:
        active_tab_id, _ = params
        if active_tab_id == PAYEES_NORMALIZE_NAMES_TAB_ID:
            self.query_one(TabbedContent).active = PAYEES_NORMALIZE_NAMES_TAB_ID[1]
            self.query_one(PayeesNormalizeNamesCommand).run_command(params)
        elif active_tab_id == PAYEES_LIST_DUPLICATES_TAB_ID:
            self.query_one(TabbedContent).active = PAYEES_LIST_DUPLICATES_TAB_ID[1]
            self.query_one(PayeesListDuplicatesCommand).run_command(params)
        elif active_tab_id == PAYEES_LIST_UNUSED_TAB_ID:
            self.query_one(TabbedContent).active = PAYEES_LIST_UNUSED_TAB_ID[1]
            self.query_one(PayeesListUnusedCommand).run_command(params)


class PayeesNormalizeNamesCommand(BaseCommand[use_cases.NormalizeNamesParams]):
    ACTIVE_TAB_ID: ClassVar[PayeesNormalizeNamesTabId] = PAYEES_NORMALIZE_NAMES_TAB_ID

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
            "Normalized Name",
        )

    @override
    async def _run_command(self, use_case_params: use_cases.NormalizeNamesParams) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee, normalized_name in use_cases.normalize_names(
            self.settings, TextualWorkerIO(self.app, log), use_case_params
        ):
            table.add_row(
                payee.id,
                payee.name,
                normalized_name,
            )


class PayeesListDuplicatesCommand(BaseCommand[use_cases.ListDuplicatesParams]):
    ACTIVE_TAB_ID: ClassVar[PayeesListDuplicatesTabId] = PAYEES_LIST_DUPLICATES_TAB_ID

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
            "Duplicate Payee Id",
            "Duplicate Payee Name",
        )

    @override
    async def _run_command(self, use_case_params: use_cases.ListDuplicatesParams) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee, duplicate_payee in use_cases.list_duplicates(
            self.settings, TextualWorkerIO(self.app, log), use_case_params
        ):
            table.add_row(
                payee.id,
                payee.name,
                duplicate_payee.id,
                duplicate_payee.name,
            )


class PayeesListUnusedCommand(BaseCommand[use_cases.ListUnusedParams]):
    ACTIVE_TAB_ID: ClassVar[PayeesListUnusedTabId] = PAYEES_LIST_UNUSED_TAB_ID

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
        )

    @override
    async def _run_command(self, use_case_params: use_cases.ListUnusedParams) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee in use_cases.list_unused(self.settings, TextualWorkerIO(self.app, log), use_case_params):
            table.add_row(
                payee.id,
                payee.name,
            )
