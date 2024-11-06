from typing import Any, ClassVar

from textual.app import App as _App
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.reactive import var
from textual.widgets import Footer, Header, TabbedContent, TabPane
from textual.worker import WorkerState
from typing_extensions import override

from ynab_cli.domain.settings import Settings
from ynab_cli.host.textual.types import CommandParams
from ynab_cli.host.textual.widgets import BaseCommand, CommandRunnableWidget
from ynab_cli.host.textual.widgets.amazon import AMAZON_TAB_ID, AmazonTabs
from ynab_cli.host.textual.widgets.categories import CATEGORIES_TAB_ID, CategoriesTabs
from ynab_cli.host.textual.widgets.payees import PAYEES_TAB_ID, PayeesTabs
from ynab_cli.host.textual.widgets.transactions import TRANSACTIONS_TAB_ID, TransactionsTabs


class CommandTabs(CommandRunnableWidget):
    settings: var[Settings] = var(Settings())

    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Transactions", id=TRANSACTIONS_TAB_ID):
                yield TransactionsTabs().data_bind(settings=CommandTabs.settings)
            with TabPane("Categories", id=CATEGORIES_TAB_ID):
                yield CategoriesTabs().data_bind(settings=CommandTabs.settings)
            with TabPane("Payees", id=PAYEES_TAB_ID):
                yield PayeesTabs().data_bind(settings=CommandTabs.settings)
            with TabPane("Amazon", id=AMAZON_TAB_ID):
                yield AmazonTabs().data_bind(settings=CommandTabs.settings)

    @override
    def run_command(self, params: CommandParams) -> None:
        active_tab_id, _ = params
        if active_tab_id[0] == TRANSACTIONS_TAB_ID:
            self.query_one(TabbedContent).active = TRANSACTIONS_TAB_ID
            self.query_one(TransactionsTabs).run_command(params)
        elif active_tab_id[0] == CATEGORIES_TAB_ID:
            self.query_one(TabbedContent).active = CATEGORIES_TAB_ID
            self.query_one(CategoriesTabs).run_command(params)
        elif active_tab_id[0] == PAYEES_TAB_ID:
            self.query_one(TabbedContent).active = PAYEES_TAB_ID
            self.query_one(PayeesTabs).run_command(params)
        elif active_tab_id[0] == AMAZON_TAB_ID:
            self.query_one(TabbedContent).active = AMAZON_TAB_ID
            self.query_one(AmazonTabs).run_command(params)


class App(_App[None]):
    CSS_PATH = "app.tcss"

    BINDINGS: ClassVar[list[BindingType]] = [Binding("ctrl+c", "quit", "Quit", show=True, priority=True)]

    settings: var[Settings] = var(Settings())

    def __init__(
        self,
        settings: Settings,
        quiet: bool = False,
        params: CommandParams | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.settings = settings

        self._quiet = quiet
        self._params = params

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        yield CommandTabs().data_bind(settings=App.settings)
        yield Footer()

    def on_mount(self) -> None:
        if self._params is not None:
            self.query_one(CommandTabs).run_command(self._params)

    def on_base_command_command_completed(self, message: BaseCommand.CommandCompleted) -> None:
        if self._quiet:
            exit_code = 0 if message.worker_state == WorkerState.SUCCESS else 1
            self.exit(return_code=exit_code)
