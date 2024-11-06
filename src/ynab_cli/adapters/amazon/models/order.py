import asyncio
from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING

from pydantic import computed_field
from typing_extensions import override

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import Client
from ynab_cli.adapters.amazon.models.entity import Entity
from ynab_cli.adapters.amazon.models.order_shipment import OrderShipment
from ynab_cli.adapters.amazon.models.refund import Refund


class Order(Entity, frozen=True):
    order_id: str
    refund_link: str
    grand_total: Decimal
    shipments: tuple[OrderShipment, ...]

    _refunds: list[Refund] | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def refunds(self) -> list[Refund]:
        if self._refunds is None:
            raise ValueError("Refunds are not hydrated")
        return self._refunds

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def item_subtotal(self) -> Decimal:
        subtotal = Decimal(0)
        for shipment in self.shipments:
            subtotal += shipment.subtotal
        return subtotal

    @override
    async def hydrate(self, client: "Client") -> None:
        if self._is_hydrated:
            return

        hydrate_coroutines = []

        refunds = []
        async for refund in client.get_refunds_from_link(self.refund_link):
            refunds.append(refund)
            hydrate_coroutines.append(refund.hydrate(client))
        for shipment in self.shipments:
            hydrate_coroutines.append(shipment.hydrate(client))
        await asyncio.gather(*hydrate_coroutines)

        self._refunds = refunds

        await super().hydrate(client)
