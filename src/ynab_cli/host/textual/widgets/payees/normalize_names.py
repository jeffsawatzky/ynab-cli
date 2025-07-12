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


class NormalizeNamesParamsDialogForm(DialogForm[use_cases.NormalizeNamesParams]):
    def __init__(self, params: use_cases.NormalizeNamesParams, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._params: use_cases.NormalizeNamesParams = {**params}

    @override
    def compose(self) -> ComposeResult:
        yield Checkbox("Dry Run", self._params["dry_run"], id="dry_run")

    @override
    async def get_result(self) -> use_cases.NormalizeNamesParams:
        return {
            "dry_run": self.query_one("#dry_run", Checkbox).value,
        }


class NormalizeNamesCommand(CommandWidget):
    def __init__(self) -> None:
        super().__init__()
        self._params: use_cases.NormalizeNamesParams = {
            "dry_run": False,
        }

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
            "Normalized Name",
        )

    @override
    async def _get_command_params(self) -> None:
        result = await self.app.push_screen_wait(
            SaveCancelDialogScreen(
                NormalizeNamesParamsDialogForm(self._params), title="Payees: Normalize Names Parameters"
            )
        )
        if result is not CANCELLED:
            self._params = result

    @override
    async def _run_command(self) -> None:
        params: use_cases.NormalizeNamesParams = {
            "dry_run": False,
        }

        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for payee, normalized_name in use_cases.NormalizeNames(
            TextualIO(self.app, log, progress_bar), cast("YnabCliApp", self.app).client
        )(self.settings, params):
            table.add_row(
                payee.id,
                payee.name,
                normalized_name,
            )
