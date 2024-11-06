import asyncio
import logging
import secrets
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from yarl import URL

from ynab_cli.adapters.amazon.browser import absolute_url
from ynab_cli.adapters.amazon.constants import Routes
from ynab_cli.adapters.amazon.scrapers.base import BaseFormScraper
from ynab_cli.adapters.amazon.scrapers.forms import (
    CfvRequestCaptchaFormScraper,
    SignInCaptchaFormScraper,
    SignInFormScraper,
)

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import Client

log = logging.getLogger(__name__)


class AuthFlow:
    def __init__(self, username: str, password: str, client: "Client") -> None:
        self._client = client

        self._auth_form_scrapers: list[BaseFormScraper] = [
            SignInFormScraper(username, password, client.browser, client.io),
            SignInCaptchaFormScraper(client.browser, client.io),
            CfvRequestCaptchaFormScraper(client.browser, client.io),
        ]

    async def _is_logged_in(self, host: str, response_url: URL) -> bool:
        if await self._client.is_logged_in(host) and response_url.path == Routes.TRANSACTIONS.path:
            return True
        return False

    async def login(self, host: str) -> bool:
        attempt = 1
        while attempt < 4:
            log.debug(f"Login attempt {attempt}")
            if await self._login(host):
                return True
            attempt += 1
            await asyncio.sleep(1)
        return False

    async def _login(self, host: str) -> bool:
        log.debug(f"Logging in to {host}")

        response_url = absolute_url(host, Routes.SIGN_IN_REFERER)
        request_url = absolute_url(host, Routes.SIGN_IN)
        cache_break = str(secrets.randbelow(10000000000000000))
        request_url = request_url.extend_query({cache_break: cache_break})

        async with self._client.browser.navigate(request_url, referer=response_url) as response:
            response_url = response.url
            if await self._is_logged_in(host, response_url):
                return True

            text = await response.text()

        while not await self._is_logged_in(host, response_url):
            html = BeautifulSoup(text, "html.parser")
            for form_scraper in self._auth_form_scrapers:
                log.debug(f"Trying {form_scraper.__class__.__name__}")
                form = await form_scraper.scrape(response_url, html)
                if form:
                    log.debug(f"Submitting {form_scraper.__class__.__name__}")

                    request_url = absolute_url(host, URL(form.action, encoded=True))
                    async with self._client.browser.navigate(
                        request_url, method=form.method, data=form.data, referer=response_url
                    ) as response:
                        response_url = response.url
                        if await self._is_logged_in(host, response_url):
                            return True

                        text = await response.text()
                    break
            else:
                log.warning("Could not find a form to submit")
                break

        return False
