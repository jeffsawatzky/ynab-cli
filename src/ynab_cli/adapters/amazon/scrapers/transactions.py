import logging
from collections.abc import AsyncIterator
from typing import ClassVar

from bs4 import Tag
from dateutil import parser
from httpx import URL
from typing_extensions import override

from ynab_cli.adapters.amazon.models.transaction import Transaction
from ynab_cli.adapters.amazon.scrapers.base import BaseScraper
from ynab_cli.adapters.amazon.scrapers.transaction import TransactionScraper

log = logging.getLogger(__name__)


class TransactionsScraper(BaseScraper[AsyncIterator[Transaction]]):
    """Scrapes transactions from:
    /cpe/yourpayments/transactions
    """

    FORM_SELECTOR: ClassVar[str] = "form:has(input[name='ppw-widgetState'])"
    DATE_CONTAINERS_SELECTOR: ClassVar[str] = "div.apx-transaction-date-container"
    DATE_SELECTOR: ClassVar[str] = "span"
    TRANSACTIONS_CONTAINER_SELECTOR: ClassVar[str] = "div"
    TRANSACTIONS_SELECTOR: ClassVar[str] = "div.apx-transactions-line-item-component-container"

    @override
    async def scrape(self, response_url: URL, html: Tag) -> AsyncIterator[Transaction]:
        async def async_iter() -> AsyncIterator[Transaction]:
            form_tag = html.select_one(self.__class__.FORM_SELECTOR)
            if not form_tag:
                log.warning("Could not find form tag")
                return

            date_container_tags = form_tag.select(self.__class__.DATE_CONTAINERS_SELECTOR)
            for date_container_tag in date_container_tags:
                date_tag = date_container_tag.select_one(self.__class__.DATE_SELECTOR)
                if not date_tag:
                    log.warning("Could not find date tag")
                    continue

                date_str = self.normalized_text(date_tag.text, whitespace=True)
                try:
                    date = parser.parse(date_str).date()
                except ValueError:
                    log.warning(f"Could not parse date: {date_str}")
                    continue

                transactions_container_tag = date_container_tag.find_next_sibling(
                    self.__class__.TRANSACTIONS_CONTAINER_SELECTOR
                )
                if not isinstance(transactions_container_tag, Tag):
                    log.warning("Could not find transactions container tag")
                    continue

                transaction_tags = transactions_container_tag.select(self.__class__.TRANSACTIONS_SELECTOR)
                for transaction_tag in transaction_tags:
                    transaction = await TransactionScraper(date).scrape(response_url, transaction_tag)
                    if transaction:
                        yield transaction

        return async_iter()
