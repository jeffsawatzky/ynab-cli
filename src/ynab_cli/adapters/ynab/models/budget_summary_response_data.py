from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.budget_summary import BudgetSummary


T = TypeVar("T", bound="BudgetSummaryResponseData")


@_attrs_define
class BudgetSummaryResponseData:
    """
    Attributes:
        budgets (list['BudgetSummary']):
        default_budget (Union[Unset, BudgetSummary]):
    """

    budgets: list["BudgetSummary"]
    default_budget: Union[Unset, "BudgetSummary"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        budgets = []
        for budgets_item_data in self.budgets:
            budgets_item = budgets_item_data.to_dict()
            budgets.append(budgets_item)

        default_budget: Unset | dict[str, Any] = UNSET
        if not isinstance(self.default_budget, Unset):
            default_budget = self.default_budget.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "budgets": budgets,
            }
        )
        if default_budget is not UNSET:
            field_dict["default_budget"] = default_budget

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.budget_summary import BudgetSummary

        d = dict(src_dict)
        budgets = []
        _budgets = d.pop("budgets")
        for budgets_item_data in _budgets:
            budgets_item = BudgetSummary.from_dict(budgets_item_data)

            budgets.append(budgets_item)

        _default_budget = d.pop("default_budget", UNSET)
        default_budget: Unset | BudgetSummary
        if not _default_budget or isinstance(_default_budget, Unset):
            default_budget = UNSET
        else:
            default_budget = BudgetSummary.from_dict(_default_budget)

        budget_summary_response_data = cls(
            budgets=budgets,
            default_budget=default_budget,
        )

        budget_summary_response_data.additional_properties = d
        return budget_summary_response_data

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
