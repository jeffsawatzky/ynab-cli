from typing import Any, ClassVar

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Button, Checkbox, Footer, Header, Input, Label, TabbedContent, TabPane
from typing_extensions import override

from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.textual.widgets.categories import CategoriesTabs
from ynab_cli.host.textual.widgets.common.dialogs import CANCELLED, DialogForm, SaveCancelDialogScreen
from ynab_cli.host.textual.widgets.common.runnable_widget import RunnableWidget
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


class SettingsDialogForm(DialogForm[Settings]):
    def __init__(self, settings: Settings, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._settings = settings

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical():
                yield Label("Access Token")
                yield Input(self._settings.ynab.access_token, placeholder="Access Token", id="access_token")
            with Vertical():
                yield Label("Budget Id")
                yield Input(self._settings.ynab.budget_id, placeholder="Budget Id", id="budget_id")
        with Horizontal():
            yield Checkbox("Debug", self._settings.debug, id="debug")
            yield Checkbox("Dry Run", self._settings.dry_run, id="dry_run")

    @override
    async def get_result(self) -> Settings:
        """Get the result from the dialog form."""
        access_token = self.query_one("#access_token", Input).value.strip()
        budget_id = self.query_one("#budget_id", Input).value.strip()
        debug = self.query_one("#debug", Checkbox).value
        dry_run = self.query_one("#dry_run", Checkbox).value

        return Settings(
            ynab=YnabSettings(
                access_token=access_token,
                budget_id=budget_id,
            ),
            debug=debug,
            dry_run=dry_run,
        )


class YnabCliApp(App[None]):
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

        with Vertical(id="toolbar"):
            yield Button("Settings", id="settings_button")

        with Vertical(id="main"):
            yield CommandTabs().data_bind(settings=YnabCliApp.settings)

        yield Footer(id="footer")

    def on_mount(self) -> None:
        self.query_one(CommandTabs).query_one(TabbedContent).focus()

    async def action_run(self) -> None:
        command_tabs = self.query_one(CommandTabs)
        await command_tabs.run_command()

    @on(Button.Pressed, "#settings_button")
    async def _settings_button_pressed(self, event: Button.Pressed) -> None:
        self._get_settings()

    @work(exclusive=True)
    async def _get_settings(self) -> None:
        result = await self.push_screen_wait(
            SaveCancelDialogScreen(SettingsDialogForm(self.settings), title="Settings")
        )
        if result is not CANCELLED:
            self.settings = result
