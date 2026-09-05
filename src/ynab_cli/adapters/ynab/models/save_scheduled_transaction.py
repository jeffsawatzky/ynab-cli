from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.models.scheduled_transaction_frequency import ScheduledTransactionFrequency
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_1 import TransactionFlagColorType1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_2_type_1 import TransactionFlagColorType2Type1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_3_type_1 import TransactionFlagColorType3Type1
from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="SaveScheduledTransaction")


@_attrs_define
class SaveScheduledTransaction:
    """
    Attributes:
        account_id (UUID):
        date (datetime.date): The scheduled transaction date in ISO format (e.g. 2016-12-01).  This should be a future
            date no more than 5 years into the future.
        amount (int | Unset): The scheduled transaction amount in milliunits format.
        payee_id (None | Unset | UUID): The payee for the scheduled transaction.  To create a transfer between two
            accounts, use the account transfer payee pointing to the target account.  Account transfer payees are specified
            as `transfer_payee_id` on the account resource.
        payee_name (None | str | Unset): The payee name for the the scheduled transaction.  If a `payee_name` value is
            provided and `payee_id` has a null value, the `payee_name` value will be used to resolve the payee by either (1)
            a payee with the same name or (2) creation of a new payee.
        category_id (None | Unset | UUID): The category for the scheduled transaction. Credit Card Payment categories
            are not permitted. Creating a split scheduled transaction is not currently supported.
        memo (None | str | Unset):
        flag_color (None | TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 |
            Unset): The transaction flag
        frequency (ScheduledTransactionFrequency | Unset): The scheduled transaction frequency
    """

    account_id: UUID
    date: datetime.date
    amount: int | Unset = UNSET
    payee_id: Unset | UUID | None = UNSET
    payee_name: str | Unset | None = UNSET
    category_id: Unset | UUID | None = UNSET
    memo: str | Unset | None = UNSET
    flag_color: (
        TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 | Unset | None
    ) = UNSET
    frequency: ScheduledTransactionFrequency | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id = str(self.account_id)

        date = self.date.isoformat()

        amount = self.amount

        payee_id: str | Unset | None
        if isinstance(self.payee_id, Unset):
            payee_id = UNSET
        elif isinstance(self.payee_id, UUID):
            payee_id = str(self.payee_id)
        else:
            payee_id = self.payee_id

        payee_name: str | Unset | None
        if isinstance(self.payee_name, Unset):
            payee_name = UNSET
        else:
            payee_name = self.payee_name

        category_id: str | Unset | None
        if isinstance(self.category_id, Unset):
            category_id = UNSET
        elif isinstance(self.category_id, UUID):
            category_id = str(self.category_id)
        else:
            category_id = self.category_id

        memo: str | Unset | None
        if isinstance(self.memo, Unset):
            memo = UNSET
        else:
            memo = self.memo

        flag_color: str | Unset | None
        if isinstance(self.flag_color, Unset):
            flag_color = UNSET
        elif isinstance(
            self.flag_color, (TransactionFlagColorType1, TransactionFlagColorType2Type1, TransactionFlagColorType3Type1)
        ):
            flag_color = self.flag_color.value
        else:
            flag_color = self.flag_color

        frequency: str | Unset = UNSET
        if not isinstance(self.frequency, Unset):
            frequency = self.frequency.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "date": date,
            }
        )
        if amount is not UNSET:
            field_dict["amount"] = amount
        if payee_id is not UNSET:
            field_dict["payee_id"] = payee_id
        if payee_name is not UNSET:
            field_dict["payee_name"] = payee_name
        if category_id is not UNSET:
            field_dict["category_id"] = category_id
        if memo is not UNSET:
            field_dict["memo"] = memo
        if flag_color is not UNSET:
            field_dict["flag_color"] = flag_color
        if frequency is not UNSET:
            field_dict["frequency"] = frequency

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        account_id = UUID(d.pop("account_id"))

        date = datetime.date.fromisoformat(d.pop("date"))

        amount = d.pop("amount", UNSET)

        def _parse_payee_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                payee_id_type_0 = UUID(data)

                return payee_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        payee_id = _parse_payee_id(d.pop("payee_id", UNSET))

        def _parse_payee_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        payee_name = _parse_payee_name(d.pop("payee_name", UNSET))

        def _parse_category_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_id_type_0 = UUID(data)

                return category_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        category_id = _parse_category_id(d.pop("category_id", UNSET))

        def _parse_memo(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        memo = _parse_memo(d.pop("memo", UNSET))

        def _parse_flag_color(
            data: object,
        ) -> TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_transaction_flag_color_type_1 = TransactionFlagColorType1(data)

                return componentsschemas_transaction_flag_color_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_transaction_flag_color_type_2_type_1 = TransactionFlagColorType2Type1(data)

                return componentsschemas_transaction_flag_color_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_transaction_flag_color_type_3_type_1 = TransactionFlagColorType3Type1(data)

                return componentsschemas_transaction_flag_color_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                TransactionFlagColorType1
                | TransactionFlagColorType2Type1
                | TransactionFlagColorType3Type1
                | Unset
                | None,
                data,
            )

        flag_color = _parse_flag_color(d.pop("flag_color", UNSET))

        _frequency = d.pop("frequency", UNSET)
        frequency: ScheduledTransactionFrequency | Unset
        if isinstance(_frequency, Unset):
            frequency = UNSET
        else:
            frequency = ScheduledTransactionFrequency(_frequency)

        save_scheduled_transaction = cls(
            account_id=account_id,
            date=date,
            amount=amount,
            payee_id=payee_id,
            payee_name=payee_name,
            category_id=category_id,
            memo=memo,
            flag_color=flag_color,
            frequency=frequency,
        )

        save_scheduled_transaction.additional_properties = d
        return save_scheduled_transaction

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
