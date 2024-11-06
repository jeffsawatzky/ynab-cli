from typing import Any

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Log
from typing_extensions import override

from ynab_cli.domain.ports.io import StdinIO


class IOScreen(ModalScreen[str]):
    """A simple modal screen which asks for user input."""

    def __init__(self, prompt: str, password: bool, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._prompt = prompt
        self._password = password

    @override
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self._prompt)
            yield Input(password=self._password)

    @on(Input.Submitted)
    def return_response(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)


class TextualWorkerIO(StdinIO):
    def __init__(self, app: App[Any], log: Log, call_from_thread: bool = False) -> None:
        self._app = app
        self._log = log
        self._call_from_thread = call_from_thread

    @override
    async def prompt(self, prompt: str, password: bool = False) -> str:
        return await self._app.push_screen_wait(IOScreen(prompt, password))

    @override
    async def print(self, message: str) -> None:
        if self._call_from_thread:
            self._app.call_from_thread(self._log.write_line, message)
        else:
            self._log.write_line(message)
