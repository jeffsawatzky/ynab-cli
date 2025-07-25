import logging
from typing import ClassVar

from bs4 import Tag
from httpx import URL
from typing_extensions import override

from ynab_cli.adapters.amazon.constants import Routes
from ynab_cli.adapters.amazon.models.order import Order
from ynab_cli.adapters.amazon.scrapers.base import BaseScraper
from ynab_cli.adapters.amazon.scrapers.order_shipment import OrderShipmentScraper

log = logging.getLogger(__name__)


class OrderScraper(BaseScraper[Order | None]):
    """Scrapes an order from:
    /gp/your-account/order-details?orderID=<order_id>
    """

    ORDER_DETAILS_SELECTOR: ClassVar[str] = "#orderDetails"
    ORDER_ID_SELECTOR: ClassVar[str] = "span.order-date-invoice-item > bdi"
    GRAND_TOTAL_SELECTOR: ClassVar[str] = (
        "div[data-component='orderSubtotals'] div.a-column.a-span5 > span.a-color-base.a-text-bold"
    )
    SHIPMENTS_SELECTOR: ClassVar[str] = "div[data-component='shipments']"
    SHIPMENT_SELECTOR: ClassVar[str] = "div[data-component='shipments'] div.a-box > div.a-box-inner"

    # Order items are rendered in a couple different ways, so we need to try multiple selectors
    ORDER_ITEM_SELECTORS: ClassVar[list[str]] = [
        "[data-component='purchasedItems'] .a-fixed-left-grid",
        "div:has(> div.yohtmlc-item)",
    ]

    @override
    async def scrape(self, response_url: URL, html: Tag) -> Order | None:
        order_details_tag = html.select_one(self.__class__.ORDER_DETAILS_SELECTOR)
        if not order_details_tag:
            log.error("Could not find order details tag")
            return None

        order_id_tag = order_details_tag.select_one(self.__class__.ORDER_ID_SELECTOR)
        if not order_id_tag:
            log.error("Could not find order ID tag")
            return None
        order_id = self.normalized_text(order_id_tag.text, whitespace=True)

        refund_link = self.absolute_url(response_url, str(Routes.REFUNDS.copy_set_param(key="orderId", value=order_id)))

        grand_total_tag = order_details_tag.select_one(self.__class__.GRAND_TOTAL_SELECTOR)
        if not grand_total_tag:
            log.error("Could not find grand total tag")
            return None
        grand_total = self.parse_currency(
            response_url, self.assert_host(response_url), self.normalized_text(grand_total_tag.text, whitespace=True)
        )

        shipments_tag = order_details_tag.select_one(self.__class__.SHIPMENTS_SELECTOR)
        if not shipments_tag:
            log.error("Could not find shipments tag")
            return None

        shipment_tags = shipments_tag.select(self.__class__.SHIPMENT_SELECTOR)
        if not shipment_tags:
            log.error("Could not find shipment tags")
            return None

        shipments = []
        for shipment_tag in shipment_tags:
            shipment = await OrderShipmentScraper(order_id).scrape(response_url, shipment_tag)
            if not shipment:
                log.error("Could not scrape order shipment")
                return None
            shipments.append(shipment)

        return Order(
            order_id=order_id,
            refund_link=refund_link,
            grand_total=grand_total,
            shipments=tuple(shipments),
        )
