from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="SubTransaction")


@_attrs_define
class SubTransaction:
    """
    Attributes:
        id (str):
        transaction_id (str):
        amount (int): The subtransaction amount in milliunits format
        deleted (bool): Whether or not the subtransaction has been deleted.  Deleted subtransactions will only be
            included in delta requests.
        memo (Union[None, Unset, str]):
        payee_id (Union[None, UUID, Unset]):
        payee_name (Union[None, Unset, str]):
        category_id (Union[None, UUID, Unset]):
        category_name (Union[None, Unset, str]):
        transfer_account_id (Union[None, UUID, Unset]): If a transfer, the account_id which the subtransaction transfers
            to
        transfer_transaction_id (Union[None, Unset, str]): If a transfer, the id of transaction on the other side of the
            transfer
    """

    id: str
    transaction_id: str
    amount: int
    deleted: bool
    memo: None | Unset | str = UNSET
    payee_id: None | UUID | Unset = UNSET
    payee_name: None | Unset | str = UNSET
    category_id: None | UUID | Unset = UNSET
    category_name: None | Unset | str = UNSET
    transfer_account_id: None | UUID | Unset = UNSET
    transfer_transaction_id: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        transaction_id = self.transaction_id

        amount = self.amount

        deleted = self.deleted

        memo: None | Unset | str
        if isinstance(self.memo, Unset):
            memo = UNSET
        else:
            memo = self.memo

        payee_id: None | Unset | str
        if isinstance(self.payee_id, Unset):
            payee_id = UNSET
        elif isinstance(self.payee_id, UUID):
            payee_id = str(self.payee_id)
        else:
            payee_id = self.payee_id

        payee_name: None | Unset | str
        if isinstance(self.payee_name, Unset):
            payee_name = UNSET
        else:
            payee_name = self.payee_name

        category_id: None | Unset | str
        if isinstance(self.category_id, Unset):
            category_id = UNSET
        elif isinstance(self.category_id, UUID):
            category_id = str(self.category_id)
        else:
            category_id = self.category_id

        category_name: None | Unset | str
        if isinstance(self.category_name, Unset):
            category_name = UNSET
        else:
            category_name = self.category_name

        transfer_account_id: None | Unset | str
        if isinstance(self.transfer_account_id, Unset):
            transfer_account_id = UNSET
        elif isinstance(self.transfer_account_id, UUID):
            transfer_account_id = str(self.transfer_account_id)
        else:
            transfer_account_id = self.transfer_account_id

        transfer_transaction_id: None | Unset | str
        if isinstance(self.transfer_transaction_id, Unset):
            transfer_transaction_id = UNSET
        else:
            transfer_transaction_id = self.transfer_transaction_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "transaction_id": transaction_id,
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
        if transfer_transaction_id is not UNSET:
            field_dict["transfer_transaction_id"] = transfer_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        transaction_id = d.pop("transaction_id")

        amount = d.pop("amount")

        deleted = d.pop("deleted")

        def _parse_memo(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        memo = _parse_memo(d.pop("memo", UNSET))

        def _parse_payee_id(data: object) -> None | UUID | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                payee_id_type_0 = UUID(data)

                return payee_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID | Unset, data)

        payee_id = _parse_payee_id(d.pop("payee_id", UNSET))

        def _parse_payee_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        payee_name = _parse_payee_name(d.pop("payee_name", UNSET))

        def _parse_category_id(data: object) -> None | UUID | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_id_type_0 = UUID(data)

                return category_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID | Unset, data)

        category_id = _parse_category_id(d.pop("category_id", UNSET))

        def _parse_category_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        category_name = _parse_category_name(d.pop("category_name", UNSET))

        def _parse_transfer_account_id(data: object) -> None | UUID | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                transfer_account_id_type_0 = UUID(data)

                return transfer_account_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID | Unset, data)

        transfer_account_id = _parse_transfer_account_id(d.pop("transfer_account_id", UNSET))

        def _parse_transfer_transaction_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        transfer_transaction_id = _parse_transfer_transaction_id(d.pop("transfer_transaction_id", UNSET))

        sub_transaction = cls(
            id=id,
            transaction_id=transaction_id,
            amount=amount,
            deleted=deleted,
            memo=memo,
            payee_id=payee_id,
            payee_name=payee_name,
            category_id=category_id,
            category_name=category_name,
            transfer_account_id=transfer_account_id,
            transfer_transaction_id=transfer_transaction_id,
        )

        sub_transaction.additional_properties = d
        return sub_transaction

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
