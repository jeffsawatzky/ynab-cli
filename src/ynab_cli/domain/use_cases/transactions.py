from getpass import getpass

import rule_engine

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import api, models
from ynab_cli.domain.models import rules
from ynab_cli.host.cli.constants import YNAB_API_URL


def should_skip_transaction(transaction: models.TransactionDetail) -> bool:
    if transaction.deleted or transaction.category_name in ["Split"]:
        return True
    return False


def get_save_transaction(
    transaction_detail: models.TransactionDetail,
    transaction_rules: rules.TransactionRules,
) -> models.SaveTransactionWithIdOrImportId | None:
    transaction_detail_dict = transaction_detail.to_dict()

    context = rule_engine.Context(default_value=None)
    for rule in transaction_rules.transaction_rules:
        if any(rule_engine.Rule(rule_str, context=context).matches(transaction_detail_dict) for rule_str in rule.rules):
            if rule.patch:
                save_transaction_dict = rule.patch.to_dict()
                save_transaction_dict["id"] = transaction_detail.id
                save_transaction_dict["import_id"] = transaction_detail.import_id

                save_transaction = models.SaveTransactionWithIdOrImportId(**save_transaction_dict)

                return save_transaction

    return None


async def apply_rules(
    access_token: str, budget_id: str, dry_run: bool, transaction_rules: rules.TransactionRules
) -> None:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            transactions_response = await api.TransactionsApi(api_client).get_transactions(budget_id, type="unapproved")
            transactions = transactions_response.data.transactions

            save_transactions = []
            for transaction in transactions:
                if should_skip_transaction(transaction=transaction):
                    continue

                save_transaction = get_save_transaction(
                    transaction_detail=transaction, transaction_rules=transaction_rules
                )
                if save_transaction:
                    print(
                        f"{transaction.id}: ({(transaction.payee_name, transaction.category_name, transaction.amount)}) -> {save_transaction.to_dict()}"
                    )

                    if not dry_run:
                        save_transactions.append(save_transaction)

            if save_transactions:
                try:
                    await api.TransactionsApi(api_client).update_transactions(
                        budget_id,
                        models.PatchTransactionsWrapper(transactions=save_transactions),
                    )
                except ynab.ApiError as e:
                    if e.status == 429:
                        new_access_token = getpass(prompt="API rate limit exceeded. Enter a new access token: ")
                        api_client.configuration.access_token = new_access_token
                        await api.TransactionsApi(api_client).update_transactions(
                            budget_id,
                            models.PatchTransactionsWrapper(transactions=save_transactions),
                        )
                    else:
                        raise e

        except ynab.ApiError as e:
            if e.status == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")
