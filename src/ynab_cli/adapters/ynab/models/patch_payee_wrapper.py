from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.save_payee import SavePayee


T = TypeVar("T", bound="PatchPayeeWrapper")


@_attrs_define
class PatchPayeeWrapper:
    """
    Attributes:
        payee (SavePayee):
    """

    payee: "SavePayee"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payee = self.payee.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payee": payee,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.save_payee import SavePayee

        d = dict(src_dict)
        payee = SavePayee.from_dict(d.pop("payee"))

        patch_payee_wrapper = cls(
            payee=payee,
        )

        patch_payee_wrapper.additional_properties = d
        return patch_payee_wrapper

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
