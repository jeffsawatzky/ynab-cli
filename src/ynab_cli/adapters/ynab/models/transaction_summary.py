import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ynab_cli.adapters.ynab.models.transaction_cleared_status import TransactionClearedStatus
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_1 import TransactionFlagColorType1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_2_type_1 import TransactionFlagColorType2Type1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_3_type_1 import TransactionFlagColorType3Type1
from ynab_cli.adapters.ynab.models.transaction_summary_debt_transaction_type_type_1 import (
    TransactionSummaryDebtTransactionTypeType1,
)
from ynab_cli.adapters.ynab.models.transaction_summary_debt_transaction_type_type_2_type_1 import (
    TransactionSummaryDebtTransactionTypeType2Type1,
)
from ynab_cli.adapters.ynab.models.transaction_summary_debt_transaction_type_type_3_type_1 import (
    TransactionSummaryDebtTransactionTypeType3Type1,
)
from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="TransactionSummary")


@_attrs_define
class TransactionSummary:
    """
    Attributes:
        id (str):
        date (datetime.date): The transaction date in ISO format (e.g. 2016-12-01)
        amount (int): The transaction amount in milliunits format
        cleared (TransactionClearedStatus): The cleared status of the transaction
        approved (bool): Whether or not the transaction is approved
        account_id (UUID):
        deleted (bool): Whether or not the transaction has been deleted.  Deleted transactions will only be included in
            delta requests.
        memo (Union[None, Unset, str]):
        flag_color (Union[None, TransactionFlagColorType1, TransactionFlagColorType2Type1,
            TransactionFlagColorType3Type1, Unset]): The transaction flag
        flag_name (Union[None, Unset, str]): The customized name of a transaction flag
        payee_id (Union[None, UUID, Unset]):
        category_id (Union[None, UUID, Unset]):
        transfer_account_id (Union[None, UUID, Unset]): If a transfer transaction, the account to which it transfers
        transfer_transaction_id (Union[None, Unset, str]): If a transfer transaction, the id of transaction on the other
            side of the transfer
        matched_transaction_id (Union[None, Unset, str]): If transaction is matched, the id of the matched transaction
        import_id (Union[None, Unset, str]): If the transaction was imported, this field is a unique (by account) import
            identifier.  If this transaction was imported through File Based Import or Direct Import and not through the
            API, the import_id will have the format: 'YNAB:[milliunit_amount]:[iso_date]:[occurrence]'.  For example, a
            transaction dated 2015-12-30 in the amount of -$294.23 USD would have an import_id of
            'YNAB:-294230:2015-12-30:1'.  If a second transaction on the same account was imported and had the same date and
            same amount, its import_id would be 'YNAB:-294230:2015-12-30:2'.
        import_payee_name (Union[None, Unset, str]): If the transaction was imported, the payee name that was used when
            importing and before applying any payee rename rules
        import_payee_name_original (Union[None, Unset, str]): If the transaction was imported, the original payee name
            as it appeared on the statement
        debt_transaction_type (Union[None, TransactionSummaryDebtTransactionTypeType1,
            TransactionSummaryDebtTransactionTypeType2Type1, TransactionSummaryDebtTransactionTypeType3Type1, Unset]): If
            the transaction is a debt/loan account transaction, the type of transaction
    """

    id: str
    date: datetime.date
    amount: int
    cleared: TransactionClearedStatus
    approved: bool
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
    transfer_transaction_id: None | Unset | str = UNSET
    matched_transaction_id: None | Unset | str = UNSET
    import_id: None | Unset | str = UNSET
    import_payee_name: None | Unset | str = UNSET
    import_payee_name_original: None | Unset | str = UNSET
    debt_transaction_type: (
        None
        | TransactionSummaryDebtTransactionTypeType1
        | TransactionSummaryDebtTransactionTypeType2Type1
        | TransactionSummaryDebtTransactionTypeType3Type1
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        date = self.date.isoformat()

        amount = self.amount

        cleared = self.cleared.value

        approved = self.approved

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

        transfer_transaction_id: None | Unset | str
        if isinstance(self.transfer_transaction_id, Unset):
            transfer_transaction_id = UNSET
        else:
            transfer_transaction_id = self.transfer_transaction_id

        matched_transaction_id: None | Unset | str
        if isinstance(self.matched_transaction_id, Unset):
            matched_transaction_id = UNSET
        else:
            matched_transaction_id = self.matched_transaction_id

        import_id: None | Unset | str
        if isinstance(self.import_id, Unset):
            import_id = UNSET
        else:
            import_id = self.import_id

        import_payee_name: None | Unset | str
        if isinstance(self.import_payee_name, Unset):
            import_payee_name = UNSET
        else:
            import_payee_name = self.import_payee_name

        import_payee_name_original: None | Unset | str
        if isinstance(self.import_payee_name_original, Unset):
            import_payee_name_original = UNSET
        else:
            import_payee_name_original = self.import_payee_name_original

        debt_transaction_type: None | Unset | str
        if isinstance(self.debt_transaction_type, Unset):
            debt_transaction_type = UNSET
        elif isinstance(self.debt_transaction_type, TransactionSummaryDebtTransactionTypeType1):
            debt_transaction_type = self.debt_transaction_type.value
        elif isinstance(self.debt_transaction_type, TransactionSummaryDebtTransactionTypeType2Type1):
            debt_transaction_type = self.debt_transaction_type.value
        elif isinstance(self.debt_transaction_type, TransactionSummaryDebtTransactionTypeType3Type1):
            debt_transaction_type = self.debt_transaction_type.value
        else:
            debt_transaction_type = self.debt_transaction_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "date": date,
                "amount": amount,
                "cleared": cleared,
                "approved": approved,
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
        if transfer_transaction_id is not UNSET:
            field_dict["transfer_transaction_id"] = transfer_transaction_id
        if matched_transaction_id is not UNSET:
            field_dict["matched_transaction_id"] = matched_transaction_id
        if import_id is not UNSET:
            field_dict["import_id"] = import_id
        if import_payee_name is not UNSET:
            field_dict["import_payee_name"] = import_payee_name
        if import_payee_name_original is not UNSET:
            field_dict["import_payee_name_original"] = import_payee_name_original
        if debt_transaction_type is not UNSET:
            field_dict["debt_transaction_type"] = debt_transaction_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        date = isoparse(d.pop("date")).date()

        amount = d.pop("amount")

        cleared = TransactionClearedStatus(d.pop("cleared"))

        approved = d.pop("approved")

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

        def _parse_transfer_transaction_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        transfer_transaction_id = _parse_transfer_transaction_id(d.pop("transfer_transaction_id", UNSET))

        def _parse_matched_transaction_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        matched_transaction_id = _parse_matched_transaction_id(d.pop("matched_transaction_id", UNSET))

        def _parse_import_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        import_id = _parse_import_id(d.pop("import_id", UNSET))

        def _parse_import_payee_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        import_payee_name = _parse_import_payee_name(d.pop("import_payee_name", UNSET))

        def _parse_import_payee_name_original(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        import_payee_name_original = _parse_import_payee_name_original(d.pop("import_payee_name_original", UNSET))

        def _parse_debt_transaction_type(
            data: object,
        ) -> (
            None
            | TransactionSummaryDebtTransactionTypeType1
            | TransactionSummaryDebtTransactionTypeType2Type1
            | TransactionSummaryDebtTransactionTypeType3Type1
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                debt_transaction_type_type_1 = TransactionSummaryDebtTransactionTypeType1(data)

                return debt_transaction_type_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                debt_transaction_type_type_2_type_1 = TransactionSummaryDebtTransactionTypeType2Type1(data)

                return debt_transaction_type_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                debt_transaction_type_type_3_type_1 = TransactionSummaryDebtTransactionTypeType3Type1(data)

                return debt_transaction_type_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                None
                | TransactionSummaryDebtTransactionTypeType1
                | TransactionSummaryDebtTransactionTypeType2Type1
                | TransactionSummaryDebtTransactionTypeType3Type1
                | Unset,
                data,
            )

        debt_transaction_type = _parse_debt_transaction_type(d.pop("debt_transaction_type", UNSET))

        transaction_summary = cls(
            id=id,
            date=date,
            amount=amount,
            cleared=cleared,
            approved=approved,
            account_id=account_id,
            deleted=deleted,
            memo=memo,
            flag_color=flag_color,
            flag_name=flag_name,
            payee_id=payee_id,
            category_id=category_id,
            transfer_account_id=transfer_account_id,
            transfer_transaction_id=transfer_transaction_id,
            matched_transaction_id=matched_transaction_id,
            import_id=import_id,
            import_payee_name=import_payee_name,
            import_payee_name_original=import_payee_name_original,
            debt_transaction_type=debt_transaction_type,
        )

        transaction_summary.additional_properties = d
        return transaction_summary

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
