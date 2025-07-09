from typing import Any, ClassVar

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Checkbox, Footer, Header, Input, Label, TabbedContent
from typing_extensions import override

from ynab_cli.adapters.ynab.client import AuthenticatedClient
from ynab_cli.domain.settings import Settings, YnabSettings
from ynab_cli.host.textual.widgets.common.command_widget import CommandWidget
from ynab_cli.host.textual.widgets.common.dialogs import CANCELLED, DialogForm, SaveCancelDialogScreen
from ynab_cli.host.textual.widgets.tabs import CommandTabs


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
        Binding("s", "settings", "Application Settings", show=True, priority=False),
        Binding("p", "parameters", "Command Parameters", show=True, priority=False),
        Binding("r", "run", "Run Command", show=True, priority=False),
    ]

    settings: reactive[Settings] = reactive(Settings())

    def __init__(
        self,
        settings: Settings,
        client: AuthenticatedClient,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.settings = settings
        self.client = client

    @override
    def compose(self) -> ComposeResult:
        yield Header(id="header")
        yield CommandTabs().data_bind(settings=YnabCliApp.settings)
        yield Footer(id="footer")

    def on_mount(self) -> None:
        self.query_one(CommandTabs).query_one(TabbedContent).focus()

    async def action_settings(self) -> None:
        self._get_settings_worker()

    @work(exclusive=True)
    async def _get_settings_worker(self) -> None:
        result = await self.push_screen_wait(
            SaveCancelDialogScreen(SettingsDialogForm(self.settings), title="Settings")
        )
        if result is not CANCELLED:
            self.settings = result
            self.client.update_token(self.settings.ynab.access_token)

    async def action_parameters(self) -> None:
        command_tabs = self.query_one(CommandTabs)
        await command_tabs.active_command().get_command_params()

    async def action_run(self) -> None:
        command_tabs = self.query_one(CommandTabs)
        await command_tabs.active_command().run_command()

    @on(CommandWidget.CommandCompleted)
    def _worker_state_changed(self, event: CommandWidget.CommandCompleted) -> None:
        # If the user had to update the access token, we need to update the settings.
        if self.settings.ynab.access_token != self.client.token:
            self.settings.ynab.access_token = self.client.token
            self.mutate_reactive(YnabCliApp.settings)
