from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from ynab_cli.adapters.ynab import models
from ynab_cli.domain.models.rules import TransactionRule, TransactionRules


class TestTransactionRule:
    @pytest.fixture
    def mock_save_transaction(self) -> MagicMock:
        mock = MagicMock(spec=models.SaveTransactionWithIdOrImportId)
        mock.to_dict.return_value = {"account_id": "test-account", "amount": 1000}
        return mock

    @pytest.fixture
    def transaction_rule_with_patch(self, mock_save_transaction: MagicMock) -> TransactionRule:
        return TransactionRule(rules=["amount > 100", "payee_name == 'Test Payee'"], patch=mock_save_transaction)

    @pytest.fixture
    def transaction_rule_without_patch(self) -> TransactionRule:
        return TransactionRule(rules=["amount < 0", "cleared == 'uncleared'"], patch=None)

    def test_init_with_patch(self, mock_save_transaction: MagicMock) -> None:
        rule = TransactionRule(rules=["amount > 100"], patch=mock_save_transaction)

        assert rule.rules == ["amount > 100"]
        assert rule.patch == mock_save_transaction

    def test_init_without_patch(self) -> None:
        rule = TransactionRule(rules=["amount > 100"], patch=None)

        assert rule.rules == ["amount > 100"]
        assert rule.patch is None

    def test_init_with_empty_rules(self) -> None:
        rule = TransactionRule(rules=[], patch=None)

        assert rule.rules == []
        assert rule.patch is None

    def test_init_with_multiple_rules(self) -> None:
        rules = ["amount > 100", "payee_name == 'Test'", "cleared == 'cleared'"]
        rule = TransactionRule(rules=rules, patch=None)

        assert rule.rules == rules
        assert len(rule.rules) == 3

    def test_to_dict_with_patch(self, transaction_rule_with_patch: TransactionRule) -> None:
        result = transaction_rule_with_patch.to_dict()

        assert isinstance(result, dict)
        assert result["rules"] == ["amount > 100", "payee_name == 'Test Payee'"]
        assert result["patch"] == {"account_id": "test-account", "amount": 1000}

    def test_to_dict_without_patch(self, transaction_rule_without_patch: TransactionRule) -> None:
        result = transaction_rule_without_patch.to_dict()

        assert isinstance(result, dict)
        assert result["rules"] == ["amount < 0", "cleared == 'uncleared'"]
        assert result["patch"] is None

    def test_to_dict_with_empty_rules(self) -> None:
        rule = TransactionRule(rules=[], patch=None)
        result = rule.to_dict()

        assert result["rules"] == []
        assert result["patch"] is None

    @patch.object(models.SaveTransactionWithIdOrImportId, "from_dict")
    def test_from_dict_with_patch(self, mock_from_dict: MagicMock) -> None:
        mock_patch = MagicMock(spec=models.SaveTransactionWithIdOrImportId)
        mock_from_dict.return_value = mock_patch

        data = {
            "rules": ["amount > 100", "payee_name == 'Test'"],
            "patch": {"account_id": "test-account", "amount": 1000},
        }

        result = TransactionRule.from_dict(data)

        assert isinstance(result, TransactionRule)
        assert result.rules == ["amount > 100", "payee_name == 'Test'"]
        assert result.patch == mock_patch
        mock_from_dict.assert_called_once_with({"account_id": "test-account", "amount": 1000})

    def test_from_dict_without_patch(self) -> None:
        data = {"rules": ["amount < 0", "cleared == 'uncleared'"]}

        result = TransactionRule.from_dict(data)

        assert isinstance(result, TransactionRule)
        assert result.rules == ["amount < 0", "cleared == 'uncleared'"]
        assert result.patch is None

    def test_from_dict_with_empty_rules(self) -> None:
        data: dict[str, Any] = {"rules": []}

        result = TransactionRule.from_dict(data)

        assert result.rules == []
        assert result.patch is None

    def test_from_dict_with_no_rules_key(self) -> None:
        data: dict[str, Any] = {}

        result = TransactionRule.from_dict(data)

        assert result.rules == []
        assert result.patch is None

    def test_from_dict_with_non_string_rules(self) -> None:
        data = {
            "rules": [123, "amount > 100", True, None],
        }

        result = TransactionRule.from_dict(data)

        assert result.rules == ["123", "amount > 100", "True", "None"]
        assert result.patch is None

    def test_from_dict_with_empty_dict(self) -> None:
        data: dict[str, Any] = {}

        result = TransactionRule.from_dict(data)

        assert isinstance(result, TransactionRule)
        assert result.rules == []
        assert result.patch is None

    def test_round_trip_serialization_with_patch(self, transaction_rule_with_patch: TransactionRule) -> None:
        # Test that to_dict -> from_dict produces equivalent object
        dict_data = transaction_rule_with_patch.to_dict()

        with patch.object(models.SaveTransactionWithIdOrImportId, "from_dict") as mock_from_dict:
            mock_from_dict.return_value = transaction_rule_with_patch.patch

            restored_rule = TransactionRule.from_dict(dict_data)

            assert restored_rule.rules == transaction_rule_with_patch.rules
            assert restored_rule.patch == transaction_rule_with_patch.patch


