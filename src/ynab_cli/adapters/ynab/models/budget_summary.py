import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.account import Account
    from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
    from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0


T = TypeVar("T", bound="BudgetSummary")


@_attrs_define
class BudgetSummary:
    """
    Attributes:
        id (UUID):
        name (str):
        last_modified_on (Union[Unset, datetime.datetime]): The last time any changes were made to the budget from
            either a web or mobile client
        first_month (Union[Unset, datetime.date]): The earliest budget month
        last_month (Union[Unset, datetime.date]): The latest budget month
        date_format (Union['DateFormatType0', None, Unset]): The date format setting for the budget.  In some cases the
            format will not be available and will be specified as null.
        currency_format (Union['CurrencyFormatType0', None, Unset]): The currency format setting for the budget.  In
            some cases the format will not be available and will be specified as null.
        accounts (Union[Unset, list['Account']]): The budget accounts (only included if `include_accounts=true`
            specified as query parameter)
    """

    id: UUID
    name: str
    last_modified_on: Unset | datetime.datetime = UNSET
    first_month: Unset | datetime.date = UNSET
    last_month: Unset | datetime.date = UNSET
    date_format: Union["DateFormatType0", None, Unset] = UNSET
    currency_format: Union["CurrencyFormatType0", None, Unset] = UNSET
    accounts: Unset | list["Account"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
        from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0

        id = str(self.id)

        name = self.name

        last_modified_on: Unset | str = UNSET
        if not isinstance(self.last_modified_on, Unset):
            last_modified_on = self.last_modified_on.isoformat()

        first_month: Unset | str = UNSET
        if not isinstance(self.first_month, Unset):
            first_month = self.first_month.isoformat()

        last_month: Unset | str = UNSET
        if not isinstance(self.last_month, Unset):
            last_month = self.last_month.isoformat()

        date_format: None | Unset | dict[str, Any]
        if isinstance(self.date_format, Unset):
            date_format = UNSET
        elif isinstance(self.date_format, DateFormatType0):
            date_format = self.date_format.to_dict()
        else:
            date_format = self.date_format

        currency_format: None | Unset | dict[str, Any]
        if isinstance(self.currency_format, Unset):
            currency_format = UNSET
        elif isinstance(self.currency_format, CurrencyFormatType0):
            currency_format = self.currency_format.to_dict()
        else:
            currency_format = self.currency_format

        accounts: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = []
            for accounts_item_data in self.accounts:
                accounts_item = accounts_item_data.to_dict()
                accounts.append(accounts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if last_modified_on is not UNSET:
            field_dict["last_modified_on"] = last_modified_on
        if first_month is not UNSET:
            field_dict["first_month"] = first_month
        if last_month is not UNSET:
            field_dict["last_month"] = last_month
        if date_format is not UNSET:
            field_dict["date_format"] = date_format
        if currency_format is not UNSET:
            field_dict["currency_format"] = currency_format
        if accounts is not UNSET:
            field_dict["accounts"] = accounts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.account import Account
        from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
        from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        _last_modified_on = d.pop("last_modified_on", UNSET)
        last_modified_on: Unset | datetime.datetime
        if isinstance(_last_modified_on, Unset):
            last_modified_on = UNSET
        else:
            last_modified_on = isoparse(_last_modified_on)

        _first_month = d.pop("first_month", UNSET)
        first_month: Unset | datetime.date
        if isinstance(_first_month, Unset):
            first_month = UNSET
        else:
            first_month = isoparse(_first_month).date()

        _last_month = d.pop("last_month", UNSET)
        last_month: Unset | datetime.date
        if isinstance(_last_month, Unset):
            last_month = UNSET
        else:
            last_month = isoparse(_last_month).date()

        def _parse_date_format(data: object) -> Union["DateFormatType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_date_format_type_0 = DateFormatType0.from_dict(data)

                return componentsschemas_date_format_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DateFormatType0", None, Unset], data)

        date_format = _parse_date_format(d.pop("date_format", UNSET))

        def _parse_currency_format(data: object) -> Union["CurrencyFormatType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_currency_format_type_0 = CurrencyFormatType0.from_dict(data)

                return componentsschemas_currency_format_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CurrencyFormatType0", None, Unset], data)

        currency_format = _parse_currency_format(d.pop("currency_format", UNSET))

        accounts = []
        _accounts = d.pop("accounts", UNSET)
        for accounts_item_data in _accounts or []:
            accounts_item = Account.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        budget_summary = cls(
            id=id,
            name=name,
            last_modified_on=last_modified_on,
            first_month=first_month,
            last_month=last_month,
            date_format=date_format,
            currency_format=currency_format,
            accounts=accounts,
        )

        budget_summary.additional_properties = d
        return budget_summary

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
