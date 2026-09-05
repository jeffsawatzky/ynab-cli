from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.models.category_base_goal_type_type_1 import CategoryBaseGoalTypeType1
from ynab_cli.adapters.ynab.models.category_base_goal_type_type_2_type_1 import CategoryBaseGoalTypeType2Type1
from ynab_cli.adapters.ynab.models.category_base_goal_type_type_3_type_1 import CategoryBaseGoalTypeType3Type1
from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="Category")


@_attrs_define
class Category:
    """
    Attributes:
        id (UUID):
        category_group_id (UUID):
        name (str):
        hidden (bool): Whether or not the category is hidden
        internal (bool): Whether or not the category is internal
        budgeted (int): Assigned (budgeted) amount in milliunits format
        activity (int): Activity amount in milliunits format
        balance (int): Available balance in milliunits format
        deleted (bool): Whether or not the category has been deleted.  Deleted categories will only be included in delta
            requests.
        category_group_name (str | Unset):
        original_category_group_id (None | Unset | UUID): DEPRECATED: No longer used.  Value will always be null.
        note (None | str | Unset):
        goal_type (CategoryBaseGoalTypeType1 | CategoryBaseGoalTypeType2Type1 | CategoryBaseGoalTypeType3Type1 | None |
            Unset): The type of goal, if the category has a goal (TB='Target Category Balance', TBD='Target Category Balance
            by Date', MF='Monthly Funding', NEED='Plan Your Spending')
        goal_needs_whole_amount (bool | None | Unset): Indicates the monthly rollover behavior for "NEED"-type goals.
            When "true", the goal will always ask for the target amount in the new month ("Set Aside"). When "false",
            previous month category funding is used ("Refill"). For other goal types, this field will be null.
        goal_day (int | None | Unset): A day offset modifier for the goal's due date. When goal_cadence is 2 (Weekly),
            this value specifies which day of the week the goal is due (0 = Sunday, 6 = Saturday). Otherwise, this value
            specifies which day of the month the goal is due (1 = 1st, 31 = 31st, null = Last day of Month).
        goal_cadence (int | None | Unset): The goal cadence. Value in range 0-14. There are two subsets of these values
            which behave differently. For values 0, 1, 2, and 13, the goal's due date repeats every goal_cadence *
            goal_cadence_frequency, where 0 = None, 1 = Monthly, 2 = Weekly, and 13 = Yearly. For example, goal_cadence 1
            with goal_cadence_frequency 2 means the goal is due every other month. For values 3-12 and 14,
            goal_cadence_frequency is ignored and the goal's due date repeats every goal_cadence, where 3 = Every 2 Months,
            4 = Every 3 Months, ..., 12 = Every 11 Months, and 14 = Every 2 Years.
        goal_cadence_frequency (int | None | Unset): The goal cadence frequency. When goal_cadence is 0, 1, 2, or 13, a
            goal's due date repeats every goal_cadence * goal_cadence_frequency. For example, goal_cadence 1 with
            goal_cadence_frequency 2 means the goal is due every other month.  When goal_cadence is 3-12 or 14,
            goal_cadence_frequency is ignored.
        goal_creation_month (datetime.date | None | Unset): The month a goal was created
        goal_target (int | None | Unset): The goal target amount in milliunits
        goal_target_month (datetime.date | None | Unset): DEPRECATED: No longer used.  Use `goal_target_date` instead.
        goal_target_date (datetime.date | None | Unset): The target date for the goal to be completed.  Only some goal
            types specify this date.
        goal_percentage_complete (int | None | Unset): The percentage completion of the goal
        goal_months_to_budget (int | None | Unset): The number of months, including the current month, left in the
            current goal period.
        goal_under_funded (int | None | Unset): The amount of funding still needed in the current month to stay on track
            towards completing the goal within the current goal period. This amount will generally correspond to the
            'Underfunded' amount in the web and mobile clients except when viewing a category with a Needed for Spending
            Goal in a future month.  The web and mobile clients will ignore any funding from a prior goal period when
            viewing category with a Needed for Spending Goal in a future month.
        goal_overall_funded (int | None | Unset): The total amount funded towards the goal within the current goal
            period.
        goal_overall_left (int | None | Unset): The amount of funding still needed to complete the goal within the
            current goal period.
        goal_snoozed_at (datetime.datetime | None | Unset): The date/time the goal was snoozed.  If the goal is not
            snoozed, this will be null.
        balance_formatted (str | Unset): Available balance of the category formatted in the plan's currency format
        balance_currency (float | Unset): Available balance of the category as a decimal currency amount
        activity_formatted (str | Unset): Activity of the category formatted in the plan's currency format
        activity_currency (float | Unset): Activity of the category as a decimal currency amount
        budgeted_formatted (str | Unset): Assigned (budgeted) amount of the category formatted in the plan's currency
            format
        budgeted_currency (float | Unset): Assigned (budgeted) amount of the category as a decimal currency amount
        goal_target_formatted (None | str | Unset): The goal target amount formatted in the plan's currency format
        goal_target_currency (float | None | Unset): The goal target amount as a decimal currency amount
        goal_under_funded_formatted (None | str | Unset): The goal underfunded amount formatted in the plan's currency
            format
        goal_under_funded_currency (float | None | Unset): The goal underfunded amount as a decimal currency amount
        goal_overall_funded_formatted (None | str | Unset): The total amount funded towards the goal formatted in the
            plan's currency format
        goal_overall_funded_currency (float | None | Unset): The total amount funded towards the goal as a decimal
            currency amount
        goal_overall_left_formatted (None | str | Unset): The amount of funding still needed to complete the goal
            formatted in the plan's currency format
        goal_overall_left_currency (float | None | Unset): The amount of funding still needed to complete the goal as a
            decimal currency amount
    """

    id: UUID
    category_group_id: UUID
    name: str
    hidden: bool
    internal: bool
    budgeted: int
    activity: int
    balance: int
    deleted: bool
    category_group_name: str | Unset = UNSET
    original_category_group_id: Unset | UUID | None = UNSET
    note: str | Unset | None = UNSET
    goal_type: (
        CategoryBaseGoalTypeType1 | CategoryBaseGoalTypeType2Type1 | CategoryBaseGoalTypeType3Type1 | Unset | None
    ) = UNSET
    goal_needs_whole_amount: bool | Unset | None = UNSET
    goal_day: int | Unset | None = UNSET
    goal_cadence: int | Unset | None = UNSET
    goal_cadence_frequency: int | Unset | None = UNSET
    goal_creation_month: datetime.date | Unset | None = UNSET
    goal_target: int | Unset | None = UNSET
    goal_target_month: datetime.date | Unset | None = UNSET
    goal_target_date: datetime.date | Unset | None = UNSET
    goal_percentage_complete: int | Unset | None = UNSET
    goal_months_to_budget: int | Unset | None = UNSET
    goal_under_funded: int | Unset | None = UNSET
    goal_overall_funded: int | Unset | None = UNSET
    goal_overall_left: int | Unset | None = UNSET
    goal_snoozed_at: datetime.datetime | Unset | None = UNSET
    balance_formatted: str | Unset = UNSET
    balance_currency: float | Unset = UNSET
    activity_formatted: str | Unset = UNSET
    activity_currency: float | Unset = UNSET
    budgeted_formatted: str | Unset = UNSET
    budgeted_currency: float | Unset = UNSET
    goal_target_formatted: str | Unset | None = UNSET
    goal_target_currency: float | Unset | None = UNSET
    goal_under_funded_formatted: str | Unset | None = UNSET
    goal_under_funded_currency: float | Unset | None = UNSET
    goal_overall_funded_formatted: str | Unset | None = UNSET
    goal_overall_funded_currency: float | Unset | None = UNSET
    goal_overall_left_formatted: str | Unset | None = UNSET
    goal_overall_left_currency: float | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        category_group_id = str(self.category_group_id)

        name = self.name

        hidden = self.hidden

        internal = self.internal

        budgeted = self.budgeted

        activity = self.activity

        balance = self.balance

        deleted = self.deleted

        category_group_name = self.category_group_name

        original_category_group_id: str | Unset | None
        if isinstance(self.original_category_group_id, Unset):
            original_category_group_id = UNSET
        elif isinstance(self.original_category_group_id, UUID):
            original_category_group_id = str(self.original_category_group_id)
        else:
            original_category_group_id = self.original_category_group_id

        note: str | Unset | None
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        goal_type: str | Unset | None
        if isinstance(self.goal_type, Unset):
            goal_type = UNSET
        elif isinstance(
            self.goal_type, (CategoryBaseGoalTypeType1, CategoryBaseGoalTypeType2Type1, CategoryBaseGoalTypeType3Type1)
        ):
            goal_type = self.goal_type.value
        else:
            goal_type = self.goal_type

        goal_needs_whole_amount: bool | Unset | None
        if isinstance(self.goal_needs_whole_amount, Unset):
            goal_needs_whole_amount = UNSET
        else:
            goal_needs_whole_amount = self.goal_needs_whole_amount

        goal_day: int | Unset | None
        if isinstance(self.goal_day, Unset):
            goal_day = UNSET
        else:
            goal_day = self.goal_day

        goal_cadence: int | Unset | None
        if isinstance(self.goal_cadence, Unset):
            goal_cadence = UNSET
        else:
            goal_cadence = self.goal_cadence

        goal_cadence_frequency: int | Unset | None
        if isinstance(self.goal_cadence_frequency, Unset):
            goal_cadence_frequency = UNSET
        else:
            goal_cadence_frequency = self.goal_cadence_frequency

        goal_creation_month: str | Unset | None
        if isinstance(self.goal_creation_month, Unset):
            goal_creation_month = UNSET
        elif isinstance(self.goal_creation_month, datetime.date):
            goal_creation_month = self.goal_creation_month.isoformat()
        else:
            goal_creation_month = self.goal_creation_month

        goal_target: int | Unset | None
        if isinstance(self.goal_target, Unset):
            goal_target = UNSET
        else:
            goal_target = self.goal_target

        goal_target_month: str | Unset | None
        if isinstance(self.goal_target_month, Unset):
            goal_target_month = UNSET
        elif isinstance(self.goal_target_month, datetime.date):
            goal_target_month = self.goal_target_month.isoformat()
        else:
            goal_target_month = self.goal_target_month

        goal_target_date: str | Unset | None
        if isinstance(self.goal_target_date, Unset):
            goal_target_date = UNSET
        elif isinstance(self.goal_target_date, datetime.date):
            goal_target_date = self.goal_target_date.isoformat()
        else:
            goal_target_date = self.goal_target_date

        goal_percentage_complete: int | Unset | None
        if isinstance(self.goal_percentage_complete, Unset):
            goal_percentage_complete = UNSET
        else:
            goal_percentage_complete = self.goal_percentage_complete

        goal_months_to_budget: int | Unset | None
        if isinstance(self.goal_months_to_budget, Unset):
            goal_months_to_budget = UNSET
        else:
            goal_months_to_budget = self.goal_months_to_budget

        goal_under_funded: int | Unset | None
        if isinstance(self.goal_under_funded, Unset):
            goal_under_funded = UNSET
        else:
            goal_under_funded = self.goal_under_funded

        goal_overall_funded: int | Unset | None
        if isinstance(self.goal_overall_funded, Unset):
            goal_overall_funded = UNSET
        else:
            goal_overall_funded = self.goal_overall_funded

        goal_overall_left: int | Unset | None
        if isinstance(self.goal_overall_left, Unset):
            goal_overall_left = UNSET
        else:
            goal_overall_left = self.goal_overall_left

        goal_snoozed_at: str | Unset | None
        if isinstance(self.goal_snoozed_at, Unset):
            goal_snoozed_at = UNSET
        elif isinstance(self.goal_snoozed_at, datetime.datetime):
            goal_snoozed_at = self.goal_snoozed_at.isoformat()
        else:
            goal_snoozed_at = self.goal_snoozed_at

        balance_formatted = self.balance_formatted

        balance_currency = self.balance_currency

        activity_formatted = self.activity_formatted

        activity_currency = self.activity_currency

        budgeted_formatted = self.budgeted_formatted

        budgeted_currency = self.budgeted_currency

        goal_target_formatted: str | Unset | None
        if isinstance(self.goal_target_formatted, Unset):
            goal_target_formatted = UNSET
        else:
            goal_target_formatted = self.goal_target_formatted

        goal_target_currency: float | Unset | None
        if isinstance(self.goal_target_currency, Unset):
            goal_target_currency = UNSET
        else:
            goal_target_currency = self.goal_target_currency

        goal_under_funded_formatted: str | Unset | None
        if isinstance(self.goal_under_funded_formatted, Unset):
            goal_under_funded_formatted = UNSET
        else:
            goal_under_funded_formatted = self.goal_under_funded_formatted

        goal_under_funded_currency: float | Unset | None
        if isinstance(self.goal_under_funded_currency, Unset):
            goal_under_funded_currency = UNSET
        else:
            goal_under_funded_currency = self.goal_under_funded_currency

        goal_overall_funded_formatted: str | Unset | None
        if isinstance(self.goal_overall_funded_formatted, Unset):
            goal_overall_funded_formatted = UNSET
        else:
            goal_overall_funded_formatted = self.goal_overall_funded_formatted

        goal_overall_funded_currency: float | Unset | None
        if isinstance(self.goal_overall_funded_currency, Unset):
            goal_overall_funded_currency = UNSET
        else:
            goal_overall_funded_currency = self.goal_overall_funded_currency

        goal_overall_left_formatted: str | Unset | None
        if isinstance(self.goal_overall_left_formatted, Unset):
            goal_overall_left_formatted = UNSET
        else:
            goal_overall_left_formatted = self.goal_overall_left_formatted

        goal_overall_left_currency: float | Unset | None
        if isinstance(self.goal_overall_left_currency, Unset):
            goal_overall_left_currency = UNSET
        else:
            goal_overall_left_currency = self.goal_overall_left_currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "category_group_id": category_group_id,
                "name": name,
                "hidden": hidden,
                "internal": internal,
                "budgeted": budgeted,
                "activity": activity,
                "balance": balance,
                "deleted": deleted,
            }
        )
        if category_group_name is not UNSET:
            field_dict["category_group_name"] = category_group_name
        if original_category_group_id is not UNSET:
            field_dict["original_category_group_id"] = original_category_group_id
        if note is not UNSET:
            field_dict["note"] = note
        if goal_type is not UNSET:
            field_dict["goal_type"] = goal_type
        if goal_needs_whole_amount is not UNSET:
            field_dict["goal_needs_whole_amount"] = goal_needs_whole_amount
        if goal_day is not UNSET:
            field_dict["goal_day"] = goal_day
        if goal_cadence is not UNSET:
            field_dict["goal_cadence"] = goal_cadence
        if goal_cadence_frequency is not UNSET:
            field_dict["goal_cadence_frequency"] = goal_cadence_frequency
        if goal_creation_month is not UNSET:
            field_dict["goal_creation_month"] = goal_creation_month
        if goal_target is not UNSET:
            field_dict["goal_target"] = goal_target
        if goal_target_month is not UNSET:
            field_dict["goal_target_month"] = goal_target_month
        if goal_target_date is not UNSET:
            field_dict["goal_target_date"] = goal_target_date
        if goal_percentage_complete is not UNSET:
            field_dict["goal_percentage_complete"] = goal_percentage_complete
        if goal_months_to_budget is not UNSET:
            field_dict["goal_months_to_budget"] = goal_months_to_budget
        if goal_under_funded is not UNSET:
            field_dict["goal_under_funded"] = goal_under_funded
        if goal_overall_funded is not UNSET:
            field_dict["goal_overall_funded"] = goal_overall_funded
        if goal_overall_left is not UNSET:
            field_dict["goal_overall_left"] = goal_overall_left
        if goal_snoozed_at is not UNSET:
            field_dict["goal_snoozed_at"] = goal_snoozed_at
        if balance_formatted is not UNSET:
            field_dict["balance_formatted"] = balance_formatted
        if balance_currency is not UNSET:
            field_dict["balance_currency"] = balance_currency
        if activity_formatted is not UNSET:
            field_dict["activity_formatted"] = activity_formatted
        if activity_currency is not UNSET:
            field_dict["activity_currency"] = activity_currency
        if budgeted_formatted is not UNSET:
            field_dict["budgeted_formatted"] = budgeted_formatted
        if budgeted_currency is not UNSET:
            field_dict["budgeted_currency"] = budgeted_currency
        if goal_target_formatted is not UNSET:
            field_dict["goal_target_formatted"] = goal_target_formatted
        if goal_target_currency is not UNSET:
            field_dict["goal_target_currency"] = goal_target_currency
        if goal_under_funded_formatted is not UNSET:
            field_dict["goal_under_funded_formatted"] = goal_under_funded_formatted
        if goal_under_funded_currency is not UNSET:
            field_dict["goal_under_funded_currency"] = goal_under_funded_currency
        if goal_overall_funded_formatted is not UNSET:
            field_dict["goal_overall_funded_formatted"] = goal_overall_funded_formatted
        if goal_overall_funded_currency is not UNSET:
            field_dict["goal_overall_funded_currency"] = goal_overall_funded_currency
        if goal_overall_left_formatted is not UNSET:
            field_dict["goal_overall_left_formatted"] = goal_overall_left_formatted
        if goal_overall_left_currency is not UNSET:
            field_dict["goal_overall_left_currency"] = goal_overall_left_currency

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:  # noqa: C901
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        category_group_id = UUID(d.pop("category_group_id"))

        name = d.pop("name")

        hidden = d.pop("hidden")

        internal = d.pop("internal")

        budgeted = d.pop("budgeted")

        activity = d.pop("activity")

        balance = d.pop("balance")

        deleted = d.pop("deleted")

        category_group_name = d.pop("category_group_name", UNSET)

        def _parse_original_category_group_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                original_category_group_id_type_0 = UUID(data)

                return original_category_group_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        original_category_group_id = _parse_original_category_group_id(d.pop("original_category_group_id", UNSET))

        def _parse_note(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        note = _parse_note(d.pop("note", UNSET))

        def _parse_goal_type(
            data: object,
        ) -> CategoryBaseGoalTypeType1 | CategoryBaseGoalTypeType2Type1 | CategoryBaseGoalTypeType3Type1 | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_type_type_1 = CategoryBaseGoalTypeType1(data)

                return goal_type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_type_type_2_type_1 = CategoryBaseGoalTypeType2Type1(data)

                return goal_type_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_type_type_3_type_1 = CategoryBaseGoalTypeType3Type1(data)

                return goal_type_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CategoryBaseGoalTypeType1
                | CategoryBaseGoalTypeType2Type1
                | CategoryBaseGoalTypeType3Type1
                | Unset
                | None,
                data,
            )

        goal_type = _parse_goal_type(d.pop("goal_type", UNSET))

        def _parse_goal_needs_whole_amount(data: object) -> bool | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | Unset | None, data)

        goal_needs_whole_amount = _parse_goal_needs_whole_amount(d.pop("goal_needs_whole_amount", UNSET))

        def _parse_goal_day(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_day = _parse_goal_day(d.pop("goal_day", UNSET))

        def _parse_goal_cadence(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_cadence = _parse_goal_cadence(d.pop("goal_cadence", UNSET))

        def _parse_goal_cadence_frequency(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_cadence_frequency = _parse_goal_cadence_frequency(d.pop("goal_cadence_frequency", UNSET))

        def _parse_goal_creation_month(data: object) -> datetime.date | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_creation_month_type_0 = datetime.date.fromisoformat(data)

                return goal_creation_month_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | Unset | None, data)

        goal_creation_month = _parse_goal_creation_month(d.pop("goal_creation_month", UNSET))

        def _parse_goal_target(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_target = _parse_goal_target(d.pop("goal_target", UNSET))

        def _parse_goal_target_month(data: object) -> datetime.date | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_target_month_type_0 = datetime.date.fromisoformat(data)

                return goal_target_month_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | Unset | None, data)

        goal_target_month = _parse_goal_target_month(d.pop("goal_target_month", UNSET))

        def _parse_goal_target_date(data: object) -> datetime.date | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_target_date_type_0 = datetime.date.fromisoformat(data)

                return goal_target_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | Unset | None, data)

        goal_target_date = _parse_goal_target_date(d.pop("goal_target_date", UNSET))

        def _parse_goal_percentage_complete(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_percentage_complete = _parse_goal_percentage_complete(d.pop("goal_percentage_complete", UNSET))

        def _parse_goal_months_to_budget(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_months_to_budget = _parse_goal_months_to_budget(d.pop("goal_months_to_budget", UNSET))

        def _parse_goal_under_funded(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_under_funded = _parse_goal_under_funded(d.pop("goal_under_funded", UNSET))

        def _parse_goal_overall_funded(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_overall_funded = _parse_goal_overall_funded(d.pop("goal_overall_funded", UNSET))

        def _parse_goal_overall_left(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_overall_left = _parse_goal_overall_left(d.pop("goal_overall_left", UNSET))

        def _parse_goal_snoozed_at(data: object) -> datetime.datetime | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_snoozed_at_type_0 = datetime.datetime.fromisoformat(data)

                return goal_snoozed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | Unset | None, data)

        goal_snoozed_at = _parse_goal_snoozed_at(d.pop("goal_snoozed_at", UNSET))

        balance_formatted = d.pop("balance_formatted", UNSET)

        balance_currency = d.pop("balance_currency", UNSET)

        activity_formatted = d.pop("activity_formatted", UNSET)

        activity_currency = d.pop("activity_currency", UNSET)

        budgeted_formatted = d.pop("budgeted_formatted", UNSET)

        budgeted_currency = d.pop("budgeted_currency", UNSET)

        def _parse_goal_target_formatted(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        goal_target_formatted = _parse_goal_target_formatted(d.pop("goal_target_formatted", UNSET))

        def _parse_goal_target_currency(data: object) -> float | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | Unset | None, data)

        goal_target_currency = _parse_goal_target_currency(d.pop("goal_target_currency", UNSET))

        def _parse_goal_under_funded_formatted(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        goal_under_funded_formatted = _parse_goal_under_funded_formatted(d.pop("goal_under_funded_formatted", UNSET))

        def _parse_goal_under_funded_currency(data: object) -> float | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | Unset | None, data)

        goal_under_funded_currency = _parse_goal_under_funded_currency(d.pop("goal_under_funded_currency", UNSET))

        def _parse_goal_overall_funded_formatted(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        goal_overall_funded_formatted = _parse_goal_overall_funded_formatted(
            d.pop("goal_overall_funded_formatted", UNSET)
        )

        def _parse_goal_overall_funded_currency(data: object) -> float | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | Unset | None, data)

        goal_overall_funded_currency = _parse_goal_overall_funded_currency(d.pop("goal_overall_funded_currency", UNSET))

        def _parse_goal_overall_left_formatted(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        goal_overall_left_formatted = _parse_goal_overall_left_formatted(d.pop("goal_overall_left_formatted", UNSET))

        def _parse_goal_overall_left_currency(data: object) -> float | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | Unset | None, data)

        goal_overall_left_currency = _parse_goal_overall_left_currency(d.pop("goal_overall_left_currency", UNSET))

        category = cls(
            id=id,
            category_group_id=category_group_id,
            name=name,
            hidden=hidden,
            internal=internal,
            budgeted=budgeted,
            activity=activity,
            balance=balance,
            deleted=deleted,
            category_group_name=category_group_name,
            original_category_group_id=original_category_group_id,
            note=note,
            goal_type=goal_type,
            goal_needs_whole_amount=goal_needs_whole_amount,
            goal_day=goal_day,
            goal_cadence=goal_cadence,
            goal_cadence_frequency=goal_cadence_frequency,
            goal_creation_month=goal_creation_month,
            goal_target=goal_target,
            goal_target_month=goal_target_month,
            goal_target_date=goal_target_date,
            goal_percentage_complete=goal_percentage_complete,
            goal_months_to_budget=goal_months_to_budget,
            goal_under_funded=goal_under_funded,
            goal_overall_funded=goal_overall_funded,
            goal_overall_left=goal_overall_left,
            goal_snoozed_at=goal_snoozed_at,
            balance_formatted=balance_formatted,
            balance_currency=balance_currency,
            activity_formatted=activity_formatted,
            activity_currency=activity_currency,
            budgeted_formatted=budgeted_formatted,
            budgeted_currency=budgeted_currency,
            goal_target_formatted=goal_target_formatted,
            goal_target_currency=goal_target_currency,
            goal_under_funded_formatted=goal_under_funded_formatted,
            goal_under_funded_currency=goal_under_funded_currency,
            goal_overall_funded_formatted=goal_overall_funded_formatted,
            goal_overall_funded_currency=goal_overall_funded_currency,
            goal_overall_left_formatted=goal_overall_left_formatted,
            goal_overall_left_currency=goal_overall_left_currency,
        )

        category.additional_properties = d
        return category

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
