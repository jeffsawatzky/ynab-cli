from enum import Enum

from typing_extensions import override


class HybridTransactionType(str, Enum):
    SUBTRANSACTION = "subtransaction"
    TRANSACTION = "transaction"

    @override
    def __str__(self) -> str:
        return str(self.value)
