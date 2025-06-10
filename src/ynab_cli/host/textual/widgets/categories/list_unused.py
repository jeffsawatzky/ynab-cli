from textual.widgets import DataTable, Log, ProgressBar
from typing_extensions import override

from ynab_cli.adapters.textual.io import TextualIO
from ynab_cli.domain.use_cases import categories as use_cases
from ynab_cli.host.textual.widgets.common.base_command import BaseCommand


class ListUnusedCommand(BaseCommand[use_cases.ListUnusedParams]):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Category Group Id",
            "Category Group Name",
            "Category Id",
            "Category Name",
        )

    @override
    async def run_command(self) -> None:
        params: use_cases.ListUnusedParams = {}
        self._run_command_worker(params)

    @override
    async def _run_command(self, use_case_params: use_cases.ListUnusedParams) -> None:
        progress_bar = self.query_one(ProgressBar)
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        async for category in use_cases.list_unused(
            self.settings, TextualIO(self.app, log, progress_bar), use_case_params
        ):
            table.add_row(
                category.category_group_id,
                category.category_group_name,
                category.id,
                category.name,
            )
