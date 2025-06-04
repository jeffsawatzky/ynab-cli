import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="MonthSummary")


@_attrs_define
class MonthSummary:
    """
    Attributes:
        month (datetime.date):
        income (int): The total amount of transactions categorized to 'Inflow: Ready to Assign' in the month
        budgeted (int): The total amount budgeted in the month
        activity (int): The total amount of transactions in the month, excluding those categorized to 'Inflow: Ready to
            Assign'
        to_be_budgeted (int): The available amount for 'Ready to Assign'
        deleted (bool): Whether or not the month has been deleted.  Deleted months will only be included in delta
            requests.
        note (Union[None, Unset, str]):
        age_of_money (Union[None, Unset, int]): The Age of Money as of the month
    """

    month: datetime.date
    income: int
    budgeted: int
    activity: int
    to_be_budgeted: int
    deleted: bool
    note: None | Unset | str = UNSET
    age_of_money: None | Unset | int = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month = self.month.isoformat()

        income = self.income

        budgeted = self.budgeted

        activity = self.activity

        to_be_budgeted = self.to_be_budgeted

        deleted = self.deleted

        note: None | Unset | str
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        age_of_money: None | Unset | int
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
            }
        )
        if note is not UNSET:
            field_dict["note"] = note
        if age_of_money is not UNSET:
            field_dict["age_of_money"] = age_of_money

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        month = isoparse(d.pop("month")).date()

        income = d.pop("income")

        budgeted = d.pop("budgeted")

        activity = d.pop("activity")

        to_be_budgeted = d.pop("to_be_budgeted")

        deleted = d.pop("deleted")

        def _parse_note(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        note = _parse_note(d.pop("note", UNSET))

        def _parse_age_of_money(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        age_of_money = _parse_age_of_money(d.pop("age_of_money", UNSET))

        month_summary = cls(
            month=month,
            income=income,
            budgeted=budgeted,
            activity=activity,
            to_be_budgeted=to_be_budgeted,
            deleted=deleted,
            note=note,
            age_of_money=age_of_money,
        )

        month_summary.additional_properties = d
        return month_summary

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
