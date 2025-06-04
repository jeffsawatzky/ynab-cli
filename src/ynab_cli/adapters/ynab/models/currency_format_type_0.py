from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CurrencyFormatType0")


@_attrs_define
class CurrencyFormatType0:
    """The currency format setting for the budget.  In some cases the format will not be available and will be specified as
    null.

        Attributes:
            iso_code (str):
            example_format (str):
            decimal_digits (int):
            decimal_separator (str):
            symbol_first (bool):
            group_separator (str):
            currency_symbol (str):
            display_symbol (bool):
    """

    iso_code: str
    example_format: str
    decimal_digits: int
    decimal_separator: str
    symbol_first: bool
    group_separator: str
    currency_symbol: str
    display_symbol: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        iso_code = self.iso_code

        example_format = self.example_format

        decimal_digits = self.decimal_digits

        decimal_separator = self.decimal_separator

        symbol_first = self.symbol_first

        group_separator = self.group_separator

        currency_symbol = self.currency_symbol

        display_symbol = self.display_symbol

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "iso_code": iso_code,
                "example_format": example_format,
                "decimal_digits": decimal_digits,
                "decimal_separator": decimal_separator,
                "symbol_first": symbol_first,
                "group_separator": group_separator,
                "currency_symbol": currency_symbol,
                "display_symbol": display_symbol,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        iso_code = d.pop("iso_code")

        example_format = d.pop("example_format")

        decimal_digits = d.pop("decimal_digits")

        decimal_separator = d.pop("decimal_separator")

        symbol_first = d.pop("symbol_first")

        group_separator = d.pop("group_separator")

        currency_symbol = d.pop("currency_symbol")

        display_symbol = d.pop("display_symbol")

        currency_format_type_0 = cls(
            iso_code=iso_code,
            example_format=example_format,
            decimal_digits=decimal_digits,
            decimal_separator=decimal_separator,
            symbol_first=symbol_first,
            group_separator=group_separator,
            currency_symbol=currency_symbol,
            display_symbol=display_symbol,
        )

        currency_format_type_0.additional_properties = d
        return currency_format_type_0

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
