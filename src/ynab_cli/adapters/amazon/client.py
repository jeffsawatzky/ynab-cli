import logging
from collections.abc import AsyncIterator
from types import TracebackType

from bs4 import BeautifulSoup
from httpx import URL, AsyncClient

from ynab_cli.adapters.amazon.constants import DEFAULT_AMAZON_HOST, Routes
from ynab_cli.adapters.amazon.errors import LoginError, NotFoundError
from ynab_cli.adapters.amazon.locale import HOST_LOCAL_INFO
from ynab_cli.adapters.amazon.models.order import Order
from ynab_cli.adapters.amazon.models.product import Product
from ynab_cli.adapters.amazon.models.refund import Refund
from ynab_cli.adapters.amazon.models.transaction import Transaction
from ynab_cli.adapters.amazon.scrapers.forms import PpwWidgetNextPageFormScraper
from ynab_cli.adapters.amazon.scrapers.order import OrderScraper
from ynab_cli.adapters.amazon.scrapers.product import ProductScraper
from ynab_cli.adapters.amazon.scrapers.refunds import RefundsScraper
from ynab_cli.adapters.amazon.scrapers.transactions import TransactionsScraper
from ynab_cli.adapters.browser.browser import Browser, absolute_url
from ynab_cli.adapters.browser.locale import HostLocaleInfo
from ynab_cli.domain.ports.io import IO

log = logging.getLogger(__name__)


class AmazonBrowser(Browser):
    """
    A specialized browser for Amazon that uses the default host and locale info.
    It inherits from the generic Browser class.
    """

    def __init__(
        self,
        async_client: AsyncClient,
        default_host: str = DEFAULT_AMAZON_HOST,
        host_local_info: HostLocaleInfo = HOST_LOCAL_INFO,
    ) -> None:
        super().__init__(async_client, default_host, host_local_info)


class AmazonClient:
    def __init__(self, io: IO, browser: AmazonBrowser, host: str = DEFAULT_AMAZON_HOST) -> None:
        self.io = io
        self.browser = browser
        self._host = host

    async def __aenter__(self) -> "AmazonClient":
        await self.browser.__aenter__()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        await self.browser.__aexit__(exc_type, exc_val, exc_tb)

    async def _request_cookies(self, host: str) -> None:
        host_cookies = await self.io.file(f"cookies.txt file for `{host}`")
        if host_cookies:
            log.info(f"Loading cookies from {host_cookies}")
            self.browser.load_cookies(host_cookies)

    async def is_logged_in(self, host: str) -> bool:
        required_cookies = ["session-token", "session-id"]
        has_cookies = self.browser.has_cookies(host, required_cookies)
        if not has_cookies:
            await self._request_cookies(host)
            has_cookies = self.browser.has_cookies(host, required_cookies)

        return has_cookies

    async def get_transactions(self) -> AsyncIterator[Transaction]:
        host = self._host

        if not await self.is_logged_in(host):
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
            request_url = absolute_url(host, URL(next_page_form.action))

            async with self.browser.navigate(
                request_url, method=next_page_form.method, data=next_page_form.data, referer=response_url
            ) as response:
                response_url = response.url
                text = await response.text()

    async def get_order_from_link(self, order_link: str) -> Order:
        order_url = URL(order_link)
        host = order_url.host or self._host

        if not await self.is_logged_in(host):
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
        product_url = URL(product_link)
        host = product_url.host or self._host

        if not await self.is_logged_in(host):
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
        refund_url = URL(refund_link)
        host = refund_url.host or self._host

        if not await self.is_logged_in(host):
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
