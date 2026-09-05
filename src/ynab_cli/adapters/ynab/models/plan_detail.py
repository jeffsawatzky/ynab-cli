from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.account import Account
    from ynab_cli.adapters.ynab.models.category_base import CategoryBase
    from ynab_cli.adapters.ynab.models.category_group import CategoryGroup
    from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
    from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0
    from ynab_cli.adapters.ynab.models.month_detail_base import MonthDetailBase
    from ynab_cli.adapters.ynab.models.payee import Payee
    from ynab_cli.adapters.ynab.models.payee_location import PayeeLocation
    from ynab_cli.adapters.ynab.models.scheduled_sub_transaction_base import ScheduledSubTransactionBase
    from ynab_cli.adapters.ynab.models.scheduled_transaction_summary_base import ScheduledTransactionSummaryBase
    from ynab_cli.adapters.ynab.models.sub_transaction_base import SubTransactionBase
    from ynab_cli.adapters.ynab.models.transaction_summary_base import TransactionSummaryBase


T = TypeVar("T", bound="PlanDetail")


@_attrs_define
class PlanDetail:
    """
    Attributes:
        id (UUID):
        name (str):
        last_modified_on (datetime.datetime | Unset): The last time any changes were made to the plan from either a web
            or mobile client
        first_month (datetime.date | Unset): The earliest plan month
        last_month (datetime.date | Unset): The latest plan month
        date_format (DateFormatType0 | None | Unset): The date format setting for the plan.  In some cases the format
            will not be available and will be specified as null.
        currency_format (CurrencyFormatType0 | None | Unset): The currency format setting for the plan.  In some cases
            the format will not be available and will be specified as null.
        accounts (list[Account] | Unset): The plan accounts (only included if `include_accounts=true` specified as query
            parameter)
        payees (list[Payee] | Unset):
        payee_locations (list[PayeeLocation] | Unset):
        category_groups (list[CategoryGroup] | Unset):
        categories (list[CategoryBase] | Unset):
        months (list[MonthDetailBase] | Unset):
        transactions (list[TransactionSummaryBase] | Unset):
        subtransactions (list[SubTransactionBase] | Unset):
        scheduled_transactions (list[ScheduledTransactionSummaryBase] | Unset):
        scheduled_subtransactions (list[ScheduledSubTransactionBase] | Unset):
    """

    id: UUID
    name: str
    last_modified_on: datetime.datetime | Unset = UNSET
    first_month: datetime.date | Unset = UNSET
    last_month: datetime.date | Unset = UNSET
    date_format: DateFormatType0 | Unset | None = UNSET
    currency_format: CurrencyFormatType0 | Unset | None = UNSET
    accounts: list[Account] | Unset = UNSET
    payees: list[Payee] | Unset = UNSET
    payee_locations: list[PayeeLocation] | Unset = UNSET
    category_groups: list[CategoryGroup] | Unset = UNSET
    categories: list[CategoryBase] | Unset = UNSET
    months: list[MonthDetailBase] | Unset = UNSET
    transactions: list[TransactionSummaryBase] | Unset = UNSET
    subtransactions: list[SubTransactionBase] | Unset = UNSET
    scheduled_transactions: list[ScheduledTransactionSummaryBase] | Unset = UNSET
    scheduled_subtransactions: list[ScheduledSubTransactionBase] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
        from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0

        id = str(self.id)

        name = self.name

        last_modified_on: str | Unset = UNSET
        if not isinstance(self.last_modified_on, Unset):
            last_modified_on = self.last_modified_on.isoformat()

        first_month: str | Unset = UNSET
        if not isinstance(self.first_month, Unset):
            first_month = self.first_month.isoformat()

        last_month: str | Unset = UNSET
        if not isinstance(self.last_month, Unset):
            last_month = self.last_month.isoformat()

        date_format: dict[str, Any] | Unset | None
        if isinstance(self.date_format, Unset):
            date_format = UNSET
        elif isinstance(self.date_format, DateFormatType0):
            date_format = self.date_format.to_dict()
        else:
            date_format = self.date_format

        currency_format: dict[str, Any] | Unset | None
        if isinstance(self.currency_format, Unset):
            currency_format = UNSET
        elif isinstance(self.currency_format, CurrencyFormatType0):
            currency_format = self.currency_format.to_dict()
        else:
            currency_format = self.currency_format

        accounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = []
            for accounts_item_data in self.accounts:
                accounts_item = accounts_item_data.to_dict()
                accounts.append(accounts_item)

        payees: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.payees, Unset):
            payees = []
            for payees_item_data in self.payees:
                payees_item = payees_item_data.to_dict()
                payees.append(payees_item)

        payee_locations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.payee_locations, Unset):
            payee_locations = []
            for payee_locations_item_data in self.payee_locations:
                payee_locations_item = payee_locations_item_data.to_dict()
                payee_locations.append(payee_locations_item)

        category_groups: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.category_groups, Unset):
            category_groups = []
            for category_groups_item_data in self.category_groups:
                category_groups_item = category_groups_item_data.to_dict()
                category_groups.append(category_groups_item)

        categories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        months: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.months, Unset):
            months = []
            for months_item_data in self.months:
                months_item = months_item_data.to_dict()
                months.append(months_item)

        transactions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.transactions, Unset):
            transactions = []
            for transactions_item_data in self.transactions:
                transactions_item = transactions_item_data.to_dict()
                transactions.append(transactions_item)

        subtransactions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.subtransactions, Unset):
            subtransactions = []
            for subtransactions_item_data in self.subtransactions:
                subtransactions_item = subtransactions_item_data.to_dict()
                subtransactions.append(subtransactions_item)

        scheduled_transactions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.scheduled_transactions, Unset):
            scheduled_transactions = []
            for scheduled_transactions_item_data in self.scheduled_transactions:
                scheduled_transactions_item = scheduled_transactions_item_data.to_dict()
                scheduled_transactions.append(scheduled_transactions_item)

        scheduled_subtransactions: list[dict[str, Any]] | Unset = UNSET
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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.account import Account
        from ynab_cli.adapters.ynab.models.category_base import CategoryBase
        from ynab_cli.adapters.ynab.models.category_group import CategoryGroup
        from ynab_cli.adapters.ynab.models.currency_format_type_0 import CurrencyFormatType0
        from ynab_cli.adapters.ynab.models.date_format_type_0 import DateFormatType0
        from ynab_cli.adapters.ynab.models.month_detail_base import MonthDetailBase
        from ynab_cli.adapters.ynab.models.payee import Payee
        from ynab_cli.adapters.ynab.models.payee_location import PayeeLocation
        from ynab_cli.adapters.ynab.models.scheduled_sub_transaction_base import ScheduledSubTransactionBase
        from ynab_cli.adapters.ynab.models.scheduled_transaction_summary_base import ScheduledTransactionSummaryBase
        from ynab_cli.adapters.ynab.models.sub_transaction_base import SubTransactionBase
        from ynab_cli.adapters.ynab.models.transaction_summary_base import TransactionSummaryBase

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        _last_modified_on = d.pop("last_modified_on", UNSET)
        last_modified_on: datetime.datetime | Unset
        if isinstance(_last_modified_on, Unset):
            last_modified_on = UNSET
        else:
            last_modified_on = datetime.datetime.fromisoformat(_last_modified_on)

        _first_month = d.pop("first_month", UNSET)
        first_month: datetime.date | Unset
        if isinstance(_first_month, Unset):
            first_month = UNSET
        else:
            first_month = datetime.date.fromisoformat(_first_month)

        _last_month = d.pop("last_month", UNSET)
        last_month: datetime.date | Unset
        if isinstance(_last_month, Unset):
            last_month = UNSET
        else:
            last_month = datetime.date.fromisoformat(_last_month)

        def _parse_date_format(data: object) -> DateFormatType0 | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_date_format_type_0 = DateFormatType0.from_dict(data)

                return componentsschemas_date_format_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DateFormatType0 | Unset | None, data)

        date_format = _parse_date_format(d.pop("date_format", UNSET))

        def _parse_currency_format(data: object) -> CurrencyFormatType0 | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_currency_format_type_0 = CurrencyFormatType0.from_dict(data)

                return componentsschemas_currency_format_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CurrencyFormatType0 | Unset | None, data)

        currency_format = _parse_currency_format(d.pop("currency_format", UNSET))

        _accounts = d.pop("accounts", UNSET)
        accounts: list[Account] | Unset = UNSET
        if _accounts is not UNSET:
            accounts = []
            for accounts_item_data in _accounts:
                accounts_item = Account.from_dict(accounts_item_data)

                accounts.append(accounts_item)

        _payees = d.pop("payees", UNSET)
        payees: list[Payee] | Unset = UNSET
        if _payees is not UNSET:
            payees = []
            for payees_item_data in _payees:
                payees_item = Payee.from_dict(payees_item_data)

                payees.append(payees_item)

        _payee_locations = d.pop("payee_locations", UNSET)
        payee_locations: list[PayeeLocation] | Unset = UNSET
        if _payee_locations is not UNSET:
            payee_locations = []
            for payee_locations_item_data in _payee_locations:
                payee_locations_item = PayeeLocation.from_dict(payee_locations_item_data)

                payee_locations.append(payee_locations_item)

        _category_groups = d.pop("category_groups", UNSET)
        category_groups: list[CategoryGroup] | Unset = UNSET
        if _category_groups is not UNSET:
            category_groups = []
            for category_groups_item_data in _category_groups:
                category_groups_item = CategoryGroup.from_dict(category_groups_item_data)

                category_groups.append(category_groups_item)

        _categories = d.pop("categories", UNSET)
        categories: list[CategoryBase] | Unset = UNSET
        if _categories is not UNSET:
            categories = []
            for categories_item_data in _categories:
                categories_item = CategoryBase.from_dict(categories_item_data)

                categories.append(categories_item)

        _months = d.pop("months", UNSET)
        months: list[MonthDetailBase] | Unset = UNSET
        if _months is not UNSET:
            months = []
            for months_item_data in _months:
                months_item = MonthDetailBase.from_dict(months_item_data)

                months.append(months_item)

        _transactions = d.pop("transactions", UNSET)
        transactions: list[TransactionSummaryBase] | Unset = UNSET
        if _transactions is not UNSET:
            transactions = []
            for transactions_item_data in _transactions:
                transactions_item = TransactionSummaryBase.from_dict(transactions_item_data)

                transactions.append(transactions_item)

        _subtransactions = d.pop("subtransactions", UNSET)
        subtransactions: list[SubTransactionBase] | Unset = UNSET
        if _subtransactions is not UNSET:
            subtransactions = []
            for subtransactions_item_data in _subtransactions:
                subtransactions_item = SubTransactionBase.from_dict(subtransactions_item_data)

                subtransactions.append(subtransactions_item)

        _scheduled_transactions = d.pop("scheduled_transactions", UNSET)
        scheduled_transactions: list[ScheduledTransactionSummaryBase] | Unset = UNSET
        if _scheduled_transactions is not UNSET:
            scheduled_transactions = []
            for scheduled_transactions_item_data in _scheduled_transactions:
                scheduled_transactions_item = ScheduledTransactionSummaryBase.from_dict(
                    scheduled_transactions_item_data
                )

                scheduled_transactions.append(scheduled_transactions_item)

        _scheduled_subtransactions = d.pop("scheduled_subtransactions", UNSET)
        scheduled_subtransactions: list[ScheduledSubTransactionBase] | Unset = UNSET
        if _scheduled_subtransactions is not UNSET:
            scheduled_subtransactions = []
            for scheduled_subtransactions_item_data in _scheduled_subtransactions:
                scheduled_subtransactions_item = ScheduledSubTransactionBase.from_dict(
                    scheduled_subtransactions_item_data
                )

                scheduled_subtransactions.append(scheduled_subtransactions_item)

        plan_detail = cls(
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

        plan_detail.additional_properties = d
        return plan_detail

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
