from getpass import getpass

import rule_engine

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.transactions import get_transactions, update_transactions
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

                save_transaction = models.SaveTransactionWithIdOrImportId.from_dict(save_transaction_dict)

                return save_transaction

    return None


async def apply_rules(
    access_token: str, budget_id: str, dry_run: bool, transaction_rules: rules.TransactionRules
) -> None:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=access_token) as client:
        try:
            get_transactions_response = await get_transactions.asyncio_detailed(
                budget_id,
                client=client,
                type_=models.GetTransactionsType.UNAPPROVED,
            )
            transactions = util.get_ynab_model(get_transactions_response, models.TransactionsResponse).data.transactions

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
                    util.ensure_success(
                        await update_transactions.asyncio_detailed(
                            budget_id,
                            client=client,
                            body=models.PatchTransactionsWrapper(transactions=save_transactions),
                        )
                    )
                except util.ApiError as e:
                    if e.status_code == 429:
                        new_access_token = getpass(prompt="API rate limit exceeded. Enter a new access token: ")
                        client.token = new_access_token
                        util.ensure_success(
                            await update_transactions.asyncio_detailed(
                                budget_id,
                                client=client,
                                body=models.PatchTransactionsWrapper(transactions=save_transactions),
                            )
                        )
                    else:
                        raise e

        except util.ApiError as e:
            if e.status_code == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")
