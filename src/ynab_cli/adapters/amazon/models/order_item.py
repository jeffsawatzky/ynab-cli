from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING

from anyio import create_task_group
from attrs import define, field
from typing_extensions import override

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import AmazonClient
from ynab_cli.adapters.amazon.models.entity import Entity
from ynab_cli.adapters.amazon.models.product import Product


@define
class OrderItem(Entity):
    order_id: str
    product_id: str
    product_link: str
    title: str
    unit_price: Decimal
    quantity: int

    _product: Product | None = field(default=None, init=False)

    @property
    def product(self) -> Product:
        if self._product is None:
            raise ValueError("Product not hydrated")
        return self._product

    @cached_property
    def total_price(self) -> Decimal:
        return self.unit_price * Decimal(self.quantity)

    @override
    async def hydrate(self, client: "AmazonClient") -> None:
        if self._is_hydrated:
            return

        product = await client.get_product_from_link(self.product_link)
        async with create_task_group() as tg:
            tg.start_soon(product.hydrate, client)

        self._product = product

        await super().hydrate(client)
