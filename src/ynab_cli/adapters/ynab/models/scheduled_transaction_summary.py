import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ynab_cli.adapters.ynab.models.scheduled_transaction_summary_frequency import ScheduledTransactionSummaryFrequency
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_1 import TransactionFlagColorType1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_2_type_1 import TransactionFlagColorType2Type1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_3_type_1 import TransactionFlagColorType3Type1
from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="ScheduledTransactionSummary")


@_attrs_define
class ScheduledTransactionSummary:
    """
    Attributes:
        id (UUID):
        date_first (datetime.date): The first date for which the Scheduled Transaction was scheduled.
        date_next (datetime.date): The next date for which the Scheduled Transaction is scheduled.
        frequency (ScheduledTransactionSummaryFrequency):
        amount (int): The scheduled transaction amount in milliunits format
        account_id (UUID):
        deleted (bool): Whether or not the scheduled transaction has been deleted.  Deleted scheduled transactions will
            only be included in delta requests.
        memo (Union[None, Unset, str]):
        flag_color (Union[None, TransactionFlagColorType1, TransactionFlagColorType2Type1,
            TransactionFlagColorType3Type1, Unset]): The transaction flag
        flag_name (Union[None, Unset, str]): The customized name of a transaction flag
        payee_id (Union[None, UUID, Unset]):
        category_id (Union[None, UUID, Unset]):
        transfer_account_id (Union[None, UUID, Unset]): If a transfer, the account_id which the scheduled transaction
            transfers to
    """

    id: UUID
    date_first: datetime.date
    date_next: datetime.date
    frequency: ScheduledTransactionSummaryFrequency
    amount: int
    account_id: UUID
    deleted: bool
    memo: None | Unset | str = UNSET
    flag_color: (
        None | TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 | Unset
    ) = UNSET
    flag_name: None | Unset | str = UNSET
    payee_id: None | UUID | Unset = UNSET
    category_id: None | UUID | Unset = UNSET
    transfer_account_id: None | UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        date_first = self.date_first.isoformat()

        date_next = self.date_next.isoformat()

        frequency = self.frequency.value

        amount = self.amount

        account_id = str(self.account_id)

        deleted = self.deleted

        memo: None | Unset | str
        if isinstance(self.memo, Unset):
            memo = UNSET
        else:
            memo = self.memo

        flag_color: None | Unset | str
        if isinstance(self.flag_color, Unset):
            flag_color = UNSET
        elif isinstance(self.flag_color, TransactionFlagColorType1):
            flag_color = self.flag_color.value
        elif isinstance(self.flag_color, TransactionFlagColorType2Type1):
            flag_color = self.flag_color.value
        elif isinstance(self.flag_color, TransactionFlagColorType3Type1):
            flag_color = self.flag_color.value
        else:
            flag_color = self.flag_color

        flag_name: None | Unset | str
        if isinstance(self.flag_name, Unset):
            flag_name = UNSET
        else:
            flag_name = self.flag_name

        payee_id: None | Unset | str
        if isinstance(self.payee_id, Unset):
            payee_id = UNSET
        elif isinstance(self.payee_id, UUID):
            payee_id = str(self.payee_id)
        else:
            payee_id = self.payee_id

        category_id: None | Unset | str
        if isinstance(self.category_id, Unset):
            category_id = UNSET
        elif isinstance(self.category_id, UUID):
            category_id = str(self.category_id)
        else:
            category_id = self.category_id

        transfer_account_id: None | Unset | str
        if isinstance(self.transfer_account_id, Unset):
            transfer_account_id = UNSET
        elif isinstance(self.transfer_account_id, UUID):
            transfer_account_id = str(self.transfer_account_id)
        else:
            transfer_account_id = self.transfer_account_id

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        date_first = isoparse(d.pop("date_first")).date()

        date_next = isoparse(d.pop("date_next")).date()

        frequency = ScheduledTransactionSummaryFrequency(d.pop("frequency"))

        amount = d.pop("amount")

        account_id = UUID(d.pop("account_id"))

        deleted = d.pop("deleted")

        def _parse_memo(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        memo = _parse_memo(d.pop("memo", UNSET))

        def _parse_flag_color(
            data: object,
        ) -> None | TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_transaction_flag_color_type_1 = TransactionFlagColorType1(data)

                return componentsschemas_transaction_flag_color_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_transaction_flag_color_type_2_type_1 = TransactionFlagColorType2Type1(data)

                return componentsschemas_transaction_flag_color_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_transaction_flag_color_type_3_type_1 = TransactionFlagColorType3Type1(data)

                return componentsschemas_transaction_flag_color_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                None
                | TransactionFlagColorType1
                | TransactionFlagColorType2Type1
                | TransactionFlagColorType3Type1
                | Unset,
                data,
            )

        flag_color = _parse_flag_color(d.pop("flag_color", UNSET))

        def _parse_flag_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        flag_name = _parse_flag_name(d.pop("flag_name", UNSET))

        def _parse_payee_id(data: object) -> None | UUID | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                payee_id_type_0 = UUID(data)

                return payee_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID | Unset, data)

        payee_id = _parse_payee_id(d.pop("payee_id", UNSET))

        def _parse_category_id(data: object) -> None | UUID | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_id_type_0 = UUID(data)

                return category_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID | Unset, data)

        category_id = _parse_category_id(d.pop("category_id", UNSET))

        def _parse_transfer_account_id(data: object) -> None | UUID | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                transfer_account_id_type_0 = UUID(data)

                return transfer_account_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID | Unset, data)

        transfer_account_id = _parse_transfer_account_id(d.pop("transfer_account_id", UNSET))

        scheduled_transaction_summary = cls(
            id=id,
            date_first=date_first,
            date_next=date_next,
            frequency=frequency,
            amount=amount,
            account_id=account_id,
            deleted=deleted,
            memo=memo,
            flag_color=flag_color,
            flag_name=flag_name,
            payee_id=payee_id,
            category_id=category_id,
            transfer_account_id=transfer_account_id,
        )

        scheduled_transaction_summary.additional_properties = d
        return scheduled_transaction_summary

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
