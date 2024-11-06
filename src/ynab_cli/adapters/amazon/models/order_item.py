import asyncio
from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING

from pydantic import computed_field
from typing_extensions import override

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import Client
from ynab_cli.adapters.amazon.models.entity import Entity
from ynab_cli.adapters.amazon.models.product import Product


class OrderItem(Entity, frozen=True):
    order_id: str
    product_id: str
    product_link: str
    title: str
    unit_price: Decimal
    quantity: int

    _product: Product | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def product(self) -> Product:
        if self._product is None:
            raise ValueError("Product not hydrated")
        return self._product

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def total_price(self) -> Decimal:
        return self.unit_price * Decimal(self.quantity)

    @override
    async def hydrate(self, client: "Client") -> None:
        if self._is_hydrated:
            return

        hydrate_coroutines = []

        product = await client.get_product_from_link(self.product_link)
        hydrate_coroutines.append(product.hydrate(client))
        await asyncio.gather(*hydrate_coroutines)

        self._product = product

        await super().hydrate(client)
