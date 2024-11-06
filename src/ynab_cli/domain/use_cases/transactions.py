import logging
from collections.abc import AsyncIterator
from typing import TypedDict

import rule_engine

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import api as ynab_api
from ynab_cli.adapters.ynab import models as ynab_models
from ynab_cli.domain import models, ports
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases.constants import YNAB_API_URL

log = logging.getLogger(__name__)


def _should_skip_transaction(transaction: ynab_models.TransactionDetail) -> bool:
    if transaction.deleted or transaction.category_name in ["Split"]:
        return True
    return False


def _get_save_transaction(
    transaction_detail: ynab_models.TransactionDetail, transaction_rules: models.TransactionRules
) -> ynab_models.SaveTransactionWithIdOrImportId | None:
    transaction_detail_dict = transaction_detail.to_dict()

    context = rule_engine.Context(default_value=None)
    for rule in transaction_rules.transaction_rules:
        if any(rule_engine.Rule(rule_str, context=context).matches(transaction_detail_dict) for rule_str in rule.rules):
            if rule.patch:
                save_transaction_dict = rule.patch.to_dict()
                save_transaction_dict["id"] = transaction_detail.id
                save_transaction_dict["import_id"] = transaction_detail.import_id

                save_transaction = ynab_models.SaveTransactionWithIdOrImportId(**save_transaction_dict)

                return save_transaction

    return None


class ApplyRulesParams(TypedDict):
    transaction_rules: models.TransactionRules


async def apply_rules(
    settings: Settings, io: ports.IO, params: ApplyRulesParams
) -> AsyncIterator[tuple[ynab_models.TransactionDetail, ynab_models.SaveTransactionWithIdOrImportId]]:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=settings.ynab.access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            transactions_response = await ynab_api.TransactionsApi(api_client).get_transactions(
                settings.ynab.budget_id, type="unapproved"
            )
            transactions = transactions_response.data.transactions

            save_transactions = []
            for transaction in transactions:
                if _should_skip_transaction(transaction=transaction):
                    continue

                save_transaction = _get_save_transaction(
                    transaction_detail=transaction, transaction_rules=params["transaction_rules"]
                )
                if save_transaction:
                    yield (transaction, save_transaction)

                    if not settings.dry_run:
                        save_transactions.append(save_transaction)

            if save_transactions:
                try:
                    await ynab_api.TransactionsApi(api_client).update_transactions(
                        settings.ynab.budget_id,
                        ynab_models.PatchTransactionsWrapper(transactions=save_transactions),
                    )
                except ynab.ApiError as e:
                    if e.status == 429:
                        new_access_token = await io.prompt(
                            prompt="API rate limit exceeded. Enter a new access token", password=True
                        )
                        api_client.configuration.access_token = new_access_token
                        await ynab_api.TransactionsApi(api_client).update_transactions(
                            settings.ynab.budget_id,
                            ynab_models.PatchTransactionsWrapper(transactions=save_transactions),
                        )
                    else:
                        raise e

        except ynab.ApiError as e:
            if e.status == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")
