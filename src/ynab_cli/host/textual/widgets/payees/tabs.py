from textual.app import ComposeResult
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.domain.settings import Settings
from ynab_cli.host.textual.widgets.common.command_widget import CommandWidget

from .list_all import ListAllCommand
from .list_duplicates import ListDuplicatesCommand
from .list_unused import ListUnusedCommand
from .normalize_names import NormalizeNamesCommand


class PayeesTabs(Widget):
    settings: var[Settings] = var(Settings())

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

    def active_command(self) -> CommandWidget:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "normalize":
                return self.query_one(NormalizeNamesCommand)
            elif tabbed_content.active_pane.id == "duplicates":
                return self.query_one(ListDuplicatesCommand)
            elif tabbed_content.active_pane.id == "unused":
                return self.query_one(ListUnusedCommand)
            elif tabbed_content.active_pane.id == "all":
                return self.query_one(ListAllCommand)

        raise ValueError("No active command found in PayeesTabs.")
