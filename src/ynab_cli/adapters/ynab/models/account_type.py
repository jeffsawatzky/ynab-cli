from enum import StrEnum

from typing_extensions import override


class AccountType(StrEnum):
    AUTOLOAN = "autoLoan"
    CASH = "cash"
    CHECKING = "checking"
    CREDITCARD = "creditCard"
    LINEOFCREDIT = "lineOfCredit"
    MEDICALDEBT = "medicalDebt"
    MORTGAGE = "mortgage"
    OTHERASSET = "otherAsset"
    OTHERDEBT = "otherDebt"
    OTHERLIABILITY = "otherLiability"
    PERSONALLOAN = "personalLoan"
    SAVINGS = "savings"
    STUDENTLOAN = "studentLoan"

    @override
    def __str__(self) -> str:
        return str(self.value)
