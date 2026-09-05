from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.models.scheduled_transaction_summary_base_frequency import (
    ScheduledTransactionSummaryBaseFrequency,
)
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_1 import TransactionFlagColorType1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_2_type_1 import TransactionFlagColorType2Type1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_3_type_1 import TransactionFlagColorType3Type1
from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.scheduled_sub_transaction import ScheduledSubTransaction


T = TypeVar("T", bound="ScheduledTransactionDetail")


@_attrs_define
class ScheduledTransactionDetail:
    """
    Attributes:
        id (UUID):
        date_first (datetime.date): The first date for which the Scheduled Transaction was scheduled.
        date_next (datetime.date): The next date for which the Scheduled Transaction is scheduled.
        frequency (ScheduledTransactionSummaryBaseFrequency):
        amount (int): The scheduled transaction amount in milliunits format
        account_id (UUID):
        deleted (bool): Whether or not the scheduled transaction has been deleted.  Deleted scheduled transactions will
            only be included in delta requests.
        account_name (str):
        subtransactions (list[ScheduledSubTransaction]): If a split scheduled transaction, the subtransactions.
        memo (None | str | Unset):
        flag_color (None | TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 |
            Unset): The transaction flag
        flag_name (None | str | Unset): The customized name of a transaction flag
        payee_id (None | Unset | UUID):
        category_id (None | Unset | UUID):
        transfer_account_id (None | Unset | UUID): If a transfer, the account_id which the scheduled transaction
            transfers to
        amount_formatted (str | Unset): The scheduled transaction amount formatted in the plan's currency format
        amount_currency (float | Unset): The scheduled transaction amount as a decimal currency amount
        payee_name (None | str | Unset):
        category_name (None | str | Unset): The name of the category.  If a split scheduled transaction, this will be
            'Split'.
    """

    id: UUID
    date_first: datetime.date
    date_next: datetime.date
    frequency: ScheduledTransactionSummaryBaseFrequency
    amount: int
    account_id: UUID
    deleted: bool
    account_name: str
    subtransactions: list[ScheduledSubTransaction]
    memo: str | Unset | None = UNSET
    flag_color: (
        TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 | Unset | None
    ) = UNSET
    flag_name: str | Unset | None = UNSET
    payee_id: Unset | UUID | None = UNSET
    category_id: Unset | UUID | None = UNSET
    transfer_account_id: Unset | UUID | None = UNSET
    amount_formatted: str | Unset = UNSET
    amount_currency: float | Unset = UNSET
    payee_name: str | Unset | None = UNSET
    category_name: str | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        date_first = self.date_first.isoformat()

        date_next = self.date_next.isoformat()

        frequency = self.frequency.value

        amount = self.amount

        account_id = str(self.account_id)

        deleted = self.deleted

        account_name = self.account_name

        subtransactions = []
        for subtransactions_item_data in self.subtransactions:
            subtransactions_item = subtransactions_item_data.to_dict()
            subtransactions.append(subtransactions_item)

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

        flag_name: str | Unset | None
        if isinstance(self.flag_name, Unset):
            flag_name = UNSET
        else:
            flag_name = self.flag_name

        payee_id: str | Unset | None
        if isinstance(self.payee_id, Unset):
            payee_id = UNSET
        elif isinstance(self.payee_id, UUID):
            payee_id = str(self.payee_id)
        else:
            payee_id = self.payee_id

        category_id: str | Unset | None
        if isinstance(self.category_id, Unset):
            category_id = UNSET
        elif isinstance(self.category_id, UUID):
            category_id = str(self.category_id)
        else:
            category_id = self.category_id

        transfer_account_id: str | Unset | None
        if isinstance(self.transfer_account_id, Unset):
            transfer_account_id = UNSET
        elif isinstance(self.transfer_account_id, UUID):
            transfer_account_id = str(self.transfer_account_id)
        else:
            transfer_account_id = self.transfer_account_id

        amount_formatted = self.amount_formatted

        amount_currency = self.amount_currency

        payee_name: str | Unset | None
        if isinstance(self.payee_name, Unset):
            payee_name = UNSET
        else:
            payee_name = self.payee_name

        category_name: str | Unset | None
        if isinstance(self.category_name, Unset):
            category_name = UNSET
        else:
            category_name = self.category_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "date_first": date_first,
                "date_next": date_next,
                "frequency": frequency,
                "amount": amount,
                "account_id": account_id,
                "deleted": deleted,
                "account_name": account_name,
                "subtransactions": subtransactions,
            }
        )
        if memo is not UNSET:
            field_dict["memo"] = memo
        if flag_color is not UNSET:
            field_dict["flag_color"] = flag_color
        if flag_name is not UNSET:
            field_dict["flag_name"] = flag_name
        if payee_id is not UNSET:
            field_dict["payee_id"] = payee_id
        if category_id is not UNSET:
            field_dict["category_id"] = category_id
        if transfer_account_id is not UNSET:
            field_dict["transfer_account_id"] = transfer_account_id
        if amount_formatted is not UNSET:
            field_dict["amount_formatted"] = amount_formatted
        if amount_currency is not UNSET:
            field_dict["amount_currency"] = amount_currency
        if payee_name is not UNSET:
            field_dict["payee_name"] = payee_name
        if category_name is not UNSET:
            field_dict["category_name"] = category_name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ynab_cli.adapters.ynab.models.scheduled_sub_transaction import ScheduledSubTransaction

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        date_first = datetime.date.fromisoformat(d.pop("date_first"))

        date_next = datetime.date.fromisoformat(d.pop("date_next"))

        frequency = ScheduledTransactionSummaryBaseFrequency(d.pop("frequency"))

        amount = d.pop("amount")

        account_id = UUID(d.pop("account_id"))

        deleted = d.pop("deleted")

        account_name = d.pop("account_name")

        subtransactions = []
        _subtransactions = d.pop("subtransactions")
        for subtransactions_item_data in _subtransactions:
            subtransactions_item = ScheduledSubTransaction.from_dict(subtransactions_item_data)

            subtransactions.append(subtransactions_item)

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

        def _parse_flag_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        flag_name = _parse_flag_name(d.pop("flag_name", UNSET))

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

        def _parse_transfer_account_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                transfer_account_id_type_0 = UUID(data)

                return transfer_account_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Unset | UUID | None, data)

        transfer_account_id = _parse_transfer_account_id(d.pop("transfer_account_id", UNSET))

        amount_formatted = d.pop("amount_formatted", UNSET)

        amount_currency = d.pop("amount_currency", UNSET)

        def _parse_payee_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        payee_name = _parse_payee_name(d.pop("payee_name", UNSET))

        def _parse_category_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        category_name = _parse_category_name(d.pop("category_name", UNSET))

        scheduled_transaction_detail = cls(
            id=id,
            date_first=date_first,
            date_next=date_next,
            frequency=frequency,
            amount=amount,
            account_id=account_id,
            deleted=deleted,
            account_name=account_name,
            subtransactions=subtransactions,
            memo=memo,
            flag_color=flag_color,
            flag_name=flag_name,
            payee_id=payee_id,
            category_id=category_id,
            transfer_account_id=transfer_account_id,
            amount_formatted=amount_formatted,
            amount_currency=amount_currency,
            payee_name=payee_name,
            category_name=category_name,
        )

        scheduled_transaction_detail.additional_properties = d
        return scheduled_transaction_detail

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
