from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.budget_settings import BudgetSettings


T = TypeVar("T", bound="BudgetSettingsResponseData")


@_attrs_define
class BudgetSettingsResponseData:
    """
    Attributes:
        settings (BudgetSettings):
    """

    settings: "BudgetSettings"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings": settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.budget_settings import BudgetSettings

        d = dict(src_dict)
        settings = BudgetSettings.from_dict(d.pop("settings"))

        budget_settings_response_data = cls(
            settings=settings,
        )

        budget_settings_response_data.additional_properties = d
        return budget_settings_response_data

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
