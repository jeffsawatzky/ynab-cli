from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BulkResponseDataBulk")


@_attrs_define
class BulkResponseDataBulk:
    """
    Attributes:
        transaction_ids (list[str]): The list of Transaction ids that were created.
        duplicate_import_ids (list[str]): If any Transactions were not created because they had an `import_id` matching
            a transaction already on the same account, the specified import_id(s) will be included in this list.
    """

    transaction_ids: list[str]
    duplicate_import_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transaction_ids = self.transaction_ids

        duplicate_import_ids = self.duplicate_import_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transaction_ids": transaction_ids,
                "duplicate_import_ids": duplicate_import_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transaction_ids = cast(list[str], d.pop("transaction_ids"))

        duplicate_import_ids = cast(list[str], d.pop("duplicate_import_ids"))

        bulk_response_data_bulk = cls(
            transaction_ids=transaction_ids,
            duplicate_import_ids=duplicate_import_ids,
        )

        bulk_response_data_bulk.additional_properties = d
        return bulk_response_data_bulk

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
