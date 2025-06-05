from typing import Any

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Log, ProgressBar
from typing_extensions import override

from ynab_cli.domain.ports.io import IO, Progress


class TextualProgress(Progress):
    def __init__(self, progress_bar: ProgressBar) -> None:
        self._progress_bar = progress_bar

    @override
    async def update(
        self, *, total: float | None = None, completed: float | None = None, advance: float | None = None
    ) -> None:
        kwargs = {}
        if total is not None:
            kwargs["total"] = total
        if completed is not None:
            kwargs["progress"] = completed
        if advance is not None:
            kwargs["advance"] = advance
        self._progress_bar.update(**kwargs)


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


class TextualWorkerIO(IO):
    def __init__(self, app: App[Any], log: Log, progress_bar: ProgressBar) -> None:
        self._app = app
        self._log = log
        self.progress = TextualProgress(progress_bar)

    @override
    async def prompt(self, prompt: str, password: bool = False) -> str:
        return await self._app.push_screen_wait(IOScreen(prompt, password))

    @override
    async def print(self, message: str) -> None:
        self._log.write_line(message)
