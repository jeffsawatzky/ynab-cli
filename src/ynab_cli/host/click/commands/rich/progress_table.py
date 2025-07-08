from typing import Any

from rich import console as rich_console
from rich import progress as rich_progress
from rich import table as rich_table
from typing_extensions import override


class ProgressTable(rich_progress.Progress):
    @override
    def __init__(
        self,
        table: rich_table.Table,
        *columns: str | rich_progress.ProgressColumn,
        auto_refresh: bool = True,
        transient: bool = True,
        **kwargs: Any,
    ) -> None:
        self._render_table = False
        self.table = table
        super().__init__(*columns, auto_refresh=auto_refresh, transient=transient, **kwargs)

    @override
    def get_renderable(self) -> rich_console.RenderableType:
        if self._render_table and self.live.is_started:
            return rich_console.Group(*self.get_renderables(), self.table)
        return super().get_renderable()

    @override
    def start(self) -> None:
        self._render_table = True
        return super().start()

    @override
    def stop(self) -> None:
        self._render_table = False
        return super().stop()
