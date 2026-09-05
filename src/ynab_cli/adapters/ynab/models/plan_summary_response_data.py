from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.plan_summary import PlanSummary


T = TypeVar("T", bound="PlanSummaryResponseData")


@_attrs_define
class PlanSummaryResponseData:
    """
    Attributes:
        plans (list[PlanSummary]):
        default_plan (None | PlanSummary | Unset):
    """

    plans: list[PlanSummary]
    default_plan: PlanSummary | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ynab_cli.adapters.ynab.models.plan_summary import PlanSummary

        plans = []
        for plans_item_data in self.plans:
            plans_item = plans_item_data.to_dict()
            plans.append(plans_item)

        default_plan: dict[str, Any] | Unset | None
        if isinstance(self.default_plan, Unset):
            default_plan = UNSET
        elif isinstance(self.default_plan, PlanSummary):
            default_plan = self.default_plan.to_dict()
        else:
            default_plan = self.default_plan

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plans": plans,
            }
        )
        if default_plan is not UNSET:
            field_dict["default_plan"] = default_plan

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.plan_summary import PlanSummary

        d = dict(src_dict)
        plans = []
        _plans = d.pop("plans")
        for plans_item_data in _plans:
            plans_item = PlanSummary.from_dict(plans_item_data)

            plans.append(plans_item)

        def _parse_default_plan(data: object) -> PlanSummary | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_plan_type_1 = PlanSummary.from_dict(data)

                return default_plan_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(PlanSummary | Unset | None, data)

        default_plan = _parse_default_plan(d.pop("default_plan", UNSET))

        plan_summary_response_data = cls(
            plans=plans,
            default_plan=default_plan,
        )

        plan_summary_response_data.additional_properties = d
        return plan_summary_response_data

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
