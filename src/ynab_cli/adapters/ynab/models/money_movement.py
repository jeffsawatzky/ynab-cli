from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="MoneyMovement")


@_attrs_define
class MoneyMovement:
    """
    Attributes:
        id (UUID):
        amount (int): The amount of the money movement in milliunits format
        month (datetime.date | None | Unset): The month of the money movement in ISO format (e.g. 2024-01-01)
        moved_at (datetime.datetime | None | Unset): The date/time the money movement was processed on the server in ISO
            format (e.g. 2024-01-01T12:00:00Z)
        note (None | str | Unset):
        money_movement_group_id (None | Unset | UUID): The id of the money movement group this movement belongs to
        performed_by_user_id (None | Unset | UUID): The id of the user who performed the money movement
        from_category_id (None | Unset | UUID): The id of the category the money was moved from
        to_category_id (None | Unset | UUID): The id of the category the money was moved to
        amount_formatted (str | Unset): The money movement amount formatted in the plan's currency format
        amount_currency (float | Unset): The money movement amount as a decimal currency amount
    """

    id: UUID
    amount: int
    month: datetime.date | Unset | None = UNSET
    moved_at: datetime.datetime | Unset | None = UNSET
    note: str | Unset | None = UNSET
    money_movement_group_id: Unset | UUID | None = UNSET
    performed_by_user_id: Unset | UUID | None = UNSET
    from_category_id: Unset | UUID | None = UNSET
    to_category_id: Unset | UUID | None = UNSET
    amount_formatted: str | Unset = UNSET
    amount_currency: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        amount = self.amount

        month: str | Unset | None
        if isinstance(self.month, Unset):
            month = UNSET
        elif isinstance(self.month, datetime.date):
            month = self.month.isoformat()
        else:
            month = self.month

        moved_at: str | Unset | None
        if isinstance(self.moved_at, Unset):
            moved_at = UNSET
        elif isinstance(self.moved_at, datetime.datetime):
            moved_at = self.moved_at.isoformat()
        else:
            moved_at = self.moved_at

        note: str | Unset | None
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        money_movement_group_id: str | Unset | None
        if isinstance(self.money_movement_group_id, Unset):
            money_movement_group_id = UNSET
        elif isinstance(self.money_movement_group_id, UUID):
            money_movement_group_id = str(self.money_movement_group_id)
        else:
            money_movement_group_id = self.money_movement_group_id

        performed_by_user_id: str | Unset | None
        if isinstance(self.performed_by_user_id, Unset):
            performed_by_user_id = UNSET
        elif isinstance(self.performed_by_user_id, UUID):
            performed_by_user_id = str(self.performed_by_user_id)
        else:
            performed_by_user_id = self.performed_by_user_id

        from_category_id: str | Unset | None
        if isinstance(self.from_category_id, Unset):
            from_category_id = UNSET
        elif isinstance(self.from_category_id, UUID):
            from_category_id = str(self.from_category_id)
        else:
            from_category_id = self.from_category_id

        to_category_id: str | Unset | None
        if isinstance(self.to_category_id, Unset):
            to_category_id = UNSET
        elif isinstance(self.to_category_id, UUID):
            to_category_id = str(self.to_category_id)
        else:
            to_category_id = self.to_category_id

        amount_formatted = self.amount_formatted

        amount_currency = self.amount_currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "amount": amount,
            }
        )
        if month is not UNSET:
            field_dict["month"] = month
        if moved_at is not UNSET:
            field_dict["moved_at"] = moved_at
        if note is not UNSET:
            field_dict["note"] = note
        if money_movement_group_id is not UNSET:
            field_dict["money_movement_group_id"] = money_movement_group_id
        if performed_by_user_id is not UNSET:
            field_dict["performed_by_user_id"] = performed_by_user_id
        if from_category_id is not UNSET:
            field_dict["from_category_id"] = from_category_id
        if to_category_id is not UNSET:
            field_dict["to_category_id"] = to_category_id
        if amount_formatted is not UNSET:
            field_dict["amount_formatted"] = amount_formatted
        if amount_currency is not UNSET:
            field_dict["amount_currency"] = amount_currency

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        amount = d.pop("amount")

        def _parse_month(data: object) -> datetime.date | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                month_type_0 = datetime.date.fromisoformat(data)

                return month_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | Unset | None, data)

        month = _parse_month(d.pop("month", UNSET))

        def _parse_moved_at(data: object) -> datetime.datetime | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                moved_at_type_0 = datetime.datetime.fromisoformat(data)

                return moved_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | Unset | None, data)

        moved_at = _parse_moved_at(d.pop("moved_at", UNSET))

        def _parse_note(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        note = _parse_note(d.pop("note", UNSET))

        def _parse_money_movement_group_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                money_movement_group_id_type_0 = UUID(data)

                return money_movement_group_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        money_movement_group_id = _parse_money_movement_group_id(d.pop("money_movement_group_id", UNSET))

        def _parse_performed_by_user_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                performed_by_user_id_type_0 = UUID(data)

                return performed_by_user_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        performed_by_user_id = _parse_performed_by_user_id(d.pop("performed_by_user_id", UNSET))

        def _parse_from_category_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                from_category_id_type_0 = UUID(data)

                return from_category_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        from_category_id = _parse_from_category_id(d.pop("from_category_id", UNSET))

        def _parse_to_category_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                to_category_id_type_0 = UUID(data)

                return to_category_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        to_category_id = _parse_to_category_id(d.pop("to_category_id", UNSET))

        amount_formatted = d.pop("amount_formatted", UNSET)

        amount_currency = d.pop("amount_currency", UNSET)

        money_movement = cls(
            id=id,
            amount=amount,
            month=month,
            moved_at=moved_at,
            note=note,
            money_movement_group_id=money_movement_group_id,
            performed_by_user_id=performed_by_user_id,
            from_category_id=from_category_id,
            to_category_id=to_category_id,
            amount_formatted=amount_formatted,
            amount_currency=amount_currency,
        )

        money_movement.additional_properties = d
        return money_movement

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
