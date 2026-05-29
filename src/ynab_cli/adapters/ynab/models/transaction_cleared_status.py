from enum import StrEnum

from typing_extensions import override


class TransactionClearedStatus(StrEnum):
    CLEARED = "cleared"
    RECONCILED = "reconciled"
    UNCLEARED = "uncleared"

    @override
    def __str__(self) -> str:
        return str(self.value)
