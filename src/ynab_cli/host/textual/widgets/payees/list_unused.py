from typing import TYPE_CHECKING, Any, cast

from textual.app import ComposeResult
from textual.widgets import Checkbox, DataTable, Log, ProgressBar
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.textual.widgets.common.command_widget import CommandWidget
from ynab_cli.host.textual.widgets.common.dialogs import CANCELLED, DialogForm, SaveCancelDialogScreen

if TYPE_CHECKING:
    from ynab_cli.host.textual.app import YnabCliApp


class ListUnusedParamsDialogForm(DialogForm[use_cases.ListUnusedParams]):
    def __init__(self, params: use_cases.ListUnusedParams, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._params: use_cases.ListUnusedParams = {**params}

    @override
    def compose(self) -> ComposeResult:
        yield Checkbox("Prefix Unused Payees", self._params["prefix_unused"], id="prefix_unused")

    @override
    async def get_result(self) -> use_cases.ListUnusedParams:
        return {
            "prefix_unused": self.query_one(Checkbox).value,
        }


class ListUnusedCommand(CommandWidget):
    def __init__(self) -> None:
        super().__init__()
        self._params: use_cases.ListUnusedParams = {
            "prefix_unused": False,  # Default to not prefixing unused payees
        }

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
        )

    @override
    async def _get_command_params(self) -> None:
        result = await self.app.push_screen_wait(
            SaveCancelDialogScreen(ListUnusedParamsDialogForm(self._params), title="Payees: List Unused Parameters")
        )
        if result is not CANCELLED:
            self._params = result

    @override
    async def _run_command(self) -> None:
        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee in use_cases.ListUnused(
            TextualIO(self.app, log, progress_bar), cast("YnabCliApp", self.app).client
        )(self.settings, self._params):
            table.add_row(
                payee.id,
                payee.name,
            )
