from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.scheduled_transaction_response_data import ScheduledTransactionResponseData


T = TypeVar("T", bound="ScheduledTransactionResponse")


@_attrs_define
class ScheduledTransactionResponse:
    """
    Attributes:
        data (ScheduledTransactionResponseData):
    """

    data: "ScheduledTransactionResponseData"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.scheduled_transaction_response_data import ScheduledTransactionResponseData

        d = dict(src_dict)
        data = ScheduledTransactionResponseData.from_dict(d.pop("data"))

        scheduled_transaction_response = cls(
            data=data,
        )

        scheduled_transaction_response.additional_properties = d
        return scheduled_transaction_response

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
