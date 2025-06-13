from enum import Enum
from typing import ClassVar, Literal, TypeAlias

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.screen import ModalScreen, ScreenResultType
from textual.widgets import Footer
from typing_extensions import override

from .dialog import SaveCancelDialog
from .form import DialogForm


class DialogScreen(ModalScreen[ScreenResultType]):
    pass


class CancelledType(Enum):
    YES = 0


CANCELLED = CancelledType.YES
Cancelled: TypeAlias = Literal[CancelledType.YES]


class SaveCancelDialogScreen(DialogScreen[Cancelled | ScreenResultType]):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "cancel", "Cancel", show=True, priority=True),
        Binding("ctrl+s", "save", "Save", show=True, priority=True),
    ]

    def __init__(self, form: DialogForm[ScreenResultType], title: str | None = None) -> None:
        super().__init__()
        self._dialog = SaveCancelDialog(form, title=title)

    @override
    def compose(self) -> ComposeResult:
        yield self._dialog
        yield Footer()

    @on(SaveCancelDialog.Cancelled)
    async def _save_cancel_dialod_cancelled(self, _: SaveCancelDialog.Cancelled) -> None:
        self.dismiss(CANCELLED)

    async def action_cancel(self) -> None:
        self.dismiss(CANCELLED)

    @on(SaveCancelDialog.Saved)
    async def _save_cancel_dialod_saved(self, event: SaveCancelDialog.Saved) -> None:
        self.dismiss(event.result)  # type: ignore[arg-type]

    async def action_save(self) -> None:
        result = await self._dialog._form.get_result()
        self.dismiss(result)
