import logging
from typing import ClassVar

from bs4 import Tag
from httpx import URL
from typing_extensions import override

from ynab_cli.adapters.amazon.models.order_shipment import OrderShipment
from ynab_cli.adapters.amazon.scrapers.base import BaseScraper
from ynab_cli.adapters.amazon.scrapers.order_item import OrderItemScraper

log = logging.getLogger(__name__)


class OrderShipmentScraper(BaseScraper[OrderShipment | None]):
    """Scrapes an order shipment from:
    /gp/your-account/order-details?orderID=<order_id>
    """

    # Order items are rendered in a couple different ways, so we need to try multiple selectors
    ORDER_ITEM_SELECTORS: ClassVar[list[str]] = [
        "[data-component='purchasedItems'] .a-fixed-left-grid",
        "div:has(> div.yohtmlc-item)",
    ]

    def __init__(self, order_id: str) -> None:
        super().__init__()

        self._order_id = order_id

    @override
    async def scrape(self, response_url: URL, html: Tag) -> OrderShipment | None:
        order_item_tags = self.select(html, self.__class__.ORDER_ITEM_SELECTORS)
        if not order_item_tags:
            log.error("Could not find order item tags")
            return None

        items = []
        for order_item_tag in order_item_tags:
            item = await OrderItemScraper(self._order_id).scrape(response_url, order_item_tag)
            if not item:
                log.error("Could not scrape order item")
                return None
            items.append(item)

        return OrderShipment(
            order_id=self._order_id,
            items=tuple(items),
        )
