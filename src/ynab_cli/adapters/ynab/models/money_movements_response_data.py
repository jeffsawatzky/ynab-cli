from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.money_movement import MoneyMovement


T = TypeVar("T", bound="MoneyMovementsResponseData")


@_attrs_define
class MoneyMovementsResponseData:
    """
    Attributes:
        money_movements (list[MoneyMovement]):
        server_knowledge (int): The knowledge of the server
    """

    money_movements: list[MoneyMovement]
    server_knowledge: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        money_movements = []
        for money_movements_item_data in self.money_movements:
            money_movements_item = money_movements_item_data.to_dict()
            money_movements.append(money_movements_item)

        server_knowledge = self.server_knowledge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "money_movements": money_movements,
                "server_knowledge": server_knowledge,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.money_movement import MoneyMovement

        d = dict(src_dict)
        money_movements = []
        _money_movements = d.pop("money_movements")
        for money_movements_item_data in _money_movements:
            money_movements_item = MoneyMovement.from_dict(money_movements_item_data)

            money_movements.append(money_movements_item)

        server_knowledge = d.pop("server_knowledge")

        money_movements_response_data = cls(
            money_movements=money_movements,
            server_knowledge=server_knowledge,
        )

        money_movements_response_data.additional_properties = d
        return money_movements_response_data

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
