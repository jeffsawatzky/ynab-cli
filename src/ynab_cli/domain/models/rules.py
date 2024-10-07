from pydantic import BaseModel

from ynab_cli.adapters.ynab import models


class TransactionRule(BaseModel):
    # List of rules that follow the rule-engine format for a transaction.
    #   See: https://zerosteiner.github.io/rule-engine/
    # The rules are given a TransactionDetail object
    #   See: https://api.ynab.com/v1#/Transactions/getTransactions
    rules: list[str]

    # The JSON SaveTransactionWithIdOrImportId to apply to the transaction if the rules are matched.
    # The id/import_id will be provided. Just fill in what you want to update.
    #   See: https://api.ynab.com/v1#/Transactions/updateTransactions
    patch: models.SaveTransactionWithIdOrImportId | None = None


class TransactionRules(BaseModel):
    transaction_rules: list[TransactionRule]
