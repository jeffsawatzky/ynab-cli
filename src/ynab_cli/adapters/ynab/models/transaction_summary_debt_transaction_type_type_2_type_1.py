from enum import StrEnum

from typing_extensions import override


class TransactionSummaryDebtTransactionTypeType2Type1(StrEnum):
    BALANCEADJUSTMENT = "balanceAdjustment"
    CHARGE = "charge"
    CREDIT = "credit"
    ESCROW = "escrow"
    FEE = "fee"
    INTEREST = "interest"
    PAYMENT = "payment"
    REFUND = "refund"

    @override
    def __str__(self) -> str:
        return str(self.value)
