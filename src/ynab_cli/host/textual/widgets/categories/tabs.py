from textual.app import ComposeResult
from textual.widgets import TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.host.textual.widgets.common.runnable_widget import RunnableWidget

from .list_all import ListAllCommand
from .list_unused import ListUnusedCommand


class CategoriesTabs(RunnableWidget):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Unused", id="unused"):
                yield ListUnusedCommand().data_bind(settings=CategoriesTabs.settings)
            with TabPane("All", id="all"):
                yield ListAllCommand().data_bind(settings=CategoriesTabs.settings)

    @override
    async def run_command(self) -> None:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "unused":
                await self.query_one(ListUnusedCommand).run_command()
            elif tabbed_content.active_pane.id == "all":
                await self.query_one(ListAllCommand).run_command()
