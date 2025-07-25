from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING

from anyio import create_task_group
from attrs import define
from typing_extensions import override

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import AmazonClient
from ynab_cli.adapters.amazon.models.entity import Entity
from ynab_cli.adapters.amazon.models.order_item import OrderItem


@define
class OrderShipment(Entity):
    order_id: str
    items: tuple[OrderItem, ...]

    @cached_property
    def subtotal(self) -> Decimal:
        subtotal = Decimal(0)
        for item in self.items:
            subtotal += item.total_price
        return subtotal

    @override
    async def hydrate(self, client: "AmazonClient") -> None:
        if self._is_hydrated:
            return

        async with create_task_group() as tg:
            for item in self.items:
                tg.start_soon(item.hydrate, client)

        await super().hydrate(client)
