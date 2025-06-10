from typing import Any, Self

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

    def to_dict(self) -> dict[str, Any]:
        return {
            "rules": self.rules,
            "patch": self.patch.to_dict() if self.patch else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        rules = [str(r) for r in data.get("rules", [])]
        patch = None
        if "patch" in data:
            patch = models.SaveTransactionWithIdOrImportId.from_dict(data["patch"])

        return cls(rules=rules, patch=patch)


@_attrs_define
class TransactionRules:
    transaction_rules: list[TransactionRule]

    def to_dict(self) -> dict[str, Any]:
        return {"transaction_rules": [rule.to_dict() for rule in self.transaction_rules]}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        transaction_rules = []
        for rule in data.get("transaction_rules", []):
            transaction_rules.append(TransactionRule.from_dict(rule))

        return cls(transaction_rules=transaction_rules)
