from enum import Enum

from typing_extensions import override


class TransactionClearedStatus(str, Enum):
    CLEARED = "cleared"
    RECONCILED = "reconciled"
    UNCLEARED = "uncleared"

    @override
    def __str__(self) -> str:
        return str(self.value)
