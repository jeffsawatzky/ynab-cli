from typing import TYPE_CHECKING, cast

from textual.widgets import DataTable, Log, ProgressBar
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.textual.widgets.common.command_widget import CommandWidget

if TYPE_CHECKING:
    from ynab_cli.host.textual.app import YnabCliApp


class NormalizeNamesCommand(CommandWidget):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
            "Normalized Name",
        )

    @override
    async def _run_command(self) -> None:
        params: use_cases.NormalizeNamesParams = {}

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
