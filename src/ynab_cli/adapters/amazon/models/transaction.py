import asyncio
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import computed_field
from typing_extensions import override

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import Client
from ynab_cli.adapters.amazon.models.entity import Entity
from ynab_cli.adapters.amazon.models.order import Order


class Transaction(Entity, frozen=True):
    completed_date: date
    payment_method: str
    grand_total: Decimal
    order_id: str
    order_link: str
    seller: str
    is_refund: bool
    is_gift_card: bool

    _order: Order | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def order(self) -> Order:
        if self._order is None:
            raise ValueError("Order not hydrated")
        return self._order

    @override
    async def hydrate(self, client: "Client") -> None:
        if self._is_hydrated:
            return

        hydrate_coroutines = []

        order = await client.get_order_from_link(self.order_link)
        hydrate_coroutines.append(order.hydrate(client))
        await asyncio.gather(*hydrate_coroutines)

        self._order = order

        await super().hydrate(client)
