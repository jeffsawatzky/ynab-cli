from collections.abc import AsyncIterator
from typing import TypedDict

import rule_engine

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.transactions import get_transactions, update_transactions
from ynab_cli.domain import ports
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


class ApplyRules:
    """Use case for applying rules to transactions."""

    def __init__(self, io: ports.IO, client: ynab.AuthenticatedClient):
        self._io = io
        self._client = client

    async def __call__(
        self, settings: Settings, params: ApplyRulesParams
    ) -> AsyncIterator[tuple[models.TransactionDetail, models.SaveTransactionWithIdOrImportId]]:
        try:
            progress_total = 0

            transactions = (
                await util.get_asyncio_detailed(
                    self._io,
                    get_transactions.asyncio_detailed,
                    settings.ynab.budget_id,
                    client=self._client,
                    type_=models.GetTransactionsType.UNAPPROVED,
                )
            ).data.transactions
            transactions.sort(key=lambda t: t.date)

            save_transactions = []

            progress_total = len(transactions)
            await self._io.progress.update(total=progress_total)
            for transaction in transactions:
                await self._io.progress.update(advance=1)

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
                await util.run_asyncio_detailed(
                    self._io,
                    update_transactions.asyncio_detailed,
                    settings.ynab.budget_id,
                    client=self._client,
                    body=models.PatchTransactionsWrapper(transactions=save_transactions),
                )

        except Exception as e:
            if isinstance(e, util.ApiError) and e.status_code == 401:
                await self._io.print("Invalid or expired access token. Please update your settings.")
            elif isinstance(e, util.ApiError) and e.status_code == 429:
                await self._io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await self._io.print(f"Exception when calling YNAB: {e}")
        finally:
            await self._io.progress.update(total=progress_total, completed=progress_total)
