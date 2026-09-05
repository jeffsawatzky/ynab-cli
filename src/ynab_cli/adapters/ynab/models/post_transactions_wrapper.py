from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.new_transaction import NewTransaction


T = TypeVar("T", bound="PostTransactionsWrapper")


@_attrs_define
class PostTransactionsWrapper:
    """
    Attributes:
        transaction (NewTransaction | Unset):
        transactions (list[NewTransaction] | Unset):
    """

    transaction: NewTransaction | Unset = UNSET
    transactions: list[NewTransaction] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transaction: dict[str, Any] | Unset = UNSET
        if not isinstance(self.transaction, Unset):
            transaction = self.transaction.to_dict()

        transactions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.transactions, Unset):
            transactions = []
            for transactions_item_data in self.transactions:
                transactions_item = transactions_item_data.to_dict()
                transactions.append(transactions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if transaction is not UNSET:
            field_dict["transaction"] = transaction
        if transactions is not UNSET:
            field_dict["transactions"] = transactions

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.new_transaction import NewTransaction

        d = dict(src_dict)
        _transaction = d.pop("transaction", UNSET)
        transaction: NewTransaction | Unset
        if isinstance(_transaction, Unset):
            transaction = UNSET
        else:
            transaction = NewTransaction.from_dict(_transaction)

        _transactions = d.pop("transactions", UNSET)
        transactions: list[NewTransaction] | Unset = UNSET
        if _transactions is not UNSET:
            transactions = []
            for transactions_item_data in _transactions:
                transactions_item = NewTransaction.from_dict(transactions_item_data)

                transactions.append(transactions_item)

        post_transactions_wrapper = cls(
            transaction=transaction,
            transactions=transactions,
        )

        post_transactions_wrapper.additional_properties = d
        return post_transactions_wrapper

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
