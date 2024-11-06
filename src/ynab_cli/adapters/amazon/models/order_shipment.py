import asyncio
from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING

from pydantic import computed_field
from typing_extensions import override

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import Client
from ynab_cli.adapters.amazon.models.entity import Entity
from ynab_cli.adapters.amazon.models.order_item import OrderItem


class OrderShipment(Entity, frozen=True):
    order_id: str
    items: tuple[OrderItem, ...]

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def subtotal(self) -> Decimal:
        subtotal = Decimal(0)
        for item in self.items:
            subtotal += item.total_price
        return subtotal

    @override
    async def hydrate(self, client: "Client") -> None:
        if self._is_hydrated:
            return

        hydrate_coroutines = []

        for item in self.items:
            hydrate_coroutines.append(item.hydrate(client))
        await asyncio.gather(*hydrate_coroutines)

        await super().hydrate(client)
