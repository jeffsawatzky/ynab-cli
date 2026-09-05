from enum import StrEnum

from typing_extensions import override


class SaveCategoryGoalFrequency(StrEnum):
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    YEARLY = "yearly"

    @override
    def __str__(self) -> str:
        return str(self.value)
