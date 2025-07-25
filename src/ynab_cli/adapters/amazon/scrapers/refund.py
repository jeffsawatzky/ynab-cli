import logging
import re
from typing import ClassVar

from bs4 import Tag
from dateutil import parser
from httpx import URL
from typing_extensions import override

from ynab_cli.adapters.amazon import locale
from ynab_cli.adapters.amazon.models.refund import Refund
from ynab_cli.adapters.amazon.scrapers.base import BaseScraper

log = logging.getLogger(__name__)


class RefundScraper(BaseScraper[Refund | None]):
    """Scrapes a single refund from:
    /spr/returns/cart?orderId=<order_id>
    """

    CONSUMED_UNIT_SECTION_SELECTOR: ClassVar[str] = "#consumed-unit-section"
    REFUND_TOTAL_SELECTOR: ClassVar[str] = "li:nth-child(1) font"
    REFUND_DATE_SELECTOR: ClassVar[str] = "li:nth-child(1) span"

    def __init__(self, order_id: str, product_id: str) -> None:
        super().__init__()

        self._order_id = order_id
        self._product_id = product_id

    @override
    async def scrape(self, response_url: URL, html: Tag) -> Refund | None:
        consumed_unit_section_tag = html.select_one(self.__class__.CONSUMED_UNIT_SECTION_SELECTOR)
        if not consumed_unit_section_tag:
            log.warning("Could not find consumed unit section tag")
            return None

        refund_total_tag = consumed_unit_section_tag.select_one(self.__class__.REFUND_TOTAL_SELECTOR)
        if not refund_total_tag:
            log.warning("Could not find refund total tag")
            return None
        refund_total = self.parse_currency(
            response_url, self.assert_host(response_url), self.normalized_text(refund_total_tag.text, whitespace=True)
        )

        refund_date_tag = consumed_unit_section_tag.select_one(self.__class__.REFUND_DATE_SELECTOR)
        if not refund_date_tag:
            log.warning("Could not find refund date tag")
            return None
        refund_date_str = self.normalized_text(refund_date_tag.text, whitespace=True)

        refund_date_regex = self.get_localized(response_url, locale.LOCALE_REFUND_DATE_REGEX, re.Pattern[str])
        refund_date_match = refund_date_regex.match(refund_date_str)
        if not refund_date_match:
            log.warning(f"Could not find refund date match: {refund_date_str}")
            return None
        refund_date_str = refund_date_match.group("refund_date")

        try:
            refund_date = parser.parse(refund_date_str).date()
        except ValueError:
            log.warning(f"Could not parse date: {refund_date_str}")
            return None

        return Refund(
            order_id=self._order_id,
            product_id=self._product_id,
            refund_total=refund_total,
            refund_date=refund_date,
        )
