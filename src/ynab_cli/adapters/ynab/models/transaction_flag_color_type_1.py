from enum import StrEnum

from typing_extensions import override


class TransactionFlagColorType1(StrEnum):
    BLUE = "blue"
    GREEN = "green"
    ORANGE = "orange"
    PURPLE = "purple"
    RED = "red"
    VALUE_6 = ""
    YELLOW = "yellow"

    @override
    def __str__(self) -> str:
        return str(self.value)
