import asyncio
import logging
from collections.abc import AsyncIterator
from datetime import date
from typing import TypedDict

from ynab_cli.adapters import amazon
from ynab_cli.domain import models, ports
from ynab_cli.domain.settings import Settings

log = logging.getLogger(__name__)


async def _get_amazon_transaction_groups(
    io: ports.IO, client: amazon.Client
) -> AsyncIterator[models.AmazonTransactionGroup]:
    current_completed_date = None
    amazon_transaction_groups: dict[tuple[date, str, str, str, str, bool, bool], models.AmazonTransactionGroup] = {}

    async for amazon_transaction in client.get_transactions():
        if amazon_transaction.completed_date != current_completed_date:
            # We've entered a new date group, yield the current group
            for amazon_transaction_group in amazon_transaction_groups.values():
                yield amazon_transaction_group
            current_completed_date = amazon_transaction.completed_date
            amazon_transaction_groups = {}

        key = models.AmazonTransactionGroup.key(amazon_transaction)
        if key in amazon_transaction_groups:
            amazon_transaction_group = amazon_transaction_groups[key]
            amazon_transaction_group = amazon_transaction_group.append(amazon_transaction)
            amazon_transaction_groups[key] = amazon_transaction_group
        else:
            amazon_transaction_groups[key] = models.AmazonTransactionGroup(
                completed_date=amazon_transaction.completed_date,
                payment_method=amazon_transaction.payment_method,
                order_id=amazon_transaction.order_id,
                order_link=amazon_transaction.order_link,
                seller=amazon_transaction.seller,
                is_refund=amazon_transaction.is_refund,
                is_gift_card=amazon_transaction.is_gift_card,
                transactions=tuple([amazon_transaction]),
            )

    # Yield the last date group
    for amazon_transaction_group in amazon_transaction_groups.values():
        yield amazon_transaction_group


class ListTransactionsParams(TypedDict):
    pass


async def list_transactions(
    settings: Settings, io: ports.IO, params: ListTransactionsParams
) -> AsyncIterator[models.AmazonTransactionGroup]:
    if not settings.amazon:
        raise ValueError("Amazon settings are not configured")

    async with amazon.Client(settings.amazon.username, settings.amazon.password, settings.amazon.host, io=io) as client:
        async for amazon_transaction_group in _get_amazon_transaction_groups(io, client):
            hydrate_coroutines = []
            for transaction in amazon_transaction_group.transactions:
                hydrate_coroutines.append(transaction.hydrate(client))
            await asyncio.gather(*hydrate_coroutines)

            yield amazon_transaction_group
