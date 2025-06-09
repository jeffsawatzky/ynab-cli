from enum import Enum
from typing import Literal, TypeAlias

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen, ScreenResultType
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
    def __init__(self, form: DialogForm[ScreenResultType], title: str | None = None) -> None:
        super().__init__()
        self._dialog = SaveCancelDialog(form, title=title)

    @override
    def compose(self) -> ComposeResult:
        yield self._dialog

    @on(SaveCancelDialog.Saved)
    async def _save_cancel_dialod_saved(self, event: SaveCancelDialog.Saved) -> None:
        self.dismiss(event.result)  # type: ignore[arg-type]

    @on(SaveCancelDialog.Cancelled)
    async def _save_cancel_dialod_cancelled(self, _: SaveCancelDialog.Cancelled) -> None:
        self.dismiss(CANCELLED)
