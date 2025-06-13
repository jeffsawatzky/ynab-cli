from textual.app import ComposeResult
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.domain.settings import Settings
from ynab_cli.host.textual.widgets.categories.tabs import CategoriesTabs
from ynab_cli.host.textual.widgets.common.command_widget import CommandWidget
from ynab_cli.host.textual.widgets.payees.tabs import PayeesTabs
from ynab_cli.host.textual.widgets.transactions.tabs import TransactionsTabs


class CommandTabs(Widget):
    settings: var[Settings] = var(Settings())

    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Transactions", id="transactions"):
                yield TransactionsTabs().data_bind(settings=CommandTabs.settings)
            with TabPane("Categories", id="categories"):
                yield CategoriesTabs().data_bind(settings=CommandTabs.settings)
            with TabPane("Payees", id="payees"):
                yield PayeesTabs().data_bind(settings=CommandTabs.settings)

    def active_command(self) -> CommandWidget:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "transactions":
                return self.query_one(TransactionsTabs).active_command()
            elif tabbed_content.active_pane.id == "categories":
                return self.query_one(CategoriesTabs).active_command()
            elif tabbed_content.active_pane.id == "payees":
                return self.query_one(PayeesTabs).active_command()

        raise ValueError("No active command found in CommandTabs.")
