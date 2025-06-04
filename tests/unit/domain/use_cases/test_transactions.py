from typing import cast
from uuid import UUID

import pytest

from tests.factories import ynab
from ynab_cli.adapters.ynab import models
from ynab_cli.domain.models import rules
from ynab_cli.domain.use_cases import transactions as use_cases

uuid = UUID("00000000-0000-0000-0000-000000000000")


@pytest.fixture
def transaction_detail() -> models.TransactionDetail:
    return cast(models.TransactionDetail, ynab.TransactionDetailFactory.build())


def test_should_skip_transaction(transaction_detail: models.TransactionDetail) -> None:
    transaction_detail.deleted = False
    assert use_cases._should_skip_transaction(transaction=transaction_detail) is False
    transaction_detail.deleted = True
    assert use_cases._should_skip_transaction(transaction=transaction_detail) is True


def test_get_save_transaction__no_rule_match(transaction_detail: models.TransactionDetail) -> None:
    transaction_rules = rules.TransactionRules.from_dict(
        {
            "transaction_rules": [
                {
                    "rules": ["payee_name == 'Insurance'"],
                    "patch": {
                        "category_id": "00000000-0000-0000-0000-000000000000",
                    },
                },
            ]
        }
    )

    transaction_detail.payee_name = "Not Insurance"
    transaction_detail.category_id = None
    result = use_cases._get_save_transaction(transaction_detail=transaction_detail, transaction_rules=transaction_rules)
    assert result is None


def test_get_save_transaction__match_payee_name(transaction_detail: models.TransactionDetail) -> None:
    transaction_rules = rules.TransactionRules.from_dict(
        {
            "transaction_rules": [
                {
                    "rules": ["payee_name == 'Insurance'"],
                    "patch": {
                        "category_id": "00000000-0000-0000-0000-000000000000",
                    },
                },
            ]
        }
    )

    transaction_detail.payee_name = "Insurance"
    transaction_detail.category_id = None
    result = use_cases._get_save_transaction(transaction_detail=transaction_detail, transaction_rules=transaction_rules)
    assert result is not None
    assert result.to_dict() == {
        "id": transaction_detail.id,
        "category_id": "00000000-0000-0000-0000-000000000000",
        "subtransactions": [],
    }


def test_get_save_transaction__set_split(transaction_detail: models.TransactionDetail) -> None:
    transaction_rules = rules.TransactionRules.from_dict(
        {
            "transaction_rules": [
                {
                    "rules": ["payee_name == 'Insurance'"],
                    "patch": {
                        "category_id": None,
                        "subtransactions": [
                            {
                                "category_id": "00000000-0000-0000-0000-000000000000",
                                "amount": transaction_detail.amount,
                            },
                            {
                                "category_id": "00000000-0000-0000-0000-000000000000",
                                "amount": transaction_detail.amount,
                            },
                        ],
                    },
                },
            ]
        }
    )

    transaction_detail.payee_name = "Insurance"
    transaction_detail.category_id = None
    result = use_cases._get_save_transaction(transaction_detail=transaction_detail, transaction_rules=transaction_rules)
    assert result is not None
    assert result.to_dict() == {
        "id": transaction_detail.id,
        "category_id": None,
        "subtransactions": [
            {"amount": transaction_detail.amount, "category_id": "00000000-0000-0000-0000-000000000000"},
            {"amount": transaction_detail.amount, "category_id": "00000000-0000-0000-0000-000000000000"},
        ],
    }
