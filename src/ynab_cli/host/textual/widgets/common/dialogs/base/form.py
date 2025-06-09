from typing import Generic, TypeVar

from textual.widget import Widget

FormResultType = TypeVar("FormResultType")


class DialogForm(Widget, Generic[FormResultType]):
    async def get_result(self) -> FormResultType:
        """Get the result of the form."""
        raise NotImplementedError("Subclasses must implement get_result method.")
