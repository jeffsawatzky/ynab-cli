from typing import Any

from attrs import define as _attrs_define

from ynab_cli.adapters.ynab import models


@_attrs_define
class TransactionRule:
    # List of rules that follow the rule-engine format for a transaction.
    #   See: https://zerosteiner.github.io/rule-engine/
    # The rules are given a TransactionDetail object
    #   See: https://api.ynab.com/v1#/Transactions/getTransactions
    rules: list[str]

    # The JSON SaveTransactionWithIdOrImportId to apply to the transaction if the rules are matched.
    # The id/import_id will be provided. Just fill in what you want to update.
    #   See: https://api.ynab.com/v1#/Transactions/updateTransactions
    patch: models.SaveTransactionWithIdOrImportId | None = None


@_attrs_define
class TransactionRules:
    transaction_rules: list[TransactionRule]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TransactionRules":
        transaction_rules = []
        for rule in data.get("transaction_rules", []):
            rules = [str(r) for r in rule.get("rules", [])]
            patch = None
            if "patch" in rule:
                patch = models.SaveTransactionWithIdOrImportId.from_dict(rule["patch"])

            transaction_rules.append(TransactionRule(rules=rules, patch=patch))

        return cls(transaction_rules=transaction_rules)
