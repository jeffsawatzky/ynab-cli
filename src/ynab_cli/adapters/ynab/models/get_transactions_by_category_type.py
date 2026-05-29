from enum import StrEnum

from typing_extensions import override


class GetTransactionsByCategoryType(StrEnum):
    UNAPPROVED = "unapproved"
    UNCATEGORIZED = "uncategorized"

    @override
    def __str__(self) -> str:
        return str(self.value)
