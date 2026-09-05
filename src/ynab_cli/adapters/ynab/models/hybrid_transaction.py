from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ynab_cli.adapters.ynab.models.hybrid_transaction_type import HybridTransactionType
from ynab_cli.adapters.ynab.models.transaction_cleared_status import TransactionClearedStatus
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_1 import TransactionFlagColorType1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_2_type_1 import TransactionFlagColorType2Type1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_3_type_1 import TransactionFlagColorType3Type1
from ynab_cli.adapters.ynab.models.transaction_summary_base_debt_transaction_type_type_1 import (
    TransactionSummaryBaseDebtTransactionTypeType1,
)
from ynab_cli.adapters.ynab.models.transaction_summary_base_debt_transaction_type_type_2_type_1 import (
    TransactionSummaryBaseDebtTransactionTypeType2Type1,
)
from ynab_cli.adapters.ynab.models.transaction_summary_base_debt_transaction_type_type_3_type_1 import (
    TransactionSummaryBaseDebtTransactionTypeType3Type1,
)
from ynab_cli.adapters.ynab.types import UNSET, Unset

T = TypeVar("T", bound="HybridTransaction")


@_attrs_define
class HybridTransaction:
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
        type_ (HybridTransactionType): Whether the hybrid transaction represents a regular transaction or a
            subtransaction
        account_name (str):
        memo (None | str | Unset):
        flag_color (None | TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 |
            Unset): The transaction flag
        flag_name (None | str | Unset): The customized name of a transaction flag
        payee_id (None | Unset | UUID):
        category_id (None | Unset | UUID):
        transfer_account_id (None | Unset | UUID): If a transfer transaction, the account to which it transfers
        transfer_transaction_id (None | str | Unset): If a transfer transaction, the id of transaction on the other side
            of the transfer
        matched_transaction_id (None | str | Unset): If transaction is matched, the id of the matched transaction
        import_id (None | str | Unset): If the transaction was imported, this field is a unique (by account) import
            identifier.  If this transaction was imported through File Based Import or Direct Import and not through the
            API, the import_id will have the format: 'YNAB:[milliunit_amount]:[iso_date]:[occurrence]'.  For example, a
            transaction dated 2015-12-30 in the amount of -$294.23 USD would have an import_id of
            'YNAB:-294230:2015-12-30:1'.  If a second transaction on the same account was imported and had the same date and
            same amount, its import_id would be 'YNAB:-294230:2015-12-30:2'.
        import_payee_name (None | str | Unset): If the transaction was imported, the payee name that was used when
            importing and before applying any payee rename rules
        import_payee_name_original (None | str | Unset): If the transaction was imported, the original payee name as it
            appeared on the statement
        debt_transaction_type (None | TransactionSummaryBaseDebtTransactionTypeType1 |
            TransactionSummaryBaseDebtTransactionTypeType2Type1 | TransactionSummaryBaseDebtTransactionTypeType3Type1 |
            Unset): If the transaction is a debt/loan account transaction, the type of transaction
        amount_formatted (str | Unset): The transaction amount formatted in the plan's currency format
        amount_currency (float | Unset): The transaction amount as a decimal currency amount
        parent_transaction_id (None | str | Unset): For subtransaction types, this is the id of the parent transaction.
            For transaction types, this id will be always be null.
        payee_name (None | str | Unset):
        category_name (str | Unset): The name of the category.  If a split transaction, this will be 'Split'.
    """

    id: str
    date: datetime.date
    amount: int
    cleared: TransactionClearedStatus
    approved: bool
    account_id: UUID
    deleted: bool
    type_: HybridTransactionType
    account_name: str
    memo: str | Unset | None = UNSET
    flag_color: (
        TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 | Unset | None
    ) = UNSET
    flag_name: str | Unset | None = UNSET
    payee_id: Unset | UUID | None = UNSET
    category_id: Unset | UUID | None = UNSET
    transfer_account_id: Unset | UUID | None = UNSET
    transfer_transaction_id: str | Unset | None = UNSET
    matched_transaction_id: str | Unset | None = UNSET
    import_id: str | Unset | None = UNSET
    import_payee_name: str | Unset | None = UNSET
    import_payee_name_original: str | Unset | None = UNSET
    debt_transaction_type: (
        TransactionSummaryBaseDebtTransactionTypeType1
        | TransactionSummaryBaseDebtTransactionTypeType2Type1
        | TransactionSummaryBaseDebtTransactionTypeType3Type1
        | Unset
        | None
    ) = UNSET
    amount_formatted: str | Unset = UNSET
    amount_currency: float | Unset = UNSET
    parent_transaction_id: str | Unset | None = UNSET
    payee_name: str | Unset | None = UNSET
    category_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        date = self.date.isoformat()

        amount = self.amount

        cleared = self.cleared.value

        approved = self.approved

        account_id = str(self.account_id)

        deleted = self.deleted

        type_ = self.type_.value

        account_name = self.account_name

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

        transfer_transaction_id: str | Unset | None
        if isinstance(self.transfer_transaction_id, Unset):
            transfer_transaction_id = UNSET
        else:
            transfer_transaction_id = self.transfer_transaction_id

        matched_transaction_id: str | Unset | None
        if isinstance(self.matched_transaction_id, Unset):
            matched_transaction_id = UNSET
        else:
            matched_transaction_id = self.matched_transaction_id

        import_id: str | Unset | None
        if isinstance(self.import_id, Unset):
            import_id = UNSET
        else:
            import_id = self.import_id

        import_payee_name: str | Unset | None
        if isinstance(self.import_payee_name, Unset):
            import_payee_name = UNSET
        else:
            import_payee_name = self.import_payee_name

        import_payee_name_original: str | Unset | None
        if isinstance(self.import_payee_name_original, Unset):
            import_payee_name_original = UNSET
        else:
            import_payee_name_original = self.import_payee_name_original

        debt_transaction_type: str | Unset | None
        if isinstance(self.debt_transaction_type, Unset):
            debt_transaction_type = UNSET
        elif isinstance(
            self.debt_transaction_type,
            (
                TransactionSummaryBaseDebtTransactionTypeType1,
                TransactionSummaryBaseDebtTransactionTypeType2Type1,
                TransactionSummaryBaseDebtTransactionTypeType3Type1,
            ),
        ):
            debt_transaction_type = self.debt_transaction_type.value
        else:
            debt_transaction_type = self.debt_transaction_type

        amount_formatted = self.amount_formatted

        amount_currency = self.amount_currency

        parent_transaction_id: str | Unset | None
        if isinstance(self.parent_transaction_id, Unset):
            parent_transaction_id = UNSET
        else:
            parent_transaction_id = self.parent_transaction_id

        payee_name: str | Unset | None
        if isinstance(self.payee_name, Unset):
            payee_name = UNSET
        else:
            payee_name = self.payee_name

        category_name = self.category_name

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
                "type": type_,
                "account_name": account_name,
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
        if amount_formatted is not UNSET:
            field_dict["amount_formatted"] = amount_formatted
        if amount_currency is not UNSET:
            field_dict["amount_currency"] = amount_currency
        if parent_transaction_id is not UNSET:
            field_dict["parent_transaction_id"] = parent_transaction_id
        if payee_name is not UNSET:
            field_dict["payee_name"] = payee_name
        if category_name is not UNSET:
            field_dict["category_name"] = category_name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        date = datetime.date.fromisoformat(d.pop("date"))

        amount = d.pop("amount")

        cleared = TransactionClearedStatus(d.pop("cleared"))

        approved = d.pop("approved")

        account_id = UUID(d.pop("account_id"))

        deleted = d.pop("deleted")

        type_ = HybridTransactionType(d.pop("type"))

        account_name = d.pop("account_name")

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

        def _parse_transfer_transaction_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        transfer_transaction_id = _parse_transfer_transaction_id(d.pop("transfer_transaction_id", UNSET))

        def _parse_matched_transaction_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        matched_transaction_id = _parse_matched_transaction_id(d.pop("matched_transaction_id", UNSET))

        def _parse_import_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        import_id = _parse_import_id(d.pop("import_id", UNSET))

        def _parse_import_payee_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        import_payee_name = _parse_import_payee_name(d.pop("import_payee_name", UNSET))

        def _parse_import_payee_name_original(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        import_payee_name_original = _parse_import_payee_name_original(d.pop("import_payee_name_original", UNSET))

        def _parse_debt_transaction_type(
            data: object,
        ) -> (
            TransactionSummaryBaseDebtTransactionTypeType1
            | TransactionSummaryBaseDebtTransactionTypeType2Type1
            | TransactionSummaryBaseDebtTransactionTypeType3Type1
            | Unset
            | None
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                debt_transaction_type_type_1 = TransactionSummaryBaseDebtTransactionTypeType1(data)

                return debt_transaction_type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                debt_transaction_type_type_2_type_1 = TransactionSummaryBaseDebtTransactionTypeType2Type1(data)

                return debt_transaction_type_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                debt_transaction_type_type_3_type_1 = TransactionSummaryBaseDebtTransactionTypeType3Type1(data)

                return debt_transaction_type_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                TransactionSummaryBaseDebtTransactionTypeType1
                | TransactionSummaryBaseDebtTransactionTypeType2Type1
                | TransactionSummaryBaseDebtTransactionTypeType3Type1
                | Unset
                | None,
                data,
            )

        debt_transaction_type = _parse_debt_transaction_type(d.pop("debt_transaction_type", UNSET))

        amount_formatted = d.pop("amount_formatted", UNSET)

        amount_currency = d.pop("amount_currency", UNSET)

        def _parse_parent_transaction_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        parent_transaction_id = _parse_parent_transaction_id(d.pop("parent_transaction_id", UNSET))

        def _parse_payee_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(str | Unset | None, data)

        payee_name = _parse_payee_name(d.pop("payee_name", UNSET))

        category_name = d.pop("category_name", UNSET)

        hybrid_transaction = cls(
            id=id,
            date=date,
            amount=amount,
            cleared=cleared,
            approved=approved,
            account_id=account_id,
            deleted=deleted,
            type_=type_,
            account_name=account_name,
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
            amount_formatted=amount_formatted,
            amount_currency=amount_currency,
            parent_transaction_id=parent_transaction_id,
            payee_name=payee_name,
            category_name=category_name,
        )

        hybrid_transaction.additional_properties = d
        return hybrid_transaction

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
