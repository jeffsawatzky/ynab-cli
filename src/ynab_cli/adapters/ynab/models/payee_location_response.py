from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.payee_location_response_data import PayeeLocationResponseData


T = TypeVar("T", bound="PayeeLocationResponse")


@_attrs_define
class PayeeLocationResponse:
    """
    Attributes:
        data (PayeeLocationResponseData):
    """

    data: "PayeeLocationResponseData"
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
        from ynab_cli.adapters.ynab.models.payee_location_response_data import PayeeLocationResponseData

        d = dict(src_dict)
        data = PayeeLocationResponseData.from_dict(d.pop("data"))

        payee_location_response = cls(
            data=data,
        )

        payee_location_response.additional_properties = d
        return payee_location_response

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
