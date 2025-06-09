import json
from pathlib import Path

from textual import work
from textual.app import ComposeResult
from textual.widgets import DataTable, Log, ProgressBar, TabbedContent, TabPane
from textual_fspicker import FileOpen
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.models import rules
from ynab_cli.domain.use_cases import transactions as use_cases
from ynab_cli.host.textual.widgets.common.base_command import BaseCommand
from ynab_cli.host.textual.widgets.common.runnable_widget import RunnableWidget


class TransactionsTabs(RunnableWidget):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Transactions", id="transactions"):
                yield TransactionsApplyRulesCommand().data_bind(settings=TransactionsTabs.settings)

    @override
    async def run_command(self) -> None:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "transactions":
                await self.query_one(TransactionsApplyRulesCommand).run_command()


class TransactionsApplyRulesCommand(BaseCommand[use_cases.ApplyRulesParams]):
    def __init__(self) -> None:
        super().__init__()
        self._transaction_rules_path: Path | None = None

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
    async def run_command(self) -> None:
        self._select_rules_worker()

    @work(exclusive=True)
    async def _select_rules_worker(self) -> None:
        self._transaction_rules_path = await self.app.push_screen_wait(
            FileOpen(title="Select Transaction Rules JSON File", default_file=self._transaction_rules_path)
        )
        if not self._transaction_rules_path:
            return

        try:
            transaction_rules_json = json.loads(self._transaction_rules_path.read_text())
            transaction_rules = rules.TransactionRules.from_dict(transaction_rules_json)
        except Exception as e:
            self.query_one(Log).write_line(f"Error loading rules: {e}")
            return

        params: use_cases.ApplyRulesParams = {
            "transaction_rules": transaction_rules,
        }
        self._run_command_worker(params)

    @override
    async def _run_command(self, use_case_params: use_cases.ApplyRulesParams) -> None:
        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for transaction, save_transaction in use_cases.apply_rules(
            self.settings, TextualIO(self.app, log, progress_bar), use_case_params
        ):
            table.add_row(
                transaction.id,
                transaction.date.isoformat(),
                transaction.payee_name,
                transaction.category_name,
                transaction.memo,
                str(transaction.amount),
                str(save_transaction.to_dict()),
            )
