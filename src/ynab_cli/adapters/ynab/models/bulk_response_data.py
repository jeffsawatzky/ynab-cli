from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.bulk_response_data_bulk import BulkResponseDataBulk


T = TypeVar("T", bound="BulkResponseData")


@_attrs_define
class BulkResponseData:
    """
    Attributes:
        bulk (BulkResponseDataBulk):
    """

    bulk: "BulkResponseDataBulk"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bulk = self.bulk.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bulk": bulk,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.bulk_response_data_bulk import BulkResponseDataBulk

        d = dict(src_dict)
        bulk = BulkResponseDataBulk.from_dict(d.pop("bulk"))

        bulk_response_data = cls(
            bulk=bulk,
        )

        bulk_response_data.additional_properties = d
        return bulk_response_data

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
