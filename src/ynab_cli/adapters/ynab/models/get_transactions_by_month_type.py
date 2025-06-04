from enum import Enum

from typing_extensions import override


class GetTransactionsByMonthType(str, Enum):
    UNAPPROVED = "unapproved"
    UNCATEGORIZED = "uncategorized"

    @override
    def __str__(self) -> str:
        return str(self.value)
