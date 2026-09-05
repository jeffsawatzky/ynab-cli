from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
    from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0


T = TypeVar("T", bound="PlanSettings")


@_attrs_define
class PlanSettings:
    """
    Attributes:
        date_format (DateFormatType0 | None): The date format setting for the plan.  In some cases the format will not
            be available and will be specified as null.
        currency_format (CurrencyFormatType0 | None): The currency format setting for the plan.  In some cases the
            format will not be available and will be specified as null.
    """

    date_format: DateFormatType0 | None
    currency_format: CurrencyFormatType0 | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
        from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0

        date_format: dict[str, Any] | None
        if isinstance(self.date_format, DateFormatType0):
            date_format = self.date_format.to_dict()
        else:
            date_format = self.date_format

        currency_format: dict[str, Any] | None
        if isinstance(self.currency_format, CurrencyFormatType0):
            currency_format = self.currency_format.to_dict()
        else:
            currency_format = self.currency_format

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_format": date_format,
                "currency_format": currency_format,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
        from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0

        d = dict(src_dict)

        def _parse_date_format(data: object) -> DateFormatType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_date_format_type_0 = DateFormatType0.from_dict(data)

                return componentsschemas_date_format_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DateFormatType0 | None, data)

        date_format = _parse_date_format(d.pop("date_format"))

        def _parse_currency_format(data: object) -> CurrencyFormatType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_currency_format_type_0 = CurrencyFormatType0.from_dict(data)

                return componentsschemas_currency_format_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CurrencyFormatType0 | None, data)

        currency_format = _parse_currency_format(d.pop("currency_format"))

        plan_settings = cls(
            date_format=date_format,
            currency_format=currency_format,
        )

        plan_settings.additional_properties = d
        return plan_settings

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
