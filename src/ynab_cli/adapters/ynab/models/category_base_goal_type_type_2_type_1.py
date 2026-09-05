from enum import StrEnum

from typing_extensions import override


class CategoryBaseGoalTypeType2Type1(StrEnum):
    DEBT = "DEBT"
    MF = "MF"
    NEED = "NEED"
    TB = "TB"
    TBD = "TBD"

    @override
    def __str__(self) -> str:
        return str(self.value)
