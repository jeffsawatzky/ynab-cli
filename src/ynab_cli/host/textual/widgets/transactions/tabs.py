from textual.app import ComposeResult
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.domain.settings import Settings
from ynab_cli.host.textual.widgets.common.command_widget import CommandWidget

from .apply_rules import ApplyRulesCommand


class TransactionsTabs(Widget):
    settings: var[Settings] = var(Settings())

    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Transactions", id="transactions"):
                yield ApplyRulesCommand().data_bind(settings=TransactionsTabs.settings)

    def active_command(self) -> CommandWidget:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "transactions":
                return self.query_one(ApplyRulesCommand)

        raise ValueError("No active command found in TransactionsTabs.")
