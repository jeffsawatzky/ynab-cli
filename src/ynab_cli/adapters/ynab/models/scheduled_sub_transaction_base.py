from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="ScheduledSubTransactionBase")


@_attrs_define
class ScheduledSubTransactionBase:
    """
    Attributes:
        id (UUID):
        scheduled_transaction_id (UUID):
        amount (int): The scheduled subtransaction amount in milliunits format
        deleted (bool): Whether or not the scheduled subtransaction has been deleted. Deleted scheduled subtransactions
            will only be included in delta requests.
        memo (None | str | Unset):
        payee_id (None | Unset | UUID):
        payee_name (None | str | Unset):
        category_id (None | Unset | UUID):
        category_name (None | str | Unset):
        transfer_account_id (None | Unset | UUID): If a transfer, the account_id which the scheduled subtransaction
            transfers to
    """

    id: UUID
    scheduled_transaction_id: UUID
    amount: int
    deleted: bool
    memo: str | Unset | None = UNSET
    payee_id: Unset | UUID | None = UNSET
    payee_name: str | Unset | None = UNSET
    category_id: Unset | UUID | None = UNSET
    category_name: str | Unset | None = UNSET
    transfer_account_id: Unset | UUID | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        scheduled_transaction_id = str(self.scheduled_transaction_id)

        amount = self.amount

        deleted = self.deleted

        memo: str | Unset | None
        if isinstance(self.memo, Unset):
            memo = UNSET
        else:
            memo = self.memo

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

        category_name: str | Unset | None
        if isinstance(self.category_name, Unset):
            category_name = UNSET
        else:
            category_name = self.category_name

        transfer_account_id: str | Unset | None
        if isinstance(self.transfer_account_id, Unset):
            transfer_account_id = UNSET
        elif isinstance(self.transfer_account_id, UUID):
            transfer_account_id = str(self.transfer_account_id)
        else:
            transfer_account_id = self.transfer_account_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "scheduled_transaction_id": scheduled_transaction_id,
                "amount": amount,
                "deleted": deleted,
            }
        )
        if memo is not UNSET:
            field_dict["memo"] = memo
        if payee_id is not UNSET:
            field_dict["payee_id"] = payee_id
        if payee_name is not UNSET:
            field_dict["payee_name"] = payee_name
        if category_id is not UNSET:
            field_dict["category_id"] = category_id
        if category_name is not UNSET:
            field_dict["category_name"] = category_name
        if transfer_account_id is not UNSET:
            field_dict["transfer_account_id"] = transfer_account_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        scheduled_transaction_id = UUID(d.pop("scheduled_transaction_id"))

        amount = d.pop("amount")

        deleted = d.pop("deleted")

        def _parse_memo(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        memo = _parse_memo(d.pop("memo", UNSET))

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

        def _parse_category_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        category_name = _parse_category_name(d.pop("category_name", UNSET))

        def _parse_transfer_account_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                transfer_account_id_type_0 = UUID(data)

                return transfer_account_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        transfer_account_id = _parse_transfer_account_id(d.pop("transfer_account_id", UNSET))

        scheduled_sub_transaction_base = cls(
            id=id,
            scheduled_transaction_id=scheduled_transaction_id,
            amount=amount,
            deleted=deleted,
            memo=memo,
            payee_id=payee_id,
            payee_name=payee_name,
            category_id=category_id,
            category_name=category_name,
            transfer_account_id=transfer_account_id,
        )

        scheduled_sub_transaction_base.additional_properties = d
        return scheduled_sub_transaction_base

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
