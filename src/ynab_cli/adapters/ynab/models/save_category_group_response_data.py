from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.category_group import CategoryGroup


T = TypeVar("T", bound="SaveCategoryGroupResponseData")


@_attrs_define
class SaveCategoryGroupResponseData:
    """
    Attributes:
        category_group (CategoryGroup):
        server_knowledge (int): The knowledge of the server
    """

    category_group: CategoryGroup
    server_knowledge: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category_group = self.category_group.to_dict()

        server_knowledge = self.server_knowledge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "category_group": category_group,
                "server_knowledge": server_knowledge,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.category_group import CategoryGroup

        d = dict(src_dict)
        category_group = CategoryGroup.from_dict(d.pop("category_group"))

        server_knowledge = d.pop("server_knowledge")

        save_category_group_response_data = cls(
            category_group=category_group,
            server_knowledge=server_knowledge,
        )

        save_category_group_response_data.additional_properties = d
        return save_category_group_response_data

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
