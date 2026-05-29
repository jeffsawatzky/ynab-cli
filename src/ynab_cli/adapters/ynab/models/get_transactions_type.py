from enum import StrEnum

from typing_extensions import override


class GetTransactionsType(StrEnum):
    UNAPPROVED = "unapproved"
    UNCATEGORIZED = "uncategorized"

    @override
    def __str__(self) -> str:
        return str(self.value)
