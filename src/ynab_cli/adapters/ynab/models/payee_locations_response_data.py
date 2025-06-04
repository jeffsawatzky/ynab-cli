from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.payee_location import PayeeLocation


T = TypeVar("T", bound="PayeeLocationsResponseData")


@_attrs_define
class PayeeLocationsResponseData:
    """
    Attributes:
        payee_locations (list['PayeeLocation']):
    """

    payee_locations: list["PayeeLocation"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payee_locations = []
        for payee_locations_item_data in self.payee_locations:
            payee_locations_item = payee_locations_item_data.to_dict()
            payee_locations.append(payee_locations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payee_locations": payee_locations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.payee_location import PayeeLocation

        d = dict(src_dict)
        payee_locations = []
        _payee_locations = d.pop("payee_locations")
        for payee_locations_item_data in _payee_locations:
            payee_locations_item = PayeeLocation.from_dict(payee_locations_item_data)

            payee_locations.append(payee_locations_item)

        payee_locations_response_data = cls(
            payee_locations=payee_locations,
        )

        payee_locations_response_data.additional_properties = d
        return payee_locations_response_data

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
