import logging
from collections.abc import AsyncIterator
from types import TracebackType

from bs4 import BeautifulSoup
from yarl import URL

from ynab_cli.adapters.amazon.auth_flow import AuthFlow
from ynab_cli.adapters.amazon.browser import Browser, absolute_url
from ynab_cli.adapters.amazon.constants import DEFAULT_AMAZON_HOST, Routes
from ynab_cli.adapters.amazon.errors import LoginError, NotFoundError
from ynab_cli.adapters.amazon.models.order import Order
from ynab_cli.adapters.amazon.models.product import Product
from ynab_cli.adapters.amazon.models.refund import Refund
from ynab_cli.adapters.amazon.models.transaction import Transaction
from ynab_cli.adapters.amazon.scrapers.forms import PpwWidgetNextPageFormScraper
from ynab_cli.adapters.amazon.scrapers.order import OrderScraper
from ynab_cli.adapters.amazon.scrapers.product import ProductScraper
from ynab_cli.adapters.amazon.scrapers.refunds import RefundsScraper
from ynab_cli.adapters.amazon.scrapers.transactions import TransactionsScraper
from ynab_cli.domain.ports.io import IO, StdinIO

log = logging.getLogger(__name__)


class Client:
    def __init__(
        self,
        username: str,
        password: str,
        host: str = DEFAULT_AMAZON_HOST,
        io: IO | None = None,
        browser: Browser | None = None,
    ) -> None:
        if io is None:
            io = StdinIO()
        self.io = io

        if browser is None:
            browser = Browser()
        self.browser = browser

        self._host = host

        self._auth_flow = AuthFlow(username, password, self)

    async def __aenter__(self) -> "Client":
        await self.browser.__aenter__()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        await self.browser.__aexit__(exc_type, exc_val, exc_tb)

    async def is_logged_in(self, host: str) -> bool:
        return self.browser.has_cookies(host, ["session-token", "session-id"])

    async def get_transactions(self) -> AsyncIterator[Transaction]:
        host = self._host

        if not await self.is_logged_in(host):
            if not await self._auth_flow.login(host):
                raise LoginError(f"Could not login to {host}")

        request_url = absolute_url(host, Routes.TRANSACTIONS)
        response_url = None

        async with self.browser.navigate(request_url) as response:
            response_url = response.url
            text = await response.text()

        next_page_scraper = PpwWidgetNextPageFormScraper(self.browser, self.io)
        transactions_scraper = TransactionsScraper()

        while True:
            html = BeautifulSoup(text, "html.parser")
            transactions = await transactions_scraper.scrape(response_url, html)
            async for transaction in transactions:
                yield transaction

            next_page_form = await next_page_scraper.scrape(response_url, html)
            if not next_page_form:
                break

            host = response_url.host or self._host
            request_url = absolute_url(host, URL(next_page_form.action, encoded=True))

            async with self.browser.navigate(
                request_url, method=next_page_form.method, data=next_page_form.data, referer=response_url
            ) as response:
                response_url = response.url
                text = await response.text()

    async def get_order_from_link(self, order_link: str) -> Order:
        order_url = URL(order_link, encoded=True)
        host = order_url.host or self._host

        if not await self.is_logged_in(host):
            if not await self._auth_flow.login(host):
                raise LoginError(f"Could not login to {host}")

        request_url = absolute_url(host, order_url)
        response_url = None

        async with self.browser.navigate(request_url) as response:
            response_url = response.url
            text = await response.text()

        order_scraper = OrderScraper()
        html = BeautifulSoup(text, "html.parser")
        order = await order_scraper.scrape(response_url, html)

        if not order:
            raise NotFoundError(f"Could not scrape order from {order_url}")

        return order

    async def get_product_from_link(self, product_link: str) -> Product:
        product_url = URL(product_link, encoded=True)
        host = product_url.host or self._host

        if not await self.is_logged_in(host):
            if not await self._auth_flow.login(host):
                raise LoginError(f"Could not login to {host}")

        request_url = absolute_url(host, product_url)
        response_url = None

        async with self.browser.navigate(request_url) as response:
            response_url = response.url
            text = await response.text()

        product_scraper = ProductScraper()
        html = BeautifulSoup(text, "html.parser")
        product = await product_scraper.scrape(response_url, html)

        if not product:
            raise NotFoundError(f"Could not scrape product from {product_url}")

        return product

    async def get_refunds_from_link(self, refund_link: str) -> AsyncIterator[Refund]:
        refund_url = URL(refund_link, encoded=True)
        host = refund_url.host or self._host

        if not await self.is_logged_in(host):
            if not await self._auth_flow.login(host):
                raise LoginError(f"Could not login to {host}")

        request_url = absolute_url(host, refund_url)
        response_url = None

        async with self.browser.navigate(request_url) as response:
            response_url = response.url
            text = await response.text()

        refunds_scraper = RefundsScraper()
        html = BeautifulSoup(text, "html.parser")
        refunds = await refunds_scraper.scrape(response_url, html)

        async for refund in refunds:
            yield refund
