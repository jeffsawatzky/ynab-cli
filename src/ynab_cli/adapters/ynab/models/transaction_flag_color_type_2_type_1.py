from enum import Enum

from typing_extensions import override


class TransactionFlagColorType2Type1(str, Enum):
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
