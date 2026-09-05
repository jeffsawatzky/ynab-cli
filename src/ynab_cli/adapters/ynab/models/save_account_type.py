from enum import StrEnum

from typing_extensions import override


class SaveAccountType(StrEnum):
    CASH = "cash"
    CHECKING = "checking"
    CREDITCARD = "creditCard"
    OTHERASSET = "otherAsset"
    OTHERLIABILITY = "otherLiability"
    SAVINGS = "savings"

    @override
    def __str__(self) -> str:
        return str(self.value)
