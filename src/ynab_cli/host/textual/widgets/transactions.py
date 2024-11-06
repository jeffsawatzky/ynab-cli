import logging
from typing import ClassVar

from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import DataTable, Log, TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualWorkerIO
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import transactions as use_cases
from ynab_cli.host.textual.types import CommandParams, TransactionsApplyRulesTabId, TransactionsTabId
from ynab_cli.host.textual.widgets import BaseCommand, CommandRunnableWidget

log = logging.getLogger(__name__)

TRANSACTIONS_TAB_ID: TransactionsTabId = "transactions"
TRANSACTIONS_APPLY_RULES_TAB_ID: TransactionsApplyRulesTabId = (TRANSACTIONS_TAB_ID, "apply_rules")


class TransactionsTabs(CommandRunnableWidget):
    settings: var[Settings] = var(Settings())

    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Transactions", id=TRANSACTIONS_APPLY_RULES_TAB_ID[1]):
                yield TransactionsApplyRulesCommand().data_bind(settings=TransactionsTabs.settings)

    @override
    def run_command(self, params: CommandParams) -> None:
        active_tab_id, _ = params
        if active_tab_id == TRANSACTIONS_APPLY_RULES_TAB_ID:
            self.query_one(TabbedContent).active = TRANSACTIONS_APPLY_RULES_TAB_ID[1]
            self.query_one(TransactionsApplyRulesCommand).run_command(params)


class TransactionsApplyRulesCommand(BaseCommand[use_cases.ApplyRulesParams]):
    ACTIVE_TAB_ID: ClassVar[TransactionsApplyRulesTabId] = TRANSACTIONS_APPLY_RULES_TAB_ID

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Transaction Id",
            "Transaction Date",
            "Transaction Payee",
            "Transaction Category",
            "Transaction Memo",
            "Transaction Amount",
            "Transaction Changes",
        )

    @override
    async def _run_command(self, use_case_params: use_cases.ApplyRulesParams) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for transaction, save_transaction in use_cases.apply_rules(
            self.settings, TextualWorkerIO(self.app, log), use_case_params
        ):
            table.add_row(
                transaction.id,
                transaction.var_date.isoformat(),
                transaction.payee_name,
                transaction.category_name,
                transaction.memo,
                str(transaction.amount),
                str(save_transaction.to_dict()),
            )
