from collections.abc import Mapping
from typing import Any, TypeVar, cast
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
        payee_id (Union[None, UUID, Unset]): The payee for the subtransaction.
        payee_name (Union[None, Unset, str]): The payee name.  If a `payee_name` value is provided and `payee_id` has a
            null value, the `payee_name` value will be used to resolve the payee by either (1) a matching payee rename rule
            (only if import_id is also specified on parent transaction) or (2) a payee with the same name or (3) creation of
            a new payee.
        category_id (Union[None, UUID, Unset]): The category for the subtransaction.  Credit Card Payment categories are
            not permitted and will be ignored if supplied.
        memo (Union[None, Unset, str]):
    """

    amount: int
    payee_id: None | UUID | Unset = UNSET
    payee_name: None | Unset | str = UNSET
    category_id: None | UUID | Unset = UNSET
    memo: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

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

        memo: None | Unset | str
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount")

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

        def _parse_memo(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

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
