from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="MoneyMovementGroup")


@_attrs_define
class MoneyMovementGroup:
    """
    Attributes:
        id (UUID):
        group_created_at (datetime.datetime): When the money movement group was created
        month (datetime.date): The month of the money movement group in ISO format (e.g. 2024-01-01)
        note (None | str | Unset):
        performed_by_user_id (None | Unset | UUID): The id of the user who performed the money movement group
    """

    id: UUID
    group_created_at: datetime.datetime
    month: datetime.date
    note: str | Unset | None = UNSET
    performed_by_user_id: Unset | UUID | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        group_created_at = self.group_created_at.isoformat()

        month = self.month.isoformat()

        note: str | Unset | None
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        performed_by_user_id: str | Unset | None
        if isinstance(self.performed_by_user_id, Unset):
            performed_by_user_id = UNSET
        elif isinstance(self.performed_by_user_id, UUID):
            performed_by_user_id = str(self.performed_by_user_id)
        else:
            performed_by_user_id = self.performed_by_user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "group_created_at": group_created_at,
                "month": month,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note
        if performed_by_user_id is not UNSET:
            field_dict["performed_by_user_id"] = performed_by_user_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        group_created_at = datetime.datetime.fromisoformat(d.pop("group_created_at"))

        month = datetime.date.fromisoformat(d.pop("month"))

        def _parse_note(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        note = _parse_note(d.pop("note", UNSET))

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

        money_movement_group = cls(
            id=id,
            group_created_at=group_created_at,
            month=month,
            note=note,
            performed_by_user_id=performed_by_user_id,
        )

        money_movement_group.additional_properties = d
        return money_movement_group

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
