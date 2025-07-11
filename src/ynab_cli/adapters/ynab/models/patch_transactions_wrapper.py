from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.save_transaction_with_id_or_import_id import SaveTransactionWithIdOrImportId


T = TypeVar("T", bound="PatchTransactionsWrapper")


@_attrs_define
class PatchTransactionsWrapper:
    """
    Attributes:
        transactions (list['SaveTransactionWithIdOrImportId']):
    """

    transactions: list["SaveTransactionWithIdOrImportId"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transactions = []
        for transactions_item_data in self.transactions:
            transactions_item = transactions_item_data.to_dict()
            transactions.append(transactions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transactions": transactions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.save_transaction_with_id_or_import_id import SaveTransactionWithIdOrImportId

        d = dict(src_dict)
        transactions = []
        _transactions = d.pop("transactions")
        for transactions_item_data in _transactions:
            transactions_item = SaveTransactionWithIdOrImportId.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        patch_transactions_wrapper = cls(
            transactions=transactions,
        )

        patch_transactions_wrapper.additional_properties = d
        return patch_transactions_wrapper

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
