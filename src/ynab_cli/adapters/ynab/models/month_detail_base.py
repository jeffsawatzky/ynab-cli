from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.category_base import CategoryBase


T = TypeVar("T", bound="MonthDetailBase")


@_attrs_define
class MonthDetailBase:
    """
    Attributes:
        month (datetime.date):
        income (int): The total amount of transactions categorized to 'Inflow: Ready to Assign' in the month
        budgeted (int): The total amount assigned (budgeted) in the month
        activity (int): The total amount of transactions in the month, excluding those categorized to 'Inflow: Ready to
            Assign'
        to_be_budgeted (int): The available amount for 'Ready to Assign'
        deleted (bool): Whether or not the month has been deleted.  Deleted months will only be included in delta
            requests.
        categories (list[CategoryBase]): The plan month categories.  Amounts (budgeted, activity, balance, etc.) are
            specific to the {month} parameter specified.
        note (None | str | Unset):
        age_of_money (int | None | Unset): The Age of Money as of the month
    """

    month: datetime.date
    income: int
    budgeted: int
    activity: int
    to_be_budgeted: int
    deleted: bool
    categories: list[CategoryBase]
    note: str | Unset | None = UNSET
    age_of_money: int | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month = self.month.isoformat()

        income = self.income

        budgeted = self.budgeted

        activity = self.activity

        to_be_budgeted = self.to_be_budgeted

        deleted = self.deleted

        categories = []
        for categories_item_data in self.categories:
            categories_item = categories_item_data.to_dict()
            categories.append(categories_item)

        note: str | Unset | None
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        age_of_money: int | Unset | None
        if isinstance(self.age_of_money, Unset):
            age_of_money = UNSET
        else:
            age_of_money = self.age_of_money

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "month": month,
                "income": income,
                "budgeted": budgeted,
                "activity": activity,
                "to_be_budgeted": to_be_budgeted,
                "deleted": deleted,
                "categories": categories,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note
        if age_of_money is not UNSET:
            field_dict["age_of_money"] = age_of_money

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.category_base import CategoryBase

        d = dict(src_dict)
        month = datetime.date.fromisoformat(d.pop("month"))

        income = d.pop("income")

        budgeted = d.pop("budgeted")

        activity = d.pop("activity")

        to_be_budgeted = d.pop("to_be_budgeted")

        deleted = d.pop("deleted")

        categories = []
        _categories = d.pop("categories")
        for categories_item_data in _categories:
            categories_item = CategoryBase.from_dict(categories_item_data)

            categories.append(categories_item)

        def _parse_note(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        note = _parse_note(d.pop("note", UNSET))

        def _parse_age_of_money(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | Unset | None, data)

        age_of_money = _parse_age_of_money(d.pop("age_of_money", UNSET))

        month_detail_base = cls(
            month=month,
            income=income,
            budgeted=budgeted,
            activity=activity,
            to_be_budgeted=to_be_budgeted,
            deleted=deleted,
            categories=categories,
            note=note,
            age_of_money=age_of_money,
        )

        month_detail_base.additional_properties = d
        return month_detail_base

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
