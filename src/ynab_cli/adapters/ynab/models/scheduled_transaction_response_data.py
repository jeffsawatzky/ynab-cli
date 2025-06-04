from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.scheduled_transaction_detail import ScheduledTransactionDetail


T = TypeVar("T", bound="ScheduledTransactionResponseData")


@_attrs_define
class ScheduledTransactionResponseData:
    """
    Attributes:
        scheduled_transaction (ScheduledTransactionDetail):
    """

    scheduled_transaction: "ScheduledTransactionDetail"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scheduled_transaction = self.scheduled_transaction.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scheduled_transaction": scheduled_transaction,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.scheduled_transaction_detail import ScheduledTransactionDetail

        d = dict(src_dict)
        scheduled_transaction = ScheduledTransactionDetail.from_dict(d.pop("scheduled_transaction"))

        scheduled_transaction_response_data = cls(
            scheduled_transaction=scheduled_transaction,
        )

        scheduled_transaction_response_data.additional_properties = d
        return scheduled_transaction_response_data

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
