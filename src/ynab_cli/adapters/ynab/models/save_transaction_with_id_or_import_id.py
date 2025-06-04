import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ynab_cli.adapters.ynab.models.transaction_cleared_status import TransactionClearedStatus
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_1 import TransactionFlagColorType1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_2_type_1 import TransactionFlagColorType2Type1
from ynab_cli.adapters.ynab.models.transaction_flag_color_type_3_type_1 import TransactionFlagColorType3Type1
from ynab_cli.adapters.ynab.types import UNSET, Unset

if TYPE_CHECKING:
    from ynab_cli.adapters.ynab.models.save_sub_transaction import SaveSubTransaction


T = TypeVar("T", bound="SaveTransactionWithIdOrImportId")


@_attrs_define
class SaveTransactionWithIdOrImportId:
    """
    Attributes:
        account_id (Union[Unset, UUID]):
        date (Union[Unset, datetime.date]): The transaction date in ISO format (e.g. 2016-12-01).  Future dates
            (scheduled transactions) are not permitted.  Split transaction dates cannot be changed and if a different date
            is supplied it will be ignored.
        amount (Union[Unset, int]): The transaction amount in milliunits format.  Split transaction amounts cannot be
            changed and if a different amount is supplied it will be ignored.
        payee_id (Union[None, UUID, Unset]): The payee for the transaction.  To create a transfer between two accounts,
            use the account transfer payee pointing to the target account.  Account transfer payees are specified as
            `transfer_payee_id` on the account resource.
        payee_name (Union[None, Unset, str]): The payee name.  If a `payee_name` value is provided and `payee_id` has a
            null value, the `payee_name` value will be used to resolve the payee by either (1) a matching payee rename rule
            (only if `import_id` is also specified) or (2) a payee with the same name or (3) creation of a new payee.
        category_id (Union[None, UUID, Unset]): The category for the transaction.  To configure a split transaction, you
            can specify null for `category_id` and provide a `subtransactions` array as part of the transaction object.  If
            an existing transaction is a split, the `category_id` cannot be changed.  Credit Card Payment categories are not
            permitted and will be ignored if supplied.
        memo (Union[None, Unset, str]):
        cleared (Union[Unset, TransactionClearedStatus]): The cleared status of the transaction
        approved (Union[Unset, bool]): Whether or not the transaction is approved.  If not supplied, transaction will be
            unapproved by default.
        flag_color (Union[None, TransactionFlagColorType1, TransactionFlagColorType2Type1,
            TransactionFlagColorType3Type1, Unset]): The transaction flag
        subtransactions (Union[Unset, list['SaveSubTransaction']]): An array of subtransactions to configure a
            transaction as a split. Updating `subtransactions` on an existing split transaction is not supported.
        id (Union[None, Unset, str]): If specified, this id will be used to lookup a transaction by its `id` for the
            purpose of updating the transaction itself. If not specified, an `import_id` should be supplied.
        import_id (Union[None, Unset, str]): If specified, this id will be used to lookup a transaction by its
            `import_id` for the purpose of updating the transaction itself. If not specified, an `id` should be supplied.
            You may not provide both an `id` and an `import_id` and updating an `import_id` on an existing transaction is
            not allowed.
    """

    account_id: Unset | UUID = UNSET
    date: Unset | datetime.date = UNSET
    amount: Unset | int = UNSET
    payee_id: None | UUID | Unset = UNSET
    payee_name: None | Unset | str = UNSET
    category_id: None | UUID | Unset = UNSET
    memo: None | Unset | str = UNSET
    cleared: Unset | TransactionClearedStatus = UNSET
    approved: Unset | bool = UNSET
    flag_color: (
        None | TransactionFlagColorType1 | TransactionFlagColorType2Type1 | TransactionFlagColorType3Type1 | Unset
    ) = UNSET
    subtransactions: Unset | list["SaveSubTransaction"] = UNSET
    id: None | Unset | str = UNSET
    import_id: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id: Unset | str = UNSET
        if not isinstance(self.account_id, Unset):
            account_id = str(self.account_id)

        date: Unset | str = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        amount = self.amount

        payee_id: None | Unset | str
        if isinstance(self.payee_id, Unset):
            payee_id = UNSET
        elif isinstance(self.payee_id, UUID):
            payee_id = str(self.payee_id)
        else:
            payee_id = self.payee_id

        payee_name: None | Unset | str
        if isinstance(self.payee_name, Unset):
            payee_name = UNSET
        else:
            payee_name = self.payee_name

        category_id: None | Unset | str
        if isinstance(self.category_id, Unset):
            category_id = UNSET
        elif isinstance(self.category_id, UUID):
            category_id = str(self.category_id)
        else:
            category_id = self.category_id

        memo: None | Unset | str
        if isinstance(self.memo, Unset):
            memo = UNSET
        else:
            memo = self.memo

        cleared: Unset | str = UNSET
        if not isinstance(self.cleared, Unset):
            cleared = self.cleared.value

        approved = self.approved

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

        subtransactions: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.subtransactions, Unset):
            subtransactions = []
            for subtransactions_item_data in self.subtransactions:
                subtransactions_item = subtransactions_item_data.to_dict()
                subtransactions.append(subtransactions_item)

        id: None | Unset | str
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        import_id: None | Unset | str
        if isinstance(self.import_id, Unset):
            import_id = UNSET
        else:
            import_id = self.import_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_id is not UNSET:
            field_dict["account_id"] = account_id
        if date is not UNSET:
            field_dict["date"] = date
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
        if cleared is not UNSET:
            field_dict["cleared"] = cleared
        if approved is not UNSET:
            field_dict["approved"] = approved
        if flag_color is not UNSET:
            field_dict["flag_color"] = flag_color
        if subtransactions is not UNSET:
            field_dict["subtransactions"] = subtransactions
        if id is not UNSET:
            field_dict["id"] = id
        if import_id is not UNSET:
            field_dict["import_id"] = import_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ynab_cli.adapters.ynab.models.save_sub_transaction import SaveSubTransaction

        d = dict(src_dict)
        _account_id = d.pop("account_id", UNSET)
        account_id: Unset | UUID
        if isinstance(_account_id, Unset):
            account_id = UNSET
        else:
            account_id = UUID(_account_id)

        _date = d.pop("date", UNSET)
        date: Unset | datetime.date
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        amount = d.pop("amount", UNSET)

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

        def _parse_payee_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        payee_name = _parse_payee_name(d.pop("payee_name", UNSET))

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

        def _parse_memo(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        memo = _parse_memo(d.pop("memo", UNSET))

        _cleared = d.pop("cleared", UNSET)
        cleared: Unset | TransactionClearedStatus
        if isinstance(_cleared, Unset):
            cleared = UNSET
        else:
            cleared = TransactionClearedStatus(_cleared)

        approved = d.pop("approved", UNSET)

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

        subtransactions = []
        _subtransactions = d.pop("subtransactions", UNSET)
        for subtransactions_item_data in _subtransactions or []:
            subtransactions_item = SaveSubTransaction.from_dict(subtransactions_item_data)

            subtransactions.append(subtransactions_item)

        def _parse_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_import_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        import_id = _parse_import_id(d.pop("import_id", UNSET))

        save_transaction_with_id_or_import_id = cls(
            account_id=account_id,
            date=date,
            amount=amount,
            payee_id=payee_id,
            payee_name=payee_name,
            category_id=category_id,
            memo=memo,
            cleared=cleared,
            approved=approved,
            flag_color=flag_color,
            subtransactions=subtransactions,
            id=id,
            import_id=import_id,
        )

        save_transaction_with_id_or_import_id.additional_properties = d
        return save_transaction_with_id_or_import_id

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
