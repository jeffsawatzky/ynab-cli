from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING

from anyio import create_task_group
from attrs import define, field
from typing_extensions import override

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import AmazonClient
from ynab_cli.adapters.amazon.models.entity import Entity
from ynab_cli.adapters.amazon.models.order_shipment import OrderShipment
from ynab_cli.adapters.amazon.models.refund import Refund


@define
class Order(Entity):
    order_id: str
    refund_link: str
    grand_total: Decimal
    shipments: tuple[OrderShipment, ...]

    _refunds: list[Refund] | None = field(default=None, init=False)

    @property
    def refunds(self) -> list[Refund]:
        if self._refunds is None:
            raise ValueError("Refunds are not hydrated")
        return self._refunds

    @cached_property
    def item_subtotal(self) -> Decimal:
        subtotal = Decimal(0)
        for shipment in self.shipments:
            subtotal += shipment.subtotal
        return subtotal

    @override
    async def hydrate(self, client: "AmazonClient") -> None:
        if self._is_hydrated:
            return

        refunds = []
        async with create_task_group() as tg:
            async for refund in client.get_refunds_from_link(self.refund_link):
                refunds.append(refund)
                tg.start_soon(refund.hydrate, client)
            for shipment in self.shipments:
                tg.start_soon(shipment.hydrate, client)

        self._refunds = refunds

        await super().hydrate(client)
