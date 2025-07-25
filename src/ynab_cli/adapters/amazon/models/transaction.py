from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from anyio import create_task_group
from attrs import define, field
from typing_extensions import override

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import AmazonClient
from ynab_cli.adapters.amazon.models.entity import Entity
from ynab_cli.adapters.amazon.models.order import Order


@define
class Transaction(Entity):
    completed_date: date
    payment_method: str
    grand_total: Decimal
    order_id: str
    order_link: str
    seller: str
    is_refund: bool
    is_gift_card: bool

    _order: Order | None = field(default=None, init=False)

    @property
    def order(self) -> Order:
        if self._order is None:
            raise ValueError("Order not hydrated")
        return self._order

    @override
    async def hydrate(self, client: "AmazonClient") -> None:
        if self._is_hydrated:
            return

        order = await client.get_order_from_link(self.order_link)

        async with create_task_group() as tg:
            tg.start_soon(order.hydrate, client)

        self._order = order

        await super().hydrate(client)
