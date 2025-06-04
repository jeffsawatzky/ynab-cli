from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.models.account_type import AccountType

T = TypeVar("T", bound="SaveAccount")


@_attrs_define
class SaveAccount:
    """
    Attributes:
        name (str): The name of the account
        type_ (AccountType): The type of account
        balance (int): The current balance of the account in milliunits format
    """

    name: str
    type_: AccountType
    balance: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_.value

        balance = self.balance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "balance": balance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = AccountType(d.pop("type"))

        balance = d.pop("balance")

        save_account = cls(
            name=name,
            type_=type_,
            balance=balance,
        )

        save_account.additional_properties = d
        return save_account

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
