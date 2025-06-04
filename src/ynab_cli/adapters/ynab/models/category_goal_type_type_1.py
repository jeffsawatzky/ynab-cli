from enum import Enum

from typing_extensions import override


class CategoryGoalTypeType1(str, Enum):
    DEBT = "DEBT"
    MF = "MF"
    NEED = "NEED"
    TB = "TB"
    TBD = "TBD"

    @override
    def __str__(self) -> str:
        return str(self.value)
