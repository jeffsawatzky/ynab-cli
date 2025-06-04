import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ynab_cli.adapters.ynab.models.account_type import AccountType
from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.loan_account_periodic_value_type_0 import LoanAccountPeriodicValueType0


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """
    Attributes:
        id (UUID):
        name (str):
        type_ (AccountType): The type of account
        on_budget (bool): Whether this account is on budget or not
        closed (bool): Whether this account is closed or not
        balance (int): The current balance of the account in milliunits format
        cleared_balance (int): The current cleared balance of the account in milliunits format
        uncleared_balance (int): The current uncleared balance of the account in milliunits format
        transfer_payee_id (Union[None, UUID]): The payee id which should be used when transferring to this account
        deleted (bool): Whether or not the account has been deleted.  Deleted accounts will only be included in delta
            requests.
        note (Union[None, Unset, str]):
        direct_import_linked (Union[Unset, bool]): Whether or not the account is linked to a financial institution for
            automatic transaction import.
        direct_import_in_error (Union[Unset, bool]): If an account linked to a financial institution
            (direct_import_linked=true) and the linked connection is not in a healthy state, this will be true.
        last_reconciled_at (Union[None, Unset, datetime.datetime]): A date/time specifying when the account was last
            reconciled.
        debt_original_balance (Union[None, Unset, int]): The original debt/loan account balance, specified in milliunits
            format.
        debt_interest_rates (Union['LoanAccountPeriodicValueType0', None, Unset]):
        debt_minimum_payments (Union['LoanAccountPeriodicValueType0', None, Unset]):
        debt_escrow_amounts (Union['LoanAccountPeriodicValueType0', None, Unset]):
    """

    id: UUID
    name: str
    type_: AccountType
    on_budget: bool
    closed: bool
    balance: int
    cleared_balance: int
    uncleared_balance: int
    transfer_payee_id: None | UUID
    deleted: bool
    note: None | Unset | str = UNSET
    direct_import_linked: Unset | bool = UNSET
    direct_import_in_error: Unset | bool = UNSET
    last_reconciled_at: None | Unset | datetime.datetime = UNSET
    debt_original_balance: None | Unset | int = UNSET
    debt_interest_rates: Union["LoanAccountPeriodicValueType0", None, Unset] = UNSET
    debt_minimum_payments: Union["LoanAccountPeriodicValueType0", None, Unset] = UNSET
    debt_escrow_amounts: Union["LoanAccountPeriodicValueType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ynab_cli.adapters.ynab.models.loan_account_periodic_value_type_0 import LoanAccountPeriodicValueType0

        id = str(self.id)

        name = self.name

        type_ = self.type_.value

        on_budget = self.on_budget

        closed = self.closed

        balance = self.balance

        cleared_balance = self.cleared_balance

        uncleared_balance = self.uncleared_balance

        transfer_payee_id: None | str
        if isinstance(self.transfer_payee_id, UUID):
            transfer_payee_id = str(self.transfer_payee_id)
        else:
            transfer_payee_id = self.transfer_payee_id

        deleted = self.deleted

        note: None | Unset | str
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        direct_import_linked = self.direct_import_linked

        direct_import_in_error = self.direct_import_in_error

        last_reconciled_at: None | Unset | str
        if isinstance(self.last_reconciled_at, Unset):
            last_reconciled_at = UNSET
        elif isinstance(self.last_reconciled_at, datetime.datetime):
            last_reconciled_at = self.last_reconciled_at.isoformat()
        else:
            last_reconciled_at = self.last_reconciled_at

        debt_original_balance: None | Unset | int
        if isinstance(self.debt_original_balance, Unset):
            debt_original_balance = UNSET
        else:
            debt_original_balance = self.debt_original_balance

        debt_interest_rates: None | Unset | dict[str, Any]
        if isinstance(self.debt_interest_rates, Unset):
            debt_interest_rates = UNSET
        elif isinstance(self.debt_interest_rates, LoanAccountPeriodicValueType0):
            debt_interest_rates = self.debt_interest_rates.to_dict()
        else:
            debt_interest_rates = self.debt_interest_rates

        debt_minimum_payments: None | Unset | dict[str, Any]
        if isinstance(self.debt_minimum_payments, Unset):
            debt_minimum_payments = UNSET
        elif isinstance(self.debt_minimum_payments, LoanAccountPeriodicValueType0):
            debt_minimum_payments = self.debt_minimum_payments.to_dict()
        else:
            debt_minimum_payments = self.debt_minimum_payments

        debt_escrow_amounts: None | Unset | dict[str, Any]
        if isinstance(self.debt_escrow_amounts, Unset):
            debt_escrow_amounts = UNSET
        elif isinstance(self.debt_escrow_amounts, LoanAccountPeriodicValueType0):
            debt_escrow_amounts = self.debt_escrow_amounts.to_dict()
        else:
            debt_escrow_amounts = self.debt_escrow_amounts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type_,
                "on_budget": on_budget,
                "closed": closed,
                "balance": balance,
                "cleared_balance": cleared_balance,
                "uncleared_balance": uncleared_balance,
                "transfer_payee_id": transfer_payee_id,
                "deleted": deleted,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note
        if direct_import_linked is not UNSET:
            field_dict["direct_import_linked"] = direct_import_linked
        if direct_import_in_error is not UNSET:
            field_dict["direct_import_in_error"] = direct_import_in_error
        if last_reconciled_at is not UNSET:
            field_dict["last_reconciled_at"] = last_reconciled_at
        if debt_original_balance is not UNSET:
            field_dict["debt_original_balance"] = debt_original_balance
        if debt_interest_rates is not UNSET:
            field_dict["debt_interest_rates"] = debt_interest_rates
        if debt_minimum_payments is not UNSET:
            field_dict["debt_minimum_payments"] = debt_minimum_payments
        if debt_escrow_amounts is not UNSET:
            field_dict["debt_escrow_amounts"] = debt_escrow_amounts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.loan_account_periodic_value_type_0 import LoanAccountPeriodicValueType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        type_ = AccountType(d.pop("type"))

        on_budget = d.pop("on_budget")

        closed = d.pop("closed")

        balance = d.pop("balance")

        cleared_balance = d.pop("cleared_balance")

        uncleared_balance = d.pop("uncleared_balance")

        def _parse_transfer_payee_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                transfer_payee_id_type_0 = UUID(data)

                return transfer_payee_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID, data)

        transfer_payee_id = _parse_transfer_payee_id(d.pop("transfer_payee_id"))

        deleted = d.pop("deleted")

        def _parse_note(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        note = _parse_note(d.pop("note", UNSET))

        direct_import_linked = d.pop("direct_import_linked", UNSET)

        direct_import_in_error = d.pop("direct_import_in_error", UNSET)

        def _parse_last_reconciled_at(data: object) -> None | Unset | datetime.datetime:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_reconciled_at_type_0 = isoparse(data)

                return last_reconciled_at_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.datetime, data)

        last_reconciled_at = _parse_last_reconciled_at(d.pop("last_reconciled_at", UNSET))

        def _parse_debt_original_balance(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        debt_original_balance = _parse_debt_original_balance(d.pop("debt_original_balance", UNSET))

        def _parse_debt_interest_rates(data: object) -> Union["LoanAccountPeriodicValueType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_loan_account_periodic_value_type_0 = LoanAccountPeriodicValueType0.from_dict(data)

                return componentsschemas_loan_account_periodic_value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LoanAccountPeriodicValueType0", None, Unset], data)

        debt_interest_rates = _parse_debt_interest_rates(d.pop("debt_interest_rates", UNSET))

        def _parse_debt_minimum_payments(data: object) -> Union["LoanAccountPeriodicValueType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_loan_account_periodic_value_type_0 = LoanAccountPeriodicValueType0.from_dict(data)

                return componentsschemas_loan_account_periodic_value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LoanAccountPeriodicValueType0", None, Unset], data)

        debt_minimum_payments = _parse_debt_minimum_payments(d.pop("debt_minimum_payments", UNSET))

        def _parse_debt_escrow_amounts(data: object) -> Union["LoanAccountPeriodicValueType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_loan_account_periodic_value_type_0 = LoanAccountPeriodicValueType0.from_dict(data)

                return componentsschemas_loan_account_periodic_value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LoanAccountPeriodicValueType0", None, Unset], data)

        debt_escrow_amounts = _parse_debt_escrow_amounts(d.pop("debt_escrow_amounts", UNSET))

        account = cls(
            id=id,
            name=name,
            type_=type_,
            on_budget=on_budget,
            closed=closed,
            balance=balance,
            cleared_balance=cleared_balance,
            uncleared_balance=uncleared_balance,
            transfer_payee_id=transfer_payee_id,
            deleted=deleted,
            note=note,
            direct_import_linked=direct_import_linked,
            direct_import_in_error=direct_import_in_error,
            last_reconciled_at=last_reconciled_at,
            debt_original_balance=debt_original_balance,
            debt_interest_rates=debt_interest_rates,
            debt_minimum_payments=debt_minimum_payments,
            debt_escrow_amounts=debt_escrow_amounts,
        )

        account.additional_properties = d
        return account

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
