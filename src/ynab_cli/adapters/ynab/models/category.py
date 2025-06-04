import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ynab_cli.adapters.ynab.models.category_goal_type_type_1 import CategoryGoalTypeType1
from ynab_cli.adapters.ynab.models.category_goal_type_type_2_type_1 import CategoryGoalTypeType2Type1
from ynab_cli.adapters.ynab.models.category_goal_type_type_3_type_1 import CategoryGoalTypeType3Type1
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
        budgeted (int): Budgeted amount in milliunits format
        activity (int): Activity amount in milliunits format
        balance (int): Balance in milliunits format
        deleted (bool): Whether or not the category has been deleted.  Deleted categories will only be included in delta
            requests.
        category_group_name (Union[Unset, str]):
        original_category_group_id (Union[None, UUID, Unset]): DEPRECATED: No longer used.  Value will always be null.
        note (Union[None, Unset, str]):
        goal_type (Union[CategoryGoalTypeType1, CategoryGoalTypeType2Type1, CategoryGoalTypeType3Type1, None, Unset]):
            The type of goal, if the category has a goal (TB='Target Category Balance', TBD='Target Category Balance by
            Date', MF='Monthly Funding', NEED='Plan Your Spending')
        goal_needs_whole_amount (Union[None, Unset, bool]): Indicates the monthly rollover behavior for "NEED"-type
            goals. When "true", the goal will always ask for the target amount in the new month ("Set Aside"). When "false",
            previous month category funding is used ("Refill"). For other goal types, this field will be null.
        goal_day (Union[None, Unset, int]): A day offset modifier for the goal's due date. When goal_cadence is 2
            (Weekly), this value specifies which day of the week the goal is due (0 = Sunday, 6 = Saturday). Otherwise, this
            value specifies which day of the month the goal is due (1 = 1st, 31 = 31st, null = Last day of Month).
        goal_cadence (Union[None, Unset, int]): The goal cadence. Value in range 0-14. There are two subsets of these
            values which behave differently. For values 0, 1, 2, and 13, the goal's due date repeats every goal_cadence *
            goal_cadence_frequency, where 0 = None, 1 = Monthly, 2 = Weekly, and 13 = Yearly. For example, goal_cadence 1
            with goal_cadence_frequency 2 means the goal is due every other month. For values 3-12 and 14,
            goal_cadence_frequency is ignored and the goal's due date repeats every goal_cadence, where 3 = Every 2 Months,
            4 = Every 3 Months, ..., 12 = Every 11 Months, and 14 = Every 2 Years.
        goal_cadence_frequency (Union[None, Unset, int]): The goal cadence frequency. When goal_cadence is 0, 1, 2, or
            13, a goal's due date repeats every goal_cadence * goal_cadence_frequency. For example, goal_cadence 1 with
            goal_cadence_frequency 2 means the goal is due every other month.  When goal_cadence is 3-12 or 14,
            goal_cadence_frequency is ignored.
        goal_creation_month (Union[None, Unset, datetime.date]): The month a goal was created
        goal_target (Union[None, Unset, int]): The goal target amount in milliunits
        goal_target_month (Union[None, Unset, datetime.date]): The original target month for the goal to be completed.
            Only some goal types specify this date.
        goal_percentage_complete (Union[None, Unset, int]): The percentage completion of the goal
        goal_months_to_budget (Union[None, Unset, int]): The number of months, including the current month, left in the
            current goal period.
        goal_under_funded (Union[None, Unset, int]): The amount of funding still needed in the current month to stay on
            track towards completing the goal within the current goal period. This amount will generally correspond to the
            'Underfunded' amount in the web and mobile clients except when viewing a category with a Needed for Spending
            Goal in a future month.  The web and mobile clients will ignore any funding from a prior goal period when
            viewing category with a Needed for Spending Goal in a future month.
        goal_overall_funded (Union[None, Unset, int]): The total amount funded towards the goal within the current goal
            period.
        goal_overall_left (Union[None, Unset, int]): The amount of funding still needed to complete the goal within the
            current goal period.
    """

    id: UUID
    category_group_id: UUID
    name: str
    hidden: bool
    budgeted: int
    activity: int
    balance: int
    deleted: bool
    category_group_name: Unset | str = UNSET
    original_category_group_id: None | UUID | Unset = UNSET
    note: None | Unset | str = UNSET
    goal_type: CategoryGoalTypeType1 | CategoryGoalTypeType2Type1 | CategoryGoalTypeType3Type1 | None | Unset = UNSET
    goal_needs_whole_amount: None | Unset | bool = UNSET
    goal_day: None | Unset | int = UNSET
    goal_cadence: None | Unset | int = UNSET
    goal_cadence_frequency: None | Unset | int = UNSET
    goal_creation_month: None | Unset | datetime.date = UNSET
    goal_target: None | Unset | int = UNSET
    goal_target_month: None | Unset | datetime.date = UNSET
    goal_percentage_complete: None | Unset | int = UNSET
    goal_months_to_budget: None | Unset | int = UNSET
    goal_under_funded: None | Unset | int = UNSET
    goal_overall_funded: None | Unset | int = UNSET
    goal_overall_left: None | Unset | int = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        category_group_id = str(self.category_group_id)

        name = self.name

        hidden = self.hidden

        budgeted = self.budgeted

        activity = self.activity

        balance = self.balance

        deleted = self.deleted

        category_group_name = self.category_group_name

        original_category_group_id: None | Unset | str
        if isinstance(self.original_category_group_id, Unset):
            original_category_group_id = UNSET
        elif isinstance(self.original_category_group_id, UUID):
            original_category_group_id = str(self.original_category_group_id)
        else:
            original_category_group_id = self.original_category_group_id

        note: None | Unset | str
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        goal_type: None | Unset | str
        if isinstance(self.goal_type, Unset):
            goal_type = UNSET
        elif isinstance(self.goal_type, CategoryGoalTypeType1):
            goal_type = self.goal_type.value
        elif isinstance(self.goal_type, CategoryGoalTypeType2Type1):
            goal_type = self.goal_type.value
        elif isinstance(self.goal_type, CategoryGoalTypeType3Type1):
            goal_type = self.goal_type.value
        else:
            goal_type = self.goal_type

        goal_needs_whole_amount: None | Unset | bool
        if isinstance(self.goal_needs_whole_amount, Unset):
            goal_needs_whole_amount = UNSET
        else:
            goal_needs_whole_amount = self.goal_needs_whole_amount

        goal_day: None | Unset | int
        if isinstance(self.goal_day, Unset):
            goal_day = UNSET
        else:
            goal_day = self.goal_day

        goal_cadence: None | Unset | int
        if isinstance(self.goal_cadence, Unset):
            goal_cadence = UNSET
        else:
            goal_cadence = self.goal_cadence

        goal_cadence_frequency: None | Unset | int
        if isinstance(self.goal_cadence_frequency, Unset):
            goal_cadence_frequency = UNSET
        else:
            goal_cadence_frequency = self.goal_cadence_frequency

        goal_creation_month: None | Unset | str
        if isinstance(self.goal_creation_month, Unset):
            goal_creation_month = UNSET
        elif isinstance(self.goal_creation_month, datetime.date):
            goal_creation_month = self.goal_creation_month.isoformat()
        else:
            goal_creation_month = self.goal_creation_month

        goal_target: None | Unset | int
        if isinstance(self.goal_target, Unset):
            goal_target = UNSET
        else:
            goal_target = self.goal_target

        goal_target_month: None | Unset | str
        if isinstance(self.goal_target_month, Unset):
            goal_target_month = UNSET
        elif isinstance(self.goal_target_month, datetime.date):
            goal_target_month = self.goal_target_month.isoformat()
        else:
            goal_target_month = self.goal_target_month

        goal_percentage_complete: None | Unset | int
        if isinstance(self.goal_percentage_complete, Unset):
            goal_percentage_complete = UNSET
        else:
            goal_percentage_complete = self.goal_percentage_complete

        goal_months_to_budget: None | Unset | int
        if isinstance(self.goal_months_to_budget, Unset):
            goal_months_to_budget = UNSET
        else:
            goal_months_to_budget = self.goal_months_to_budget

        goal_under_funded: None | Unset | int
        if isinstance(self.goal_under_funded, Unset):
            goal_under_funded = UNSET
        else:
            goal_under_funded = self.goal_under_funded

        goal_overall_funded: None | Unset | int
        if isinstance(self.goal_overall_funded, Unset):
            goal_overall_funded = UNSET
        else:
            goal_overall_funded = self.goal_overall_funded

        goal_overall_left: None | Unset | int
        if isinstance(self.goal_overall_left, Unset):
            goal_overall_left = UNSET
        else:
            goal_overall_left = self.goal_overall_left

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "category_group_id": category_group_id,
                "name": name,
                "hidden": hidden,
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        category_group_id = UUID(d.pop("category_group_id"))

        name = d.pop("name")

        hidden = d.pop("hidden")

        budgeted = d.pop("budgeted")

        activity = d.pop("activity")

        balance = d.pop("balance")

        deleted = d.pop("deleted")

        category_group_name = d.pop("category_group_name", UNSET)

        def _parse_original_category_group_id(data: object) -> None | UUID | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                original_category_group_id_type_0 = UUID(data)

                return original_category_group_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID | Unset, data)

        original_category_group_id = _parse_original_category_group_id(d.pop("original_category_group_id", UNSET))

        def _parse_note(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        note = _parse_note(d.pop("note", UNSET))

        def _parse_goal_type(
            data: object,
        ) -> CategoryGoalTypeType1 | CategoryGoalTypeType2Type1 | CategoryGoalTypeType3Type1 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_type_type_1 = CategoryGoalTypeType1(data)

                return goal_type_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_type_type_2_type_1 = CategoryGoalTypeType2Type1(data)

                return goal_type_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_type_type_3_type_1 = CategoryGoalTypeType3Type1(data)

                return goal_type_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                CategoryGoalTypeType1 | CategoryGoalTypeType2Type1 | CategoryGoalTypeType3Type1 | None | Unset, data
            )

        goal_type = _parse_goal_type(d.pop("goal_type", UNSET))

        def _parse_goal_needs_whole_amount(data: object) -> None | Unset | bool:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | bool, data)

        goal_needs_whole_amount = _parse_goal_needs_whole_amount(d.pop("goal_needs_whole_amount", UNSET))

        def _parse_goal_day(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_day = _parse_goal_day(d.pop("goal_day", UNSET))

        def _parse_goal_cadence(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_cadence = _parse_goal_cadence(d.pop("goal_cadence", UNSET))

        def _parse_goal_cadence_frequency(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_cadence_frequency = _parse_goal_cadence_frequency(d.pop("goal_cadence_frequency", UNSET))

        def _parse_goal_creation_month(data: object) -> None | Unset | datetime.date:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_creation_month_type_0 = isoparse(data).date()

                return goal_creation_month_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.date, data)

        goal_creation_month = _parse_goal_creation_month(d.pop("goal_creation_month", UNSET))

        def _parse_goal_target(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_target = _parse_goal_target(d.pop("goal_target", UNSET))

        def _parse_goal_target_month(data: object) -> None | Unset | datetime.date:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                goal_target_month_type_0 = isoparse(data).date()

                return goal_target_month_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.date, data)

        goal_target_month = _parse_goal_target_month(d.pop("goal_target_month", UNSET))

        def _parse_goal_percentage_complete(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_percentage_complete = _parse_goal_percentage_complete(d.pop("goal_percentage_complete", UNSET))

        def _parse_goal_months_to_budget(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_months_to_budget = _parse_goal_months_to_budget(d.pop("goal_months_to_budget", UNSET))

        def _parse_goal_under_funded(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_under_funded = _parse_goal_under_funded(d.pop("goal_under_funded", UNSET))

        def _parse_goal_overall_funded(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_overall_funded = _parse_goal_overall_funded(d.pop("goal_overall_funded", UNSET))

        def _parse_goal_overall_left(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_overall_left = _parse_goal_overall_left(d.pop("goal_overall_left", UNSET))

        category = cls(
            id=id,
            category_group_id=category_group_id,
            name=name,
            hidden=hidden,
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
            goal_percentage_complete=goal_percentage_complete,
            goal_months_to_budget=goal_months_to_budget,
            goal_under_funded=goal_under_funded,
            goal_overall_funded=goal_overall_funded,
            goal_overall_left=goal_overall_left,
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
