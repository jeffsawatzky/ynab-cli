import logging
import re
from typing import ClassVar

from bs4 import Tag
from httpx import URL
from typing_extensions import override

from ynab_cli.adapters.amazon.models.order_item import OrderItem
from ynab_cli.adapters.amazon.scrapers.base import BaseScraper

log = logging.getLogger(__name__)


class OrderItemScraper(BaseScraper[OrderItem | None]):
    """Scrapes an order item from:
    /gp/your-account/order-details?orderID=<order_id>

    Order items are rendered in a couple different ways, so we need to try multiple selectors
    """

    PRODUCT_LINK_SELECTORS: ClassVar[list[str]] = [
        "[data-component='itemTitle'] a",
        "div.yohtmlc-item a",
    ]
    UNIT_PRICE_SELECTORS: ClassVar[list[str]] = [
        "[data-component='unitPrice'] .a-text-price :not(.a-offscreen)",
        ".yohtmlc-item .a-color-price",
        ".yohtmlc-item .gift-card-instance .a-span2",
    ]
    QUANTITY_SELECTORS: ClassVar[list[str]] = [
        ".od-item-view-qty > span",
        "span.item-view-qty",
    ]

    PRODUCT_ID_REGEX: ClassVar[re.Pattern[str]] = re.compile(
        r"(/dp/(?P<product_id1>[a-zA-Z0-9]+)|/gp/product/(?P<product_id2>[a-zA-Z0-9]+))"
    )

    def __init__(self, order_id: str) -> None:
        super().__init__()

        self._order_id = order_id

    @override
    async def scrape(self, response_url: URL, html: Tag) -> OrderItem | None:
        product_link_tag = self.select_one(html, self.__class__.PRODUCT_LINK_SELECTORS)
        if not product_link_tag:
            log.error("Could not find product link tag")
            return None
        product_link = self.absolute_url(response_url, self.normalized_text(product_link_tag.get("href")))

        product_id_match = self.__class__.PRODUCT_ID_REGEX.search(product_link)
        if not product_id_match:
            log.error("Could not find product ID in product link")
            return None
        product_id = product_id_match.group("product_id1") or product_id_match.group("product_id2")

        title = self.normalized_text(product_link_tag.text, whitespace=True)

        unit_price_tag = self.select_one(html, self.__class__.UNIT_PRICE_SELECTORS)
        if not unit_price_tag:
            log.error("Could not find unit price tag")
            return None
        unit_price = self.parse_currency(
            response_url, self.assert_host(response_url), self.normalized_text(unit_price_tag.text, whitespace=True)
        )

        quantity_tag = self.select_one(html, self.__class__.QUANTITY_SELECTORS)
        if not quantity_tag:
            quantity = 1
        else:
            quantity = int(self.normalized_text(quantity_tag.text, whitespace=True))

        return OrderItem(
            order_id=self._order_id,
            product_id=product_id,
            product_link=product_link,
            title=title,
            unit_price=unit_price,
            quantity=quantity,
        )
