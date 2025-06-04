from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CategoryGroup")


@_attrs_define
class CategoryGroup:
    """
    Attributes:
        id (UUID):
        name (str):
        hidden (bool): Whether or not the category group is hidden
        deleted (bool): Whether or not the category group has been deleted.  Deleted category groups will only be
            included in delta requests.
    """

    id: UUID
    name: str
    hidden: bool
    deleted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        hidden = self.hidden

        deleted = self.deleted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "hidden": hidden,
                "deleted": deleted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        hidden = d.pop("hidden")

        deleted = d.pop("deleted")

        category_group = cls(
            id=id,
            name=name,
            hidden=hidden,
            deleted=deleted,
        )

        category_group.additional_properties = d
        return category_group

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
