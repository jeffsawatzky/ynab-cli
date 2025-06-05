from collections.abc import AsyncIterator
from typing import TypedDict

import rule_engine

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.transactions import get_transactions, update_transactions
from ynab_cli.domain import ports
from ynab_cli.domain.constants import YNAB_API_URL
from ynab_cli.domain.models import rules
from ynab_cli.domain.settings import Settings


def _should_skip_transaction(transaction: models.TransactionDetail) -> bool:
    if transaction.deleted or transaction.category_name in ["Split"]:
        return True
    return False


def _get_save_transaction(
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


class ApplyRulesParams(TypedDict):
    transaction_rules: rules.TransactionRules


async def apply_rules(
    settings: Settings, io: ports.IO, params: ApplyRulesParams
) -> AsyncIterator[tuple[models.TransactionDetail, models.SaveTransactionWithIdOrImportId]]:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=settings.ynab.access_token) as client:
        try:
            get_transactions_response = await get_transactions.asyncio_detailed(
                settings.ynab.budget_id,
                client=client,
                type_=models.GetTransactionsType.UNAPPROVED,
            )
            transactions = util.get_ynab_model(get_transactions_response, models.TransactionsResponse).data.transactions

            save_transactions = []

            progress_total = len(transactions)
            for transaction in transactions:
                await io.progress.update(total=progress_total, advance=1)

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
                    util.ensure_success(
                        await update_transactions.asyncio_detailed(
                            settings.ynab.budget_id,
                            client=client,
                            body=models.PatchTransactionsWrapper(transactions=save_transactions),
                        )
                    )
                except util.ApiError as e:
                    if e.status_code == 429:
                        new_access_token = await io.prompt(
                            prompt="API rate limit exceeded. Enter a new access token", password=True
                        )
                        client.token = new_access_token
                        util.ensure_success(
                            await update_transactions.asyncio_detailed(
                                settings.ynab.budget_id,
                                client=client,
                                body=models.PatchTransactionsWrapper(transactions=save_transactions),
                            )
                        )
                    else:
                        raise e

        except util.ApiError as e:
            if e.status_code == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")
