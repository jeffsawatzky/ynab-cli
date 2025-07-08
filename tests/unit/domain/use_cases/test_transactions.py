from http import HTTPStatus
from typing import cast
from unittest.mock import AsyncMock, MagicMock

import pytest
from pytest_mock import MockerFixture

from tests.factories import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.types import Response
from ynab_cli.domain.models import rules
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import transactions as use_cases


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


@pytest.mark.anyio
async def test_apply_rules(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_transactions = mocker.patch("ynab_cli.domain.use_cases.transactions.get_transactions")
    mock_get_transactions.asyncio_detailed = AsyncMock()
    mock_get_transactions.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.TransactionsResponse(
            data=models.TransactionsResponseData(
                transactions=[
                    ynab.TransactionDetailFactory.build(payee_name="Insurance", category_id=None, deleted=False),
                    ynab.TransactionDetailFactory.build(deleted=True),
                ],
                server_knowledge=0,
            ),
        ),
    )

    settings = Settings()
    params: use_cases.ApplyRulesParams = {
        "transaction_rules": rules.TransactionRules.from_dict(
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
    }

    results: list[tuple[models.TransactionDetail, models.SaveTransactionWithIdOrImportId]] = []
    async for result in use_cases.ApplyRules(mock_io, MagicMock())(settings, params):
        transaction_detail, save_transaction = result
        assert isinstance(transaction_detail, models.TransactionDetail)
        assert isinstance(save_transaction, models.SaveTransactionWithIdOrImportId)
        results.append(result)

    assert len(results) == 1


@pytest.mark.parametrize(
    ("exception", "expected_print"),
    [
        (util.ApiError(401), "Invalid or expired access token. Please update your settings."),
        (util.ApiError(429), "API rate limit exceeded. Try again later, or get a new access token."),
        (Exception("Unexpected error"), "Exception when calling YNAB: Unexpected error"),
    ],
)
@pytest.mark.anyio
async def test_apply_rules_exception(
    exception: Exception, expected_print: str, mocker: MockerFixture, mock_io: MagicMock
) -> None:
    mock_get_transactions = mocker.patch("ynab_cli.domain.use_cases.transactions.get_transactions")
    mock_get_transactions.asyncio_detailed = AsyncMock()
    mock_get_transactions.asyncio_detailed.side_effect = exception

    settings = Settings()
    params: use_cases.ApplyRulesParams = {
        "transaction_rules": rules.TransactionRules.from_dict({"transaction_rules": []})
    }

    async for _ in use_cases.ApplyRules(mock_io, MagicMock())(settings, params):
        pass

    mock_io.print.assert_called_with(expected_print)
