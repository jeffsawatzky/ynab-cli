from typing import Any, ClassVar

from textual.app import App as _App
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Checkbox, Footer, Header, Input, Label, TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.domain.settings import Settings
from ynab_cli.host.textual.widgets import RunnableWidget
from ynab_cli.host.textual.widgets.categories import CategoriesTabs
from ynab_cli.host.textual.widgets.payees import PayeesTabs
from ynab_cli.host.textual.widgets.transactions import TransactionsTabs


class CommandTabs(RunnableWidget):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Transactions", id="transactions"):
                yield TransactionsTabs().data_bind(settings=CommandTabs.settings)
            with TabPane("Categories", id="categories"):
                yield CategoriesTabs().data_bind(settings=CommandTabs.settings)
            with TabPane("Payees", id="payees"):
                yield PayeesTabs().data_bind(settings=CommandTabs.settings)

    @override
    async def run_command(self) -> None:
        tabbed_content = self.query_one(TabbedContent)
        if tabbed_content.active_pane:
            if tabbed_content.active_pane.id == "transactions":
                await self.query_one(TransactionsTabs).run_command()
            elif tabbed_content.active_pane.id == "categories":
                await self.query_one(CategoriesTabs).run_command()
            elif tabbed_content.active_pane.id == "payees":
                await self.query_one(PayeesTabs).run_command()


class App(_App[None]):
    TITLE = "YNAB CLI"
    CSS_PATH: ClassVar[str] = "app.tcss"

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("ctrl+c", "quit", "Quit", show=True, priority=True),
        Binding("r", "run", "Run", show=True, priority=False),
    ]

    settings: reactive[Settings] = reactive(Settings())

    def __init__(
        self,
        settings: Settings,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.settings = settings

    @override
    def compose(self) -> ComposeResult:
        yield Header(id="header")
        with Vertical(id="settings"):
            with Horizontal():
                with Vertical():
                    yield Label("Access Token")
                    yield Input(self.settings.ynab.access_token, placeholder="Access Token", id="access_token")
                with Vertical():
                    yield Label("Budget Id")
                    yield Input(self.settings.ynab.budget_id, placeholder="Budget Id", id="budget_id")
            with Horizontal():
                yield Checkbox("Debug", self.settings.debug, id="debug")
                yield Checkbox("Dry Run", self.settings.dry_run, id="dry_run")

        with Vertical(id="main"):
            yield CommandTabs().data_bind(settings=App.settings)
        yield Footer(id="footer")

    def on_mount(self) -> None:
        self.query_one(CommandTabs).query_one(TabbedContent).focus()

    async def action_run(self) -> None:
        command_tabs = self.query_one(CommandTabs)
        await command_tabs.run_command()

    async def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "access_token":
            self.settings.ynab.access_token = event.value
        elif event.input.id == "budget_id":
            self.settings.ynab.budget_id = event.value
        self.mutate_reactive(App.settings)

    async def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id == "debug":
            self.settings.debug = event.value
        elif event.checkbox.id == "dry_run":
            self.settings.dry_run = event.value
        self.mutate_reactive(App.settings)
