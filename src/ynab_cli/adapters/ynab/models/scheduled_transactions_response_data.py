from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.scheduled_transaction_detail import ScheduledTransactionDetail


T = TypeVar("T", bound="ScheduledTransactionsResponseData")


@_attrs_define
class ScheduledTransactionsResponseData:
    """
    Attributes:
        scheduled_transactions (list['ScheduledTransactionDetail']):
        server_knowledge (int): The knowledge of the server
    """

    scheduled_transactions: list["ScheduledTransactionDetail"]
    server_knowledge: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scheduled_transactions = []
        for scheduled_transactions_item_data in self.scheduled_transactions:
            scheduled_transactions_item = scheduled_transactions_item_data.to_dict()
            scheduled_transactions.append(scheduled_transactions_item)

        server_knowledge = self.server_knowledge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scheduled_transactions": scheduled_transactions,
                "server_knowledge": server_knowledge,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.scheduled_transaction_detail import ScheduledTransactionDetail

        d = dict(src_dict)
        scheduled_transactions = []
        _scheduled_transactions = d.pop("scheduled_transactions")
        for scheduled_transactions_item_data in _scheduled_transactions:
            scheduled_transactions_item = ScheduledTransactionDetail.from_dict(scheduled_transactions_item_data)

            scheduled_transactions.append(scheduled_transactions_item)

        server_knowledge = d.pop("server_knowledge")

        scheduled_transactions_response_data = cls(
            scheduled_transactions=scheduled_transactions,
            server_knowledge=server_knowledge,
        )

        scheduled_transactions_response_data.additional_properties = d
        return scheduled_transactions_response_data

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
