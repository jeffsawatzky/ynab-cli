"""
YNAB API Endpoints

Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.ynab.com

The version of the OpenAPI document: 1.72.1
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from datetime import date
from typing import Annotated, Any, ClassVar, Self

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr

from ynab_cli.adapters.ynab.models.save_sub_transaction import SaveSubTransaction
from ynab_cli.adapters.ynab.models.transaction_cleared_status import TransactionClearedStatus
from ynab_cli.adapters.ynab.models.transaction_flag_color import TransactionFlagColor


class ExistingTransaction(BaseModel):
    """
    ExistingTransaction
    """

    account_id: StrictStr | None = None
    var_date: date | None = Field(
        default=None,
        description="The transaction date in ISO format (e.g. 2016-12-01).  Future dates (scheduled transactions) are not permitted.  Split transaction dates cannot be changed and if a different date is supplied it will be ignored.",
        alias="date",
    )
    amount: StrictInt | None = Field(
        default=None,
        description="The transaction amount in milliunits format.  Split transaction amounts cannot be changed and if a different amount is supplied it will be ignored.",
    )
    payee_id: StrictStr | None = Field(
        default=None,
        description="The payee for the transaction.  To create a transfer between two accounts, use the account transfer payee pointing to the target account.  Account transfer payees are specified as `transfer_payee_id` on the account resource.",
    )
    payee_name: Annotated[str, Field(strict=True, max_length=200)] | None = Field(
        default=None,
        description="The payee name.  If a `payee_name` value is provided and `payee_id` has a null value, the `payee_name` value will be used to resolve the payee by either (1) a matching payee rename rule (only if `import_id` is also specified) or (2) a payee with the same name or (3) creation of a new payee.",
    )
    category_id: StrictStr | None = Field(
        default=None,
        description="The category for the transaction.  To configure a split transaction, you can specify null for `category_id` and provide a `subtransactions` array as part of the transaction object.  If an existing transaction is a split, the `category_id` cannot be changed.  Credit Card Payment categories are not permitted and will be ignored if supplied.",
    )
    memo: Annotated[str, Field(strict=True, max_length=500)] | None = None
    cleared: TransactionClearedStatus | None = None
    approved: StrictBool | None = Field(
        default=None,
        description="Whether or not the transaction is approved.  If not supplied, transaction will be unapproved by default.",
    )
    flag_color: TransactionFlagColor | None = None
    subtransactions: list[SaveSubTransaction] | None = Field(
        default=None,
        description="An array of subtransactions to configure a transaction as a split. Updating `subtransactions` on an existing split transaction is not supported.",
    )
    __properties: ClassVar[list[str]] = [
        "account_id",
        "date",
        "amount",
        "payee_id",
        "payee_name",
        "category_id",
        "memo",
        "cleared",
        "approved",
        "flag_color",
        "subtransactions",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self | None:
        """Create an instance of ExistingTransaction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in subtransactions (list)
        _items = []
        if self.subtransactions:
            for _item_subtransactions in self.subtransactions:
                if _item_subtransactions:
                    _items.append(_item_subtransactions.to_dict())
            _dict["subtransactions"] = _items
        # set to None if payee_id (nullable) is None
        # and model_fields_set contains the field
        if self.payee_id is None and "payee_id" in self.model_fields_set:
            _dict["payee_id"] = None

        # set to None if payee_name (nullable) is None
        # and model_fields_set contains the field
        if self.payee_name is None and "payee_name" in self.model_fields_set:
            _dict["payee_name"] = None

        # set to None if category_id (nullable) is None
        # and model_fields_set contains the field
        if self.category_id is None and "category_id" in self.model_fields_set:
            _dict["category_id"] = None

        # set to None if memo (nullable) is None
        # and model_fields_set contains the field
        if self.memo is None and "memo" in self.model_fields_set:
            _dict["memo"] = None

        # set to None if flag_color (nullable) is None
        # and model_fields_set contains the field
        if self.flag_color is None and "flag_color" in self.model_fields_set:
            _dict["flag_color"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict[str, Any] | None) -> Self | None:
        """Create an instance of ExistingTransaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "account_id": obj.get("account_id"),
                "date": obj.get("date"),
                "amount": obj.get("amount"),
                "payee_id": obj.get("payee_id"),
                "payee_name": obj.get("payee_name"),
                "category_id": obj.get("category_id"),
                "memo": obj.get("memo"),
                "cleared": obj.get("cleared"),
                "approved": obj.get("approved"),
                "flag_color": obj.get("flag_color"),
                "subtransactions": [SaveSubTransaction.from_dict(_item) for _item in obj["subtransactions"]]
                if obj.get("subtransactions") is not None
                else None,
            }
        )
        return _obj
