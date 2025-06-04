from enum import Enum

from typing_extensions import override


class TransactionFlagColorType3Type1(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    ORANGE = "orange"
    PURPLE = "purple"
    RED = "red"
    YELLOW = "yellow"

    @override
    def __str__(self) -> str:
        return str(self.value)
