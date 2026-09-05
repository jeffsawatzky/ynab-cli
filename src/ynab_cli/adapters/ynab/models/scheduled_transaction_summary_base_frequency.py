from enum import StrEnum

from typing_extensions import override


class ScheduledTransactionSummaryBaseFrequency(StrEnum):
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
