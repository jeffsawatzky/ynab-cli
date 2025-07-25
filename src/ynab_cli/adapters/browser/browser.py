import logging
from collections.abc import (
    AsyncGenerator,
    Mapping,
    Sequence,
)
from contextlib import asynccontextmanager
from http.cookiejar import FileCookieJar
from pathlib import Path
from types import TracebackType
from typing import Any

import anyio
from fake_useragent import UserAgent
from httpx import URL, AsyncClient, Response

from ynab_cli.adapters.browser.constants import DEFAULT_HEADERS, DEFAULT_SCHEME
from ynab_cli.adapters.browser.locale import HostLocaleInfo

log = logging.getLogger(__name__)


HeaderTypes = Mapping[str, str] | Mapping[bytes, bytes] | Sequence[tuple[str, str]] | Sequence[tuple[bytes, bytes]]


def absolute_url(host: str, url: URL | str, scheme: str = DEFAULT_SCHEME) -> URL:
    if isinstance(url, str):
        url = URL(url)

    log.debug(f"Resolving absolute URL: {url}")
    if not url.is_absolute_url or url.scheme == "":
        base_url_scheme = url.scheme or scheme
        base_url_host = url.host or host
        base_url = URL(scheme=base_url_scheme, host=base_url_host)
        url = base_url.join(url)

    log.debug(f"Resolved absolute URL: {url}")
    return url


class BrowserResponse:
    def __init__(self, response: Response) -> None:
        self._response = response

    @property
    def url(self) -> URL:
        return self._response.url

    async def read(self) -> bytes:
        return self._response.content

    async def text(self) -> str:
        return self._response.text


class Browser:
    """
    This is a simple browser abstraction that uses `httpx` to make requests.
    It will handle cookies and headers for you
    """

    def __init__(self, async_client: AsyncClient, default_host: str, host_locale_info: HostLocaleInfo) -> None:
        self._async_client = async_client
        self._default_host = default_host
        self._host_locale_info = host_locale_info
        self._user_agent = UserAgent(platforms="desktop").random

    async def __aenter__(self) -> "Browser":
        if isinstance(self._async_client.cookies.jar, FileCookieJar):
            try:
                self._async_client.cookies.jar.load()
            except Exception as e:
                log.warning(f"Failed to load cookies: {e}")

        await self._async_client.__aenter__()

        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        await self._async_client.__aexit__(exc_type, exc_val, exc_tb)

        if isinstance(self._async_client.cookies.jar, FileCookieJar):
            try:
                self._async_client.cookies.jar.save()
            except Exception as e:
                log.warning(f"Failed to save cookies: {e}")

        # Zero-sleep to allow underlying connections to close
        await anyio.sleep(0)

    def has_cookies(self, host: str, cookie_names: list[str], scheme: str = DEFAULT_SCHEME) -> bool:
        def find_cookie(cookie_name: str) -> bool:
            for cookie in self._async_client.cookies.jar:
                if cookie_name == cookie.name and host.endswith(cookie.domain) and cookie.secure == (scheme == "https"):
                    return True
            return False

        return all(find_cookie(cookie_name) for cookie_name in cookie_names)

    def load_cookies(self, cookies_path: Path) -> None:
        if isinstance(self._async_client.cookies.jar, FileCookieJar):
            try:
                self._async_client.cookies.jar.load(str(cookies_path.resolve()))
                log.debug(f"Cookies loaded from {cookies_path}")
            except Exception as e:
                log.warning(f"Failed to load cookies from {cookies_path}: {e}")

    @asynccontextmanager
    async def navigate(
        self,
        absolute_url: URL,
        method: str = "get",
        *,
        data: Mapping[str, Any] | None = None,
        referer: URL | None = None,
    ) -> AsyncGenerator[BrowserResponse, None]:
        if not absolute_url.is_absolute_url:
            raise ValueError("absolute_url must be absolute")

        headers: dict[str, str] = {}

        # Add dynamic default headers
        headers["User-Agent"] = self._user_agent
        host = absolute_url.host or self._default_host
        headers["Origin"] = f"{absolute_url.scheme}://{host}"
        if referer is not None:
            headers["Referer"] = str(referer)

        local_info = self._host_locale_info.get(host)
        if local_info is None:
            local_info = self._host_locale_info[self._default_host]
        accept_language = local_info["accept_language"]
        headers["Accept-Language"] = accept_language

        # Add static default headers
        for key, value in DEFAULT_HEADERS.items():
            if key not in headers:
                headers[key] = value

        async with self.fetch(method, absolute_url, data=data, headers=headers, follow_redirects=True) as response:
            yield response

    @asynccontextmanager
    async def fetch(
        self,
        method: str,
        absolute_url: URL,
        *,
        data: Mapping[str, Any] | None = None,
        headers: HeaderTypes | None = None,
        follow_redirects: bool = False,
    ) -> AsyncGenerator[BrowserResponse, None]:
        if not absolute_url.is_absolute_url:
            raise ValueError("absolute_url must be absolute")

        log.debug(f"Requesting {method.upper()}: `{absolute_url}`")

        response = await self._async_client.request(
            method, absolute_url, data=data, headers=headers, follow_redirects=follow_redirects
        )
        log.debug(f"{response.status_code}: {response.url}")
        if not response.url.is_absolute_url:
            raise ValueError("response.url must be absolute")

        yield BrowserResponse(response)
