from textual.app import ComposeResult
from textual.widgets import TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.host.textual.widgets.common.runnable_widget import RunnableWidget

from .apply_rules import ApplyRulesCommand


class TransactionsTabs(RunnableWidget):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Transactions", id="transactions"):
                yield ApplyRulesCommand().data_bind(settings=TransactionsTabs.settings)

    @override
    async def run_command(self) -> None:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "transactions":
                await self.query_one(ApplyRulesCommand).run_command()
