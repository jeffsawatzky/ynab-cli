from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="SaveCategory")


@_attrs_define
class SaveCategory:
    """
    Attributes:
        name (Union[None, Unset, str]):
        note (Union[None, Unset, str]):
        category_group_id (Union[Unset, UUID]):
        goal_target (Union[None, Unset, int]): The goal target amount in milliunits format.  This amount can only be
            changed if the category already has a configured goal (goal_type != null).
    """

    name: None | Unset | str = UNSET
    note: None | Unset | str = UNSET
    category_group_id: Unset | UUID = UNSET
    goal_target: None | Unset | int = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | Unset | str
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        note: None | Unset | str
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        category_group_id: Unset | str = UNSET
        if not isinstance(self.category_group_id, Unset):
            category_group_id = str(self.category_group_id)

        goal_target: None | Unset | int
        if isinstance(self.goal_target, Unset):
            goal_target = UNSET
        else:
            goal_target = self.goal_target

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if note is not UNSET:
            field_dict["note"] = note
        if category_group_id is not UNSET:
            field_dict["category_group_id"] = category_group_id
        if goal_target is not UNSET:
            field_dict["goal_target"] = goal_target

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_note(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        note = _parse_note(d.pop("note", UNSET))

        _category_group_id = d.pop("category_group_id", UNSET)
        category_group_id: Unset | UUID
        if isinstance(_category_group_id, Unset):
            category_group_id = UNSET
        else:
            category_group_id = UUID(_category_group_id)

        def _parse_goal_target(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        goal_target = _parse_goal_target(d.pop("goal_target", UNSET))

        save_category = cls(
            name=name,
            note=note,
            category_group_id=category_group_id,
            goal_target=goal_target,
        )

        save_category.additional_properties = d
        return save_category

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
