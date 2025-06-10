from textual.widgets import DataTable, Log, ProgressBar
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.use_cases import payees as use_cases
from ynab_cli.host.textual.widgets.common.base_command import BaseCommand


class ListAllCommand(BaseCommand[use_cases.ListAllParams]):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Payee Id",
            "Payee Name",
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

        async for payee in use_cases.list_all(self.settings, TextualIO(self.app, log, progress_bar), use_case_params):
            table.add_row(
                payee.id,
                payee.name,
            )
