from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="SaveSubTransaction")


@_attrs_define
class SaveSubTransaction:
    """
    Attributes:
        amount (int): The subtransaction amount in milliunits format.
        payee_id (None | Unset | UUID): The payee for the subtransaction.
        payee_name (None | str | Unset): The payee name.  If a `payee_name` value is provided and `payee_id` has a null
            value, the `payee_name` value will be used to resolve the payee by either (1) a matching payee rename rule (only
            if import_id is also specified on parent transaction) or (2) a payee with the same name or (3) creation of a new
            payee.
        category_id (None | Unset | UUID): The category for the subtransaction.  Credit Card Payment categories are not
            permitted and will be ignored if supplied.
        memo (None | str | Unset):
    """

    amount: int
    payee_id: Unset | UUID | None = UNSET
    payee_name: str | Unset | None = UNSET
    category_id: Unset | UUID | None = UNSET
    memo: str | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        payee_id: str | Unset | None
        if isinstance(self.payee_id, Unset):
            payee_id = UNSET
        elif isinstance(self.payee_id, UUID):
            payee_id = str(self.payee_id)
        else:
            payee_id = self.payee_id

        payee_name: str | Unset | None
        if isinstance(self.payee_name, Unset):
            payee_name = UNSET
        else:
            payee_name = self.payee_name

        category_id: str | Unset | None
        if isinstance(self.category_id, Unset):
            category_id = UNSET
        elif isinstance(self.category_id, UUID):
            category_id = str(self.category_id)
        else:
            category_id = self.category_id

        memo: str | Unset | None
        if isinstance(self.memo, Unset):
            memo = UNSET
        else:
            memo = self.memo

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
            }
        )
        if payee_id is not UNSET:
            field_dict["payee_id"] = payee_id
        if payee_name is not UNSET:
            field_dict["payee_name"] = payee_name
        if category_id is not UNSET:
            field_dict["category_id"] = category_id
        if memo is not UNSET:
            field_dict["memo"] = memo

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        amount = d.pop("amount")

        def _parse_payee_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                payee_id_type_0 = UUID(data)

                return payee_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        payee_id = _parse_payee_id(d.pop("payee_id", UNSET))

        def _parse_payee_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        payee_name = _parse_payee_name(d.pop("payee_name", UNSET))

        def _parse_category_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_id_type_0 = UUID(data)

                return category_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        category_id = _parse_category_id(d.pop("category_id", UNSET))

        def _parse_memo(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        memo = _parse_memo(d.pop("memo", UNSET))

        save_sub_transaction = cls(
            amount=amount,
            payee_id=payee_id,
            payee_name=payee_name,
            category_id=category_id,
            memo=memo,
        )

        save_sub_transaction.additional_properties = d
        return save_sub_transaction

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
