from typing import Generic, TypeVar

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button
from typing_extensions import override

from .form import DialogForm

DialogResultType = TypeVar("DialogResultType")


class Dialog(Widget, Generic[DialogResultType]):
    def __init__(self, form: DialogForm[DialogResultType]) -> None:
        super().__init__()

        self._form = form

    @override
    def compose(self) -> ComposeResult:
        yield self._form


class SaveCancelDialog(Dialog[DialogResultType]):
    class Saved(Message):
        def __init__(self, result: DialogResultType) -> None:
            super().__init__()
            self.result = result

    class Cancelled(Message):
        pass

    def __init__(self, form: DialogForm[DialogResultType], title: str | None = None) -> None:
        super().__init__(form)

        self._form = form
        self.border_title = title or "Save/Cancel"

    @override
    def compose(self) -> ComposeResult:
        yield from super().compose()

        with Horizontal():
            yield Button("Cancel", id="cancel", variant="error")
            yield Button("Save", id="save", variant="primary")

    @on(Button.Pressed, "#cancel")
    async def _cancel_button_pressed(self, _: Button.Pressed) -> None:
        await self._cancel()

    async def _cancel(self) -> None:
        self.post_message(self.Cancelled())

    @on(Button.Pressed, "#save")
    async def _save_button_pressed(self, _: Button.Pressed) -> None:
        await self._save()

    async def _save(self) -> None:
        result = await self._form.get_result()
        self.post_message(self.Saved(result))
