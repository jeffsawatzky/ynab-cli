from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.models.save_category_goal_frequency import SaveCategoryGoalFrequency
from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="ExistingCategory")


@_attrs_define
class ExistingCategory:
    """
    Attributes:
        name (None | str | Unset):
        note (None | str | Unset):
        category_group_id (UUID | Unset): The id of the category group to which this category belongs.  An internal
            category group may not be specified.
        goal_target (int | None | Unset): The goal target amount in milliunits format.  If value is specified and goal
            has not already been configured for category, a monthly goal will be created for the category with this target
            amount.  If goal_type is not specified, it will default to 'NEED' or 'MF' for Credit Card Payment categories.
            When updating a category, passing null removes any existing target.
        goal_target_date (datetime.date | None | Unset): The goal target date in ISO format (e.g. 2016-12-01).
        goal_needs_whole_amount (bool | None | Unset): Whether the goal requires the full target amount each period.
            Only supported for 'NEED' goals. When true, the goal is configured as 'Set aside another...'. When false, the
            goal is configured as 'Refill up to...'.
        goal_frequency (SaveCategoryGoalFrequency | Unset): When specified, configures a recurring 'NEED' target of
            goal_target that repeats at this frequency, replacing any existing target. Requires goal_target. Cannot be
            combined with goal_target_date and is not supported for Credit Card Payment categories. Omit to leave an
            existing target's cadence unchanged.
    """

    name: str | Unset | None = UNSET
    note: str | Unset | None = UNSET
    category_group_id: UUID | Unset = UNSET
    goal_target: int | Unset | None = UNSET
    goal_target_date: datetime.date | Unset | None = UNSET
    goal_needs_whole_amount: bool | Unset | None = UNSET
    goal_frequency: SaveCategoryGoalFrequency | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: str | Unset | None
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        note: str | Unset | None
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        category_group_id: str | Unset = UNSET
        if not isinstance(self.category_group_id, Unset):
            category_group_id = str(self.category_group_id)

        goal_target: int | Unset | None
        if isinstance(self.goal_target, Unset):
            goal_target = UNSET
        else:
            goal_target = self.goal_target

        goal_target_date: str | Unset | None
        if isinstance(self.goal_target_date, Unset):
            goal_target_date = UNSET
        elif isinstance(self.goal_target_date, datetime.date):
            goal_target_date = self.goal_target_date.isoformat()
        else:
            goal_target_date = self.goal_target_date

        goal_needs_whole_amount: bool | Unset | None
        if isinstance(self.goal_needs_whole_amount, Unset):
            goal_needs_whole_amount = UNSET
        else:
            goal_needs_whole_amount = self.goal_needs_whole_amount

        goal_frequency: str | Unset = UNSET
        if not isinstance(self.goal_frequency, Unset):
            goal_frequency = self.goal_frequency.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if note is not UNSET:
            field_dict["note"] = note
        if category_group_id is not UNSET:
            field_dict["category_group_id"] = category_group_id
        if goal_target is not UNSET:
            field_dict["goal_target"] = goal_target
        if goal_target_date is not UNSET:
            field_dict["goal_target_date"] = goal_target_date
        if goal_needs_whole_amount is not UNSET:
            field_dict["goal_needs_whole_amount"] = goal_needs_whole_amount
        if goal_frequency is not UNSET:
            field_dict["goal_frequency"] = goal_frequency

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_note(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        note = _parse_note(d.pop("note", UNSET))

        _category_group_id = d.pop("category_group_id", UNSET)
        category_group_id: UUID | Unset
        if isinstance(_category_group_id, Unset):
            category_group_id = UNSET
        else:
            category_group_id = UUID(_category_group_id)

        def _parse_goal_target(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        goal_target = _parse_goal_target(d.pop("goal_target", UNSET))

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

        def _parse_goal_needs_whole_amount(data: object) -> bool | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | Unset | None, data)

        goal_needs_whole_amount = _parse_goal_needs_whole_amount(d.pop("goal_needs_whole_amount", UNSET))

        _goal_frequency = d.pop("goal_frequency", UNSET)
        goal_frequency: SaveCategoryGoalFrequency | Unset
        if isinstance(_goal_frequency, Unset):
            goal_frequency = UNSET
        else:
            goal_frequency = SaveCategoryGoalFrequency(_goal_frequency)

        existing_category = cls(
            name=name,
            note=note,
            category_group_id=category_group_id,
            goal_target=goal_target,
            goal_target_date=goal_target_date,
            goal_needs_whole_amount=goal_needs_whole_amount,
            goal_frequency=goal_frequency,
        )

        existing_category.additional_properties = d
        return existing_category

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
