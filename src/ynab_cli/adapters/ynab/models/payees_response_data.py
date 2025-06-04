from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.payee import Payee


T = TypeVar("T", bound="PayeesResponseData")


@_attrs_define
class PayeesResponseData:
    """
    Attributes:
        payees (list['Payee']):
        server_knowledge (int): The knowledge of the server
    """

    payees: list["Payee"]
    server_knowledge: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payees = []
        for payees_item_data in self.payees:
            payees_item = payees_item_data.to_dict()
            payees.append(payees_item)

        server_knowledge = self.server_knowledge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payees": payees,
                "server_knowledge": server_knowledge,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.payee import Payee

        d = dict(src_dict)
        payees = []
        _payees = d.pop("payees")
        for payees_item_data in _payees:
            payees_item = Payee.from_dict(payees_item_data)

            payees.append(payees_item)

        server_knowledge = d.pop("server_knowledge")

        payees_response_data = cls(
            payees=payees,
            server_knowledge=server_knowledge,
        )

        payees_response_data.additional_properties = d
        return payees_response_data

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
