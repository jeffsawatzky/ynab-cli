from typing import Any, ClassVar

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.widgets import Checkbox, DataTable, Log, ProgressBar
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.textual.widgets.common.base_command import BaseCommand
from ynab_cli.host.textual.widgets.common.dialogs import CANCELLED, DialogForm, SaveCancelDialogScreen


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


class ListUnusedCommand(BaseCommand[use_cases.ListUnusedParams]):
    BINDINGS: ClassVar[list[BindingType]] = [Binding("p", "parameters", "Parameters", show=True, priority=False)]

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

    async def action_parameters(self) -> None:
        self._get_parameters()

    @work(exclusive=True)
    async def _get_parameters(self) -> None:
        result = await self.app.push_screen_wait(
            SaveCancelDialogScreen(ListUnusedParamsDialogForm(self._params), title="Payees: List Unused Parameters")
        )
        if result is not CANCELLED:
            self._params = result

    @override
    async def run_command(self) -> None:
        self._run_command_worker(self._params)

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
