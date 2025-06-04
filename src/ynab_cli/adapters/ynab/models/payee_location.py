from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PayeeLocation")


@_attrs_define
class PayeeLocation:
    """
    Attributes:
        id (UUID):
        payee_id (UUID):
        latitude (str):
        longitude (str):
        deleted (bool): Whether or not the payee location has been deleted.  Deleted payee locations will only be
            included in delta requests.
    """

    id: UUID
    payee_id: UUID
    latitude: str
    longitude: str
    deleted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        payee_id = str(self.payee_id)

        latitude = self.latitude

        longitude = self.longitude

        deleted = self.deleted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "payee_id": payee_id,
                "latitude": latitude,
                "longitude": longitude,
                "deleted": deleted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        payee_id = UUID(d.pop("payee_id"))

        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        deleted = d.pop("deleted")

        payee_location = cls(
            id=id,
            payee_id=payee_id,
            latitude=latitude,
            longitude=longitude,
            deleted=deleted,
        )

        payee_location.additional_properties = d
        return payee_location

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
