import logging
import re
from decimal import Decimal
from typing import ClassVar, Protocol, TypeVar, cast

from babel import numbers
from bs4 import Tag
from httpx import URL
from typing_extensions import override

import ynab_cli.adapters.browser.locale
from ynab_cli.adapters.amazon import locale
from ynab_cli.adapters.amazon.constants import DEFAULT_AMAZON_HOST
from ynab_cli.adapters.amazon.models.form import Form
from ynab_cli.adapters.browser.browser import Browser
from ynab_cli.domain.ports.io import IO

log = logging.getLogger(__name__)

M = TypeVar("M", covariant=True)
T = TypeVar("T")


class Scraper(Protocol[M]):
    async def scrape(self, response_url: URL, html: Tag) -> M: ...


class BaseScraper(Scraper[M]):
    def assert_host(self, url: URL) -> str:
        if not url.host:
            raise ValueError("No host found in response URL")
        return url.host

    def get_locale_info(self, host: str) -> ynab_cli.adapters.browser.locale.LocaleInfo:
        return locale.HOST_LOCAL_INFO.get(host, locale.HOST_LOCAL_INFO[DEFAULT_AMAZON_HOST])

    def get_locale(self, host: str) -> str:
        return self.get_locale_info(host)["locale"]

    def get_localized(self, response_url: URL, key: str, type: type[T]) -> T:
        return cast(T, locale.LOCALE[self.get_locale(self.assert_host(response_url))][key])

    def normalized_text(self, value: str | list[str] | None, whitespace: bool = False) -> str:
        if value is None:
            return ""
        if isinstance(value, list):
            value = " ".join(value)
        if whitespace:
            value = re.sub(r"\s+", " ", value).strip()

        return value

    def absolute_url(self, response_url: URL, url: str) -> str:
        u = URL(url)
        if not u.is_absolute_url or u.scheme == "":
            if not response_url.is_absolute_url or response_url.scheme == "":
                raise ValueError(f"Response URL needs to be absolute to build an absolute URL: {response_url}")
            u = response_url.join(u)

        return str(u)

    def parse_currency(self, response_url: URL, currency_host: str, value: str) -> Decimal:
        locale_host_local_info = self.get_locale_info(self.assert_host(response_url))
        currency_host_locale_info = self.get_locale_info(currency_host)

        decp = numbers.get_decimal_symbol(locale=locale_host_local_info["locale"])
        plus = numbers.get_plus_sign_symbol(locale=locale_host_local_info["locale"])
        minus = numbers.get_minus_sign_symbol(locale=locale_host_local_info["locale"])
        group = numbers.get_group_symbol(locale=locale_host_local_info["locale"])
        name = numbers.get_currency_name(
            currency_host_locale_info["currency"],
            locale=locale_host_local_info["locale"],
        )
        symbol = numbers.get_currency_symbol(
            currency_host_locale_info["currency"],
            locale=locale_host_local_info["locale"],
        )

        remove = [plus, name, symbol, group]
        for token in remove:
            # remove the pieces of information that shall be obvious
            value = re.sub(re.escape(token), "", value)
        # change the minus sign to a LOCALE=C minus
        value = re.sub(re.escape(minus), "-", value)
        # and change the decimal mark to a LOCALE=C decimal point
        value = re.sub(re.escape(decp), ".", value)
        # just in case remove extraneous spaces
        value = re.sub(r"\s+", "", value)
        return Decimal(value)

    def select(self, html: Tag, selectors: str | list[str]) -> list[Tag]:
        if isinstance(selectors, str):
            selectors = [selectors]

        for selector in selectors:
            tags = html.select(selector)
            if tags:
                return tags
        return []

    def select_one(self, html: Tag, selectors: str | list[str]) -> Tag | None:
        if isinstance(selectors, str):
            selectors = [selectors]

        for selector in selectors:
            tag = html.select_one(selector)
            if tag:
                return tag
        return None


class BaseFormScraper(BaseScraper[Form | None]):
    FORM_SELECTOR: ClassVar[str] = ""
    SUBMIT_SELECTOR: ClassVar[str] = ""

    def __init__(self, browser: Browser, io: IO) -> None:
        self._browser = browser
        self._io = io

    @override
    async def scrape(self, response_url: URL, html: Tag) -> Form | None:
        form_tag = await self._find_form_tag(html)
        if not form_tag:
            log.warning("No form found")
            return None
        action, method, data = await self._parse_form_tag(response_url, form_tag, {})

        if self.__class__.SUBMIT_SELECTOR:
            submit_tag = await self._find_submit_tag(form_tag)
            if not submit_tag:
                log.warning("No submit button found")
                return None
            data = await self._parse_submit_tag(submit_tag, data)

        return Form(action=action, method=method, data=data)

    async def _find_form_tag(self, html: Tag) -> Tag | None:
        form_tag = html.select_one(self.__class__.FORM_SELECTOR)
        if not form_tag:
            return None
        return form_tag

    async def _find_submit_tag(self, form_tag: Tag) -> Tag | None:
        submit_tag = form_tag.select_one(self.__class__.SUBMIT_SELECTOR)
        if not submit_tag:
            return None
        return submit_tag

    async def _parse_form_tag(
        self, response_url: URL, form_tag: Tag, data: dict[str, str]
    ) -> tuple[str, str, dict[str, str]]:
        action = self.absolute_url(response_url, self.normalized_text(form_tag.get("action", "/")))
        method = self.normalized_text(form_tag.get("method", "post"))

        input_tags = form_tag.select("input")
        data.update(
            {
                self.normalized_text(tag.get("name")): self.normalized_text(tag.get("value", ""))
                for tag in input_tags
                if tag.get("name") and self.normalized_text(tag.get("type")) != "submit"
            }
        )

        return (action, method, data)

    async def _parse_submit_tag(self, submit_tag: Tag, data: dict[str, str]) -> dict[str, str]:
        data[self.normalized_text(submit_tag.get("name"))] = self.normalized_text(submit_tag.get("value", ""))
        return data
