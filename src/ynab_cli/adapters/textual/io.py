from typing import Any

from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Log, ProgressBar
from typing_extensions import override

from ynab_cli.domain.ports.io import IO, Progress
from ynab_cli.host.textual.widgets.common.dialogs import CANCELLED, DialogForm, SaveCancelDialogScreen


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


class IODialogForm(DialogForm[str]):
    def __init__(self, prompt: str, password: bool, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._prompt = prompt
        self._password = password

    @override
    def compose(self) -> ComposeResult:
        yield Label(self._prompt)
        yield Input(password=self._password)

    @override
    async def get_result(self) -> str:
        return self.query_one(Input).value.strip()


class TextualIO(IO):
    def __init__(self, app: App[Any], log: Log, progress_bar: ProgressBar) -> None:
        self._app = app
        self._log = log
        self.progress = TextualProgress(progress_bar)

    @override
    async def prompt(self, prompt: str, password: bool = False) -> str:
        result = await self._app.push_screen_wait(SaveCancelDialogScreen(IODialogForm(prompt, password), title="Input"))
        if result is CANCELLED:
            return ""
        return result

    @override
    async def print(self, message: str) -> None:
        self._log.write_line(message)
