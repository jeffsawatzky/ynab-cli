from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.category import Category


T = TypeVar("T", bound="MonthDetail")


@_attrs_define
class MonthDetail:
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
        categories (list[Category]): The plan month categories.  Amounts (budgeted, activity, balance, etc.) are
            specific to the {month} parameter specified.
        note (None | str | Unset):
        age_of_money (int | None | Unset): The Age of Money as of the month
        income_formatted (str | Unset): The total income formatted in the plan's currency format
        income_currency (float | Unset): The total income as a decimal currency amount
        budgeted_formatted (str | Unset): The total amount assigned formatted in the plan's currency format
        budgeted_currency (float | Unset): The total amount assigned as a decimal currency amount
        activity_formatted (str | Unset): The total activity amount formatted in the plan's currency format
        activity_currency (float | Unset): The total activity amount as a decimal currency amount
        to_be_budgeted_formatted (str | Unset): The available amount for 'Ready to Assign' formatted in the plan's
            currency format
        to_be_budgeted_currency (float | Unset): The available amount for 'Ready to Assign' as a decimal currency amount
    """

    month: datetime.date
    income: int
    budgeted: int
    activity: int
    to_be_budgeted: int
    deleted: bool
    categories: list[Category]
    note: str | Unset | None = UNSET
    age_of_money: int | Unset | None = UNSET
    income_formatted: str | Unset = UNSET
    income_currency: float | Unset = UNSET
    budgeted_formatted: str | Unset = UNSET
    budgeted_currency: float | Unset = UNSET
    activity_formatted: str | Unset = UNSET
    activity_currency: float | Unset = UNSET
    to_be_budgeted_formatted: str | Unset = UNSET
    to_be_budgeted_currency: float | Unset = UNSET
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

        income_formatted = self.income_formatted

        income_currency = self.income_currency

        budgeted_formatted = self.budgeted_formatted

        budgeted_currency = self.budgeted_currency

        activity_formatted = self.activity_formatted

        activity_currency = self.activity_currency

        to_be_budgeted_formatted = self.to_be_budgeted_formatted

        to_be_budgeted_currency = self.to_be_budgeted_currency

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
        if income_formatted is not UNSET:
            field_dict["income_formatted"] = income_formatted
        if income_currency is not UNSET:
            field_dict["income_currency"] = income_currency
        if budgeted_formatted is not UNSET:
            field_dict["budgeted_formatted"] = budgeted_formatted
        if budgeted_currency is not UNSET:
            field_dict["budgeted_currency"] = budgeted_currency
        if activity_formatted is not UNSET:
            field_dict["activity_formatted"] = activity_formatted
        if activity_currency is not UNSET:
            field_dict["activity_currency"] = activity_currency
        if to_be_budgeted_formatted is not UNSET:
            field_dict["to_be_budgeted_formatted"] = to_be_budgeted_formatted
        if to_be_budgeted_currency is not UNSET:
            field_dict["to_be_budgeted_currency"] = to_be_budgeted_currency

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.category import Category

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
            categories_item = Category.from_dict(categories_item_data)

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

        income_formatted = d.pop("income_formatted", UNSET)

        income_currency = d.pop("income_currency", UNSET)

        budgeted_formatted = d.pop("budgeted_formatted", UNSET)

        budgeted_currency = d.pop("budgeted_currency", UNSET)

        activity_formatted = d.pop("activity_formatted", UNSET)

        activity_currency = d.pop("activity_currency", UNSET)

        to_be_budgeted_formatted = d.pop("to_be_budgeted_formatted", UNSET)

        to_be_budgeted_currency = d.pop("to_be_budgeted_currency", UNSET)

        month_detail = cls(
            month=month,
            income=income,
            budgeted=budgeted,
            activity=activity,
            to_be_budgeted=to_be_budgeted,
            deleted=deleted,
            categories=categories,
            note=note,
            age_of_money=age_of_money,
            income_formatted=income_formatted,
            income_currency=income_currency,
            budgeted_formatted=budgeted_formatted,
            budgeted_currency=budgeted_currency,
            activity_formatted=activity_formatted,
            activity_currency=activity_currency,
            to_be_budgeted_formatted=to_be_budgeted_formatted,
            to_be_budgeted_currency=to_be_budgeted_currency,
        )

        month_detail.additional_properties = d
        return month_detail

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