class TestTransactionRules:
    @pytest.fixture
    def mock_transaction_rule(self) -> MagicMock:
        mock = MagicMock(spec=TransactionRule)
        mock.to_dict.return_value = {"rules": ["amount > 100"], "patch": {"account_id": "test-account"}}
        return mock

    @pytest.fixture
    def transaction_rules_with_rules(self, mock_transaction_rule: MagicMock) -> TransactionRules:
        rule1 = TransactionRule(rules=["amount > 100"], patch=None)
        rule2 = TransactionRule(rules=["payee_name == 'Test'"], patch=None)
        return TransactionRules(transaction_rules=[rule1, rule2])

    @pytest.fixture
    def transaction_rules_empty(self) -> TransactionRules:
        return TransactionRules(transaction_rules=[])

    def test_init_with_rules(self, transaction_rules_with_rules: TransactionRules) -> None:
        assert len(transaction_rules_with_rules.transaction_rules) == 2
        assert all(isinstance(rule, TransactionRule) for rule in transaction_rules_with_rules.transaction_rules)

    def test_init_with_empty_list(self, transaction_rules_empty: TransactionRules) -> None:
        assert transaction_rules_empty.transaction_rules == []

    def test_init_with_single_rule(self) -> None:
        rule = TransactionRule(rules=["amount > 100"], patch=None)
        transaction_rules = TransactionRules(transaction_rules=[rule])

        assert len(transaction_rules.transaction_rules) == 1
        assert transaction_rules.transaction_rules[0] == rule

    def test_to_dict_with_rules(self, transaction_rules_with_rules: TransactionRules) -> None:
        result = transaction_rules_with_rules.to_dict()

        assert isinstance(result, dict)
        assert "transaction_rules" in result
        assert len(result["transaction_rules"]) == 2
        assert all(isinstance(rule_dict, dict) for rule_dict in result["transaction_rules"])

    def test_to_dict_with_empty_rules(self, transaction_rules_empty: TransactionRules) -> None:
        result = transaction_rules_empty.to_dict()

        assert isinstance(result, dict)
        assert result["transaction_rules"] == []

    def test_to_dict_calls_to_dict_on_each_rule(self) -> None:
        mock_rule1 = MagicMock(spec=TransactionRule)
        mock_rule1.to_dict.return_value = {"rules": ["rule1"], "patch": None}
        mock_rule2 = MagicMock(spec=TransactionRule)
        mock_rule2.to_dict.return_value = {"rules": ["rule2"], "patch": None}

        transaction_rules = TransactionRules(transaction_rules=[mock_rule1, mock_rule2])
        result = transaction_rules.to_dict()

        mock_rule1.to_dict.assert_called_once()
        mock_rule2.to_dict.assert_called_once()
        assert result["transaction_rules"] == [{"rules": ["rule1"], "patch": None}, {"rules": ["rule2"], "patch": None}]

    @patch.object(TransactionRule, "from_dict")
    def test_from_dict_with_rules(self, mock_from_dict: MagicMock) -> None:
        mock_rule1 = MagicMock(spec=TransactionRule)
        mock_rule2 = MagicMock(spec=TransactionRule)
        mock_from_dict.side_effect = [mock_rule1, mock_rule2]

        data = {
            "transaction_rules": [
                {"rules": ["amount > 100"], "patch": None},
                {"rules": ["payee_name == 'Test'"], "patch": None},
            ]
        }

        result = TransactionRules.from_dict(data)

        assert isinstance(result, TransactionRules)
        assert len(result.transaction_rules) == 2
        assert result.transaction_rules[0] == mock_rule1
        assert result.transaction_rules[1] == mock_rule2
        assert mock_from_dict.call_count == 2

    def test_from_dict_with_empty_rules(self) -> None:
        data: dict[str, Any] = {"transaction_rules": []}

        result = TransactionRules.from_dict(data)

        assert isinstance(result, TransactionRules)
        assert result.transaction_rules == []

    def test_from_dict_with_no_transaction_rules_key(self) -> None:
        data: dict[str, Any] = {}

        result = TransactionRules.from_dict(data)

        assert isinstance(result, TransactionRules)
        assert result.transaction_rules == []

    @patch.object(TransactionRule, "from_dict")
    def test_from_dict_with_single_rule(self, mock_from_dict: MagicMock) -> None:
        mock_rule = MagicMock(spec=TransactionRule)
        mock_from_dict.return_value = mock_rule

        data = {"transaction_rules": [{"rules": ["amount > 100"], "patch": None}]}

        result = TransactionRules.from_dict(data)

        assert len(result.transaction_rules) == 1
        assert result.transaction_rules[0] == mock_rule
        mock_from_dict.assert_called_once_with({"rules": ["amount > 100"], "patch": None})

    def test_from_dict_with_empty_dict(self) -> None:
        data: dict[str, Any] = {}

        result = TransactionRules.from_dict(data)

        assert isinstance(result, TransactionRules)
        assert result.transaction_rules == []

    def test_round_trip_serialization_with_rules(self, transaction_rules_with_rules: TransactionRules) -> None:
        dict_data = transaction_rules_with_rules.to_dict()

        with patch.object(TransactionRule, "from_dict") as mock_from_dict:
            mock_from_dict.side_effect = transaction_rules_with_rules.transaction_rules

            restored_rules = TransactionRules.from_dict(dict_data)

            assert len(restored_rules.transaction_rules) == len(transaction_rules_with_rules.transaction_rules)

    def test_round_trip_serialization_empty(self, transaction_rules_empty: TransactionRules) -> None:
        dict_data = transaction_rules_empty.to_dict()
        restored_rules = TransactionRules.from_dict(dict_data)

        assert restored_rules.transaction_rules == transaction_rules_empty.transaction_rules

    @patch.object(TransactionRule, "from_dict")
    def test_from_dict_preserves_rule_order(self, mock_from_dict: MagicMock) -> None:
        rules_data = [
            {"rules": ["rule1"], "patch": None},
            {"rules": ["rule2"], "patch": None},
            {"rules": ["rule3"], "patch": None},
        ]

        mock_rules = [MagicMock(spec=TransactionRule) for _ in range(3)]
        mock_from_dict.side_effect = mock_rules

        data = {"transaction_rules": rules_data}
        result = TransactionRules.from_dict(data)

        assert len(result.transaction_rules) == 3
        for i, rule in enumerate(result.transaction_rules):
            assert rule == mock_rules[i]

    def test_to_dict_return_type(self, transaction_rules_with_rules: TransactionRules) -> None:
        result = transaction_rules_with_rules.to_dict()

        assert isinstance(result, dict)
        assert isinstance(result["transaction_rules"], list)

    def test_from_dict_return_type(self) -> None:
        data: dict[str, Any] = {"transaction_rules": []}
        result = TransactionRules.from_dict(data)

        assert isinstance(result, TransactionRules)
        assert hasattr(result, "transaction_rules")
