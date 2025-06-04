from enum import Enum

from typing_extensions import override


class ScheduledTransactionSummaryFrequency(str, Enum):
    DAILY = "daily"
    EVERY3MONTHS = "every3Months"
    EVERY4MONTHS = "every4Months"
    EVERY4WEEKS = "every4Weeks"
    EVERYOTHERMONTH = "everyOtherMonth"
    EVERYOTHERWEEK = "everyOtherWeek"
    EVERYOTHERYEAR = "everyOtherYear"
    MONTHLY = "monthly"
    NEVER = "never"
    TWICEAMONTH = "twiceAMonth"
    TWICEAYEAR = "twiceAYear"
    WEEKLY = "weekly"
    YEARLY = "yearly"

    @override
    def __str__(self) -> str:
        return str(self.value)
