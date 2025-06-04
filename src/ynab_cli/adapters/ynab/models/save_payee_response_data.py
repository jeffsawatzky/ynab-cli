from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.payee import Payee


T = TypeVar("T", bound="SavePayeeResponseData")


@_attrs_define
class SavePayeeResponseData:
    """
    Attributes:
        payee (Payee):
        server_knowledge (int): The knowledge of the server
    """

    payee: "Payee"
    server_knowledge: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payee = self.payee.to_dict()

        server_knowledge = self.server_knowledge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payee": payee,
                "server_knowledge": server_knowledge,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.payee import Payee

        d = dict(src_dict)
        payee = Payee.from_dict(d.pop("payee"))

        server_knowledge = d.pop("server_knowledge")

        save_payee_response_data = cls(
            payee=payee,
            server_knowledge=server_knowledge,
        )

        save_payee_response_data.additional_properties = d
        return save_payee_response_data

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
