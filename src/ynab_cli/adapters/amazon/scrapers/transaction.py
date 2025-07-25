import logging
import re
from datetime import date
from typing import ClassVar

from bs4 import Tag
from httpx import URL
from typing_extensions import override

from ynab_cli.adapters.amazon import locale
from ynab_cli.adapters.amazon.models.transaction import Transaction
from ynab_cli.adapters.amazon.scrapers.base import BaseScraper

log = logging.getLogger(__name__)


class TransactionScraper(BaseScraper[Transaction | None]):
    """Scrapes a single transaction from:
    /cpe/yourpayments/transactions
    """

    PAYMENT_METHOD_SELECTOR: ClassVar[str] = (
        "div.apx-transactions-line-item-component-container > div:nth-child(1) span.a-size-base"
    )
    ORDER_LINK_SELECTOR: ClassVar[str] = (
        "div.apx-transactions-line-item-component-container > div:nth-child(2) a.a-link-normal"
    )
    GRAND_TOTAL_SELECTOR: ClassVar[str] = (
        "div.apx-transactions-line-item-component-container > div:nth-child(1) span.a-size-base-plus"
    )
    SELLER_NAME_SELECTOR: ClassVar[str] = (
        "div.apx-transactions-line-item-component-container > div:nth-child(3) span.a-size-base"
    )
    ORDER_ID_REGEX: ClassVar[re.Pattern[str]] = re.compile(r"orderID=(?P<order_id>[\d-]+)")

    def __init__(self, completed_date: date) -> None:
        super().__init__()

        self._completed_date = completed_date

    @override
    async def scrape(self, response_url: URL, html: Tag) -> Transaction | None:
        payment_method_tag = html.select_one(self.__class__.PAYMENT_METHOD_SELECTOR)
        if not payment_method_tag:
            log.warning("Could not find payment method tag")
            return None
        payment_method = self.normalized_text(payment_method_tag.text, whitespace=True)
        is_gift_card = (
            payment_method.lower()
            == self.get_localized(response_url, locale.LOCALE_AMAZON_GIFT_CARD_PAYMENT_METHOD, str).lower()
        )

        order_link_tag = html.select_one(self.__class__.ORDER_LINK_SELECTOR)
        if not order_link_tag:
            log.warning("Could not find order link tag")
            return None
        order_link = self.absolute_url(response_url, self.normalized_text(order_link_tag.get("href")))

        order_id_match = self.__class__.ORDER_ID_REGEX.search(order_link)
        if not order_id_match:
            log.warning("Could not find order ID in order link")
            return None
        order_number = order_id_match.group("order_id")

        grand_total_tag = html.select_one(self.__class__.GRAND_TOTAL_SELECTOR)
        if not grand_total_tag:
            log.warning("Could not find grand total tag")
            return None
        grand_total = self.parse_currency(
            response_url,
            URL(order_link).host or self.assert_host(response_url),
            self.normalized_text(grand_total_tag.text, whitespace=True),
        )

        seller_name_tag = html.select_one(self.__class__.SELLER_NAME_SELECTOR)
        if not seller_name_tag:
            # This is empty for gift card transactions
            seller_name = "Amazon"
        else:
            seller_name = self.normalized_text(seller_name_tag.text, whitespace=True)

        return Transaction(
            completed_date=self._completed_date,
            payment_method=payment_method,
            grand_total=abs(grand_total),
            order_id=order_number,
            order_link=order_link,
            seller=seller_name,
            is_refund=grand_total > 0,
            is_gift_card=is_gift_card,
        )
