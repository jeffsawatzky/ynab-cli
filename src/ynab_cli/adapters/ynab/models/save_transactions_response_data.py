from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.transaction_detail import TransactionDetail


T = TypeVar("T", bound="SaveTransactionsResponseData")


@_attrs_define
class SaveTransactionsResponseData:
    """
    Attributes:
        transaction_ids (list[str]): The transaction ids that were saved
        server_knowledge (int): The knowledge of the server
        transaction (Union[Unset, TransactionDetail]):
        transactions (Union[Unset, list['TransactionDetail']]): If multiple transactions were specified, the
            transactions that were saved
        duplicate_import_ids (Union[Unset, list[str]]): If multiple transactions were specified, a list of import_ids
            that were not created because of an existing `import_id` found on the same account
    """

    transaction_ids: list[str]
    server_knowledge: int
    transaction: Union[Unset, "TransactionDetail"] = UNSET
    transactions: Unset | list["TransactionDetail"] = UNSET
    duplicate_import_ids: Unset | list[str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transaction_ids = self.transaction_ids

        server_knowledge = self.server_knowledge

        transaction: Unset | dict[str, Any] = UNSET
        if not isinstance(self.transaction, Unset):
            transaction = self.transaction.to_dict()

        transactions: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.transactions, Unset):
            transactions = []
            for transactions_item_data in self.transactions:
                transactions_item = transactions_item_data.to_dict()
                transactions.append(transactions_item)

        duplicate_import_ids: Unset | list[str] = UNSET
        if not isinstance(self.duplicate_import_ids, Unset):
            duplicate_import_ids = self.duplicate_import_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transaction_ids": transaction_ids,
                "server_knowledge": server_knowledge,
            }
        )
        if transaction is not UNSET:
            field_dict["transaction"] = transaction
        if transactions is not UNSET:
            field_dict["transactions"] = transactions
        if duplicate_import_ids is not UNSET:
            field_dict["duplicate_import_ids"] = duplicate_import_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.transaction_detail import TransactionDetail

        d = dict(src_dict)
        transaction_ids = cast(list[str], d.pop("transaction_ids"))

        server_knowledge = d.pop("server_knowledge")

        _transaction = d.pop("transaction", UNSET)
        transaction: Unset | TransactionDetail
        if isinstance(_transaction, Unset):
            transaction = UNSET
        else:
            transaction = TransactionDetail.from_dict(_transaction)

        transactions = []
        _transactions = d.pop("transactions", UNSET)
        for transactions_item_data in _transactions or []:
            transactions_item = TransactionDetail.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        duplicate_import_ids = cast(list[str], d.pop("duplicate_import_ids", UNSET))

        save_transactions_response_data = cls(
            transaction_ids=transaction_ids,
            server_knowledge=server_knowledge,
            transaction=transaction,
            transactions=transactions,
            duplicate_import_ids=duplicate_import_ids,
        )

        save_transactions_response_data.additional_properties = d
        return save_transactions_response_data

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
