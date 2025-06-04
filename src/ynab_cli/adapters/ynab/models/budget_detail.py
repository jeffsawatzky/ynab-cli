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
    from ynab_cli.adapters.ynab.models.category import Category
    from ynab_cli.adapters.ynab.models.category_group import CategoryGroup
    from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
    from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0
    from ynab_cli.adapters.ynab.models.month_detail import MonthDetail
    from ynab_cli.adapters.ynab.models.payee import Payee
    from ynab_cli.adapters.ynab.models.payee_location import PayeeLocation
    from ynab_cli.adapters.ynab.models.scheduled_sub_transaction import ScheduledSubTransaction
    from ynab_cli.adapters.ynab.models.scheduled_transaction_summary import ScheduledTransactionSummary
    from ynab_cli.adapters.ynab.models.sub_transaction import SubTransaction
    from ynab_cli.adapters.ynab.models.transaction_summary import TransactionSummary


T = TypeVar("T", bound="BudgetDetail")


@_attrs_define
class BudgetDetail:
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
        payees (Union[Unset, list['Payee']]):
        payee_locations (Union[Unset, list['PayeeLocation']]):
        category_groups (Union[Unset, list['CategoryGroup']]):
        categories (Union[Unset, list['Category']]):
        months (Union[Unset, list['MonthDetail']]):
        transactions (Union[Unset, list['TransactionSummary']]):
        subtransactions (Union[Unset, list['SubTransaction']]):
        scheduled_transactions (Union[Unset, list['ScheduledTransactionSummary']]):
        scheduled_subtransactions (Union[Unset, list['ScheduledSubTransaction']]):
    """

    id: UUID
    name: str
    last_modified_on: Unset | datetime.datetime = UNSET
    first_month: Unset | datetime.date = UNSET
    last_month: Unset | datetime.date = UNSET
    date_format: Union["DateFormatType0", None, Unset] = UNSET
    currency_format: Union["CurrencyFormatType0", None, Unset] = UNSET
    accounts: Unset | list["Account"] = UNSET
    payees: Unset | list["Payee"] = UNSET
    payee_locations: Unset | list["PayeeLocation"] = UNSET
    category_groups: Unset | list["CategoryGroup"] = UNSET
    categories: Unset | list["Category"] = UNSET
    months: Unset | list["MonthDetail"] = UNSET
    transactions: Unset | list["TransactionSummary"] = UNSET
    subtransactions: Unset | list["SubTransaction"] = UNSET
    scheduled_transactions: Unset | list["ScheduledTransactionSummary"] = UNSET
    scheduled_subtransactions: Unset | list["ScheduledSubTransaction"] = UNSET
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

        payees: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.payees, Unset):
            payees = []
            for payees_item_data in self.payees:
                payees_item = payees_item_data.to_dict()
                payees.append(payees_item)

        payee_locations: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.payee_locations, Unset):
            payee_locations = []
            for payee_locations_item_data in self.payee_locations:
                payee_locations_item = payee_locations_item_data.to_dict()
                payee_locations.append(payee_locations_item)

        category_groups: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.category_groups, Unset):
            category_groups = []
            for category_groups_item_data in self.category_groups:
                category_groups_item = category_groups_item_data.to_dict()
                category_groups.append(category_groups_item)

        categories: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        months: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.months, Unset):
            months = []
            for months_item_data in self.months:
                months_item = months_item_data.to_dict()
                months.append(months_item)

        transactions: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.transactions, Unset):
            transactions = []
            for transactions_item_data in self.transactions:
                transactions_item = transactions_item_data.to_dict()
                transactions.append(transactions_item)

        subtransactions: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.subtransactions, Unset):
            subtransactions = []
            for subtransactions_item_data in self.subtransactions:
                subtransactions_item = subtransactions_item_data.to_dict()
                subtransactions.append(subtransactions_item)

        scheduled_transactions: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.scheduled_transactions, Unset):
            scheduled_transactions = []
            for scheduled_transactions_item_data in self.scheduled_transactions:
                scheduled_transactions_item = scheduled_transactions_item_data.to_dict()
                scheduled_transactions.append(scheduled_transactions_item)

        scheduled_subtransactions: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.scheduled_subtransactions, Unset):
            scheduled_subtransactions = []
            for scheduled_subtransactions_item_data in self.scheduled_subtransactions:
                scheduled_subtransactions_item = scheduled_subtransactions_item_data.to_dict()
                scheduled_subtransactions.append(scheduled_subtransactions_item)

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
        if payees is not UNSET:
            field_dict["payees"] = payees
        if payee_locations is not UNSET:
            field_dict["payee_locations"] = payee_locations
        if category_groups is not UNSET:
            field_dict["category_groups"] = category_groups
        if categories is not UNSET:
            field_dict["categories"] = categories
        if months is not UNSET:
            field_dict["months"] = months
        if transactions is not UNSET:
            field_dict["transactions"] = transactions
        if subtransactions is not UNSET:
            field_dict["subtransactions"] = subtransactions
        if scheduled_transactions is not UNSET:
            field_dict["scheduled_transactions"] = scheduled_transactions
        if scheduled_subtransactions is not UNSET:
            field_dict["scheduled_subtransactions"] = scheduled_subtransactions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.account import Account
        from ynab_cli.adapters.ynab.models.category import Category
        from ynab_cli.adapters.ynab.models.category_group import CategoryGroup
        from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
        from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0
        from ynab_cli.adapters.ynab.models.month_detail import MonthDetail
        from ynab_cli.adapters.ynab.models.payee import Payee
        from ynab_cli.adapters.ynab.models.payee_location import PayeeLocation
        from ynab_cli.adapters.ynab.models.scheduled_sub_transaction import ScheduledSubTransaction
        from ynab_cli.adapters.ynab.models.scheduled_transaction_summary import ScheduledTransactionSummary
        from ynab_cli.adapters.ynab.models.sub_transaction import SubTransaction
        from ynab_cli.adapters.ynab.models.transaction_summary import TransactionSummary

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

        payees = []
        _payees = d.pop("payees", UNSET)
        for payees_item_data in _payees or []:
            payees_item = Payee.from_dict(payees_item_data)

            payees.append(payees_item)

        payee_locations = []
        _payee_locations = d.pop("payee_locations", UNSET)
        for payee_locations_item_data in _payee_locations or []:
            payee_locations_item = PayeeLocation.from_dict(payee_locations_item_data)

            payee_locations.append(payee_locations_item)

        category_groups = []
        _category_groups = d.pop("category_groups", UNSET)
        for category_groups_item_data in _category_groups or []:
            category_groups_item = CategoryGroup.from_dict(category_groups_item_data)

            category_groups.append(category_groups_item)

        categories = []
        _categories = d.pop("categories", UNSET)
        for categories_item_data in _categories or []:
            categories_item = Category.from_dict(categories_item_data)

            categories.append(categories_item)

        months = []
        _months = d.pop("months", UNSET)
        for months_item_data in _months or []:
            months_item = MonthDetail.from_dict(months_item_data)

            months.append(months_item)

        transactions = []
        _transactions = d.pop("transactions", UNSET)
        for transactions_item_data in _transactions or []:
            transactions_item = TransactionSummary.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        subtransactions = []
        _subtransactions = d.pop("subtransactions", UNSET)
        for subtransactions_item_data in _subtransactions or []:
            subtransactions_item = SubTransaction.from_dict(subtransactions_item_data)

            subtransactions.append(subtransactions_item)

        scheduled_transactions = []
        _scheduled_transactions = d.pop("scheduled_transactions", UNSET)
        for scheduled_transactions_item_data in _scheduled_transactions or []:
            scheduled_transactions_item = ScheduledTransactionSummary.from_dict(scheduled_transactions_item_data)

            scheduled_transactions.append(scheduled_transactions_item)

        scheduled_subtransactions = []
        _scheduled_subtransactions = d.pop("scheduled_subtransactions", UNSET)
        for scheduled_subtransactions_item_data in _scheduled_subtransactions or []:
            scheduled_subtransactions_item = ScheduledSubTransaction.from_dict(scheduled_subtransactions_item_data)

            scheduled_subtransactions.append(scheduled_subtransactions_item)

        budget_detail = cls(
            id=id,
            name=name,
            last_modified_on=last_modified_on,
            first_month=first_month,
            last_month=last_month,
            date_format=date_format,
            currency_format=currency_format,
            accounts=accounts,
            payees=payees,
            payee_locations=payee_locations,
            category_groups=category_groups,
            categories=categories,
            months=months,
            transactions=transactions,
            subtransactions=subtransactions,
            scheduled_transactions=scheduled_transactions,
            scheduled_subtransactions=scheduled_subtransactions,
        )

        budget_detail.additional_properties = d
        return budget_detail

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
