from enum import Enum

from typing_extensions import override


class CategoryGoalTypeType2Type1(str, Enum):
    DEBT = "DEBT"
    MF = "MF"
    NEED = "NEED"
    TB = "TB"
    TBD = "TBD"

    @override
    def __str__(self) -> str:
        return str(self.value)
