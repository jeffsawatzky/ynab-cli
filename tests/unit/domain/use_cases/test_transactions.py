from ynab_cli.adapters.ynab import models
from ynab_cli.domain.models import rules
from ynab_cli.domain.use_cases import transactions as use_cases


def test_should_skip_transaction(transaction_detail: models.TransactionDetail) -> None:
    transaction_detail.deleted = False
    assert use_cases.should_skip_transaction(transaction=transaction_detail) is False
    transaction_detail.deleted = True
    assert use_cases.should_skip_transaction(transaction=transaction_detail) is True


def test_get_save_transaction__no_rule_match(transaction_detail: models.TransactionDetail) -> None:
    transaction_rules = rules.TransactionRules.model_validate(
        {
            "transaction_rules": [
                {
                    "rules": ["payee_name == 'Insurance'"],
                    "patch": {
                        "category_id": "category",
                    },
                },
            ]
        }
    )

    transaction_detail.payee_name = "Not Insurance"
    transaction_detail.category_id = None
    result = use_cases.get_save_transaction(transaction_detail=transaction_detail, transaction_rules=transaction_rules)
    assert result is None


def test_get_save_transaction__match_payee_name(transaction_detail: models.TransactionDetail) -> None:
    transaction_rules = rules.TransactionRules.model_validate(
        {
            "transaction_rules": [
                {
                    "rules": ["payee_name == 'Insurance'"],
                    "patch": {
                        "category_id": "category",
                    },
                },
            ]
        }
    )

    transaction_detail.payee_name = "Insurance"
    transaction_detail.category_id = None
    result = use_cases.get_save_transaction(transaction_detail=transaction_detail, transaction_rules=transaction_rules)
    assert result == models.SaveTransactionWithIdOrImportId(
        id=transaction_detail.id,
        import_id=transaction_detail.import_id,
        category_id="category",
    )
    assert result.to_dict() == {
        "id": transaction_detail.id,
        "import_id": transaction_detail.import_id,
        "category_id": "category",
    }


def test_get_save_transaction__set_split(transaction_detail: models.TransactionDetail) -> None:
    transaction_rules = rules.TransactionRules.model_validate(
        {
            "transaction_rules": [
                {
                    "rules": ["payee_name == 'Insurance'"],
                    "patch": {
                        "category_id": None,
                        "subtransactions": [
                            {
                                "category_id": "category_id_1",
                                "amount": transaction_detail.amount,
                            },
                            {
                                "category_id": "category_id_2",
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
    result = use_cases.get_save_transaction(transaction_detail=transaction_detail, transaction_rules=transaction_rules)
    assert result == models.SaveTransactionWithIdOrImportId(
        id=transaction_detail.id,
        import_id=transaction_detail.import_id,
        category_id=None,
        subtransactions=[
            models.SaveSubTransaction(
                category_id="category_id_1",
                amount=transaction_detail.amount,
            ),
            models.SaveSubTransaction(
                category_id="category_id_2",
                amount=transaction_detail.amount,
            ),
        ],
    )
