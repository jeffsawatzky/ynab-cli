from enum import StrEnum

from typing_extensions import override


class HybridTransactionType(StrEnum):
    SUBTRANSACTION = "subtransaction"
    TRANSACTION = "transaction"

    @override
    def __str__(self) -> str:
        return str(self.value)
