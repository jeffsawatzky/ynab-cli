from textual.app import ComposeResult
from textual.widgets import TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.host.textual.widgets.common.runnable_widget import RunnableWidget

from .list_all import ListAllCommand
from .list_duplicates import ListDuplicatesCommand
from .list_unused import ListUnusedCommand
from .normalize_names import NormalizeNamesCommand


class PayeesTabs(RunnableWidget):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Normalize", id="normalize"):
                yield NormalizeNamesCommand().data_bind(settings=PayeesTabs.settings)
            with TabPane("Duplicates", id="duplicates"):
                yield ListDuplicatesCommand().data_bind(settings=PayeesTabs.settings)
            with TabPane("Unused", id="unused"):
                yield ListUnusedCommand().data_bind(settings=PayeesTabs.settings)
            with TabPane("All", id="all"):
                yield ListAllCommand().data_bind(settings=PayeesTabs.settings)

    @override
    async def run_command(self) -> None:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "normalize":
                await self.query_one(NormalizeNamesCommand).run_command()
            elif tabbed_content.active_pane.id == "duplicates":
                await self.query_one(ListDuplicatesCommand).run_command()
            elif tabbed_content.active_pane.id == "unused":
                await self.query_one(ListUnusedCommand).run_command()
            elif tabbed_content.active_pane.id == "all":
                await self.query_one(ListAllCommand).run_command()
