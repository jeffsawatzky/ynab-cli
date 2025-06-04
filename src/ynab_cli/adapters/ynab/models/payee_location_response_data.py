from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.payee_location import PayeeLocation


T = TypeVar("T", bound="PayeeLocationResponseData")


@_attrs_define
class PayeeLocationResponseData:
    """
    Attributes:
        payee_location (PayeeLocation):
    """

    payee_location: "PayeeLocation"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payee_location = self.payee_location.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payee_location": payee_location,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.payee_location import PayeeLocation

        d = dict(src_dict)
        payee_location = PayeeLocation.from_dict(d.pop("payee_location"))

        payee_location_response_data = cls(
            payee_location=payee_location,
        )

        payee_location_response_data.additional_properties = d
        return payee_location_response_data

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
