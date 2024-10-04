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
from typing import Any, ClassVar, Self

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr


class MonthSummary(BaseModel):
    """
    MonthSummary
    """

    month: date
    note: StrictStr | None = None
    income: StrictInt = Field(
        description="The total amount of transactions categorized to 'Inflow: Ready to Assign' in the month"
    )
    budgeted: StrictInt = Field(description="The total amount budgeted in the month")
    activity: StrictInt = Field(
        description="The total amount of transactions in the month, excluding those categorized to 'Inflow: Ready to Assign'"
    )
    to_be_budgeted: StrictInt = Field(description="The available amount for 'Ready to Assign'")
    age_of_money: StrictInt | None = Field(default=None, description="The Age of Money as of the month")
    deleted: StrictBool = Field(
        description="Whether or not the month has been deleted.  Deleted months will only be included in delta requests."
    )
    __properties: ClassVar[list[str]] = [
        "month",
        "note",
        "income",
        "budgeted",
        "activity",
        "to_be_budgeted",
        "age_of_money",
        "deleted",
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
        """Create an instance of MonthSummary from a JSON string"""
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
        # set to None if note (nullable) is None
        # and model_fields_set contains the field
        if self.note is None and "note" in self.model_fields_set:
            _dict["note"] = None

        # set to None if age_of_money (nullable) is None
        # and model_fields_set contains the field
        if self.age_of_money is None and "age_of_money" in self.model_fields_set:
            _dict["age_of_money"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict[str, Any] | None) -> Self | None:
        """Create an instance of MonthSummary from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "month": obj.get("month"),
                "note": obj.get("note"),
                "income": obj.get("income"),
                "budgeted": obj.get("budgeted"),
                "activity": obj.get("activity"),
                "to_be_budgeted": obj.get("to_be_budgeted"),
                "age_of_money": obj.get("age_of_money"),
                "deleted": obj.get("deleted"),
            }
        )
        return _obj
