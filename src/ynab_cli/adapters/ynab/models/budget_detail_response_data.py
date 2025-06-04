from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.budget_detail import BudgetDetail


T = TypeVar("T", bound="BudgetDetailResponseData")


@_attrs_define
class BudgetDetailResponseData:
    """
    Attributes:
        budget (BudgetDetail):
        server_knowledge (int): The knowledge of the server
    """

    budget: "BudgetDetail"
    server_knowledge: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        budget = self.budget.to_dict()

        server_knowledge = self.server_knowledge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "budget": budget,
                "server_knowledge": server_knowledge,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.budget_detail import BudgetDetail

        d = dict(src_dict)
        budget = BudgetDetail.from_dict(d.pop("budget"))

        server_knowledge = d.pop("server_knowledge")

        budget_detail_response_data = cls(
            budget=budget,
            server_knowledge=server_knowledge,
        )

        budget_detail_response_data.additional_properties = d
        return budget_detail_response_data

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
