import json
from typing import TYPE_CHECKING, Any, cast

from textual import on, work
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, DataTable, Log, Pretty, ProgressBar
from textual_fspicker import FileOpen
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.models import rules
from ynab_cli.domain.use_cases import transactions as use_cases
from ynab_cli.host.textual.widgets.common.command_widget import CommandWidget
from ynab_cli.host.textual.widgets.common.dialogs import CANCELLED, DialogForm, SaveCancelDialogScreen

if TYPE_CHECKING:
    from ynab_cli.host.textual.app import YnabCliApp


class ApplyRulesParamsDialogForm(DialogForm[use_cases.ApplyRulesParams]):
    def __init__(self, params: use_cases.ApplyRulesParams, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._params: use_cases.ApplyRulesParams = {**params}

    @override
    def compose(self) -> ComposeResult:
        yield Button("Select Transaction Rules JSON File", id="select_rules", variant="primary")
        with ScrollableContainer():
            yield Pretty(self._params["transaction_rules"].to_dict())

    @on(Button.Pressed, "#select_rules")
    async def _select_rules_button_pressed(self, _: Button.Pressed) -> None:
        self._select_rules_worker()

    @work(exclusive=True)
    async def _select_rules_worker(self) -> None:
        self._transaction_rules_path = await self.app.push_screen_wait(
            FileOpen(title="Select Transaction Rules JSON File")
        )
        if not self._transaction_rules_path:
            return

        try:
            transaction_rules_json = json.loads(self._transaction_rules_path.read_text())
            self._params["transaction_rules"] = rules.TransactionRules.from_dict(transaction_rules_json)
            self.query_one(Pretty).update(self._params["transaction_rules"].to_dict())
        except Exception as e:
            self.query_one(Log).write_line(f"Error loading rules: {e}")
            return

    @override
    async def get_result(self) -> use_cases.ApplyRulesParams:
        return {
            "transaction_rules": self._params["transaction_rules"],
        }


class ApplyRulesCommand(CommandWidget):
    def __init__(self) -> None:
        super().__init__()
        self._params: use_cases.ApplyRulesParams = {
            "transaction_rules": rules.TransactionRules(transaction_rules=[]),
        }

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
    async def _get_command_params(self) -> None:
        result = await self.app.push_screen_wait(
            SaveCancelDialogScreen(
                ApplyRulesParamsDialogForm(self._params), title="Transactions: Apply Rules Parameters"
            )
        )
        if result is not CANCELLED:
            self._params = result

    @override
    async def _run_command(self) -> None:
        if not self._params["transaction_rules"].transaction_rules:
            await self.get_command_params()

            if not self._params["transaction_rules"].transaction_rules:
                return

        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for transaction, save_transaction in use_cases.ApplyRules(
            TextualIO(self.app, log, progress_bar), cast("YnabCliApp", self.app).client
        )(self.settings, self._params):
            table.add_row(
                transaction.id,
                transaction.date.isoformat(),
                transaction.payee_name,
                transaction.category_name,
                transaction.memo,
                str(transaction.amount),
                str(save_transaction.to_dict()),
            )
