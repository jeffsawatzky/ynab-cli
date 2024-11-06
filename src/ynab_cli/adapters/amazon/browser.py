import asyncio
import logging
from collections.abc import AsyncGenerator, Iterable
from contextlib import asynccontextmanager
from types import TracebackType
from typing import Any, TypeAlias, TypedDict, Unpack

from aiohttp import ClientResponse, ClientSession
from aiohttp_client_cache.backends.base import CacheBackend
from aiohttp_client_cache.session import CachedSession
from multidict import CIMultiDict
from yarl import URL

from ynab_cli.adapters.amazon.constants import DEFAULT_AMAZON_HOST, DEFAULT_AMAZON_SCHEME, DEFAULT_HEADERS
from ynab_cli.adapters.amazon.locale import HOST_LOCAL_INFO

log = logging.getLogger(__name__)

LooseHeaders: TypeAlias = dict[str, str] | CIMultiDict[str] | Iterable[tuple[str, str]]


def absolute_url(host: str, url: URL | str, scheme: str = DEFAULT_AMAZON_SCHEME) -> URL:
    if isinstance(url, str):
        url = URL(url, encoded=True)

    log.debug(f"Resolving absolute URL: {url}")
    if not url.absolute or url.scheme == "":
        base_url_scheme = url.scheme or scheme
        base_url_host = url.host or host
        base_url = URL.build(scheme=base_url_scheme, host=base_url_host, encoded=True)
        url = base_url.join(url)

    log.debug(f"Resolved absolute URL: {url}")
    return url


class RequestOptions(TypedDict, total=False):
    data: Any
    headers: LooseHeaders
    allow_redirects: bool
    max_redirects: int


class BrowserResponse:
    def __init__(self, response: ClientResponse) -> None:
        self._response = response

    @property
    def url(self) -> URL:
        return self._response.url

    async def read(self) -> bytes:
        return await self._response.read()

    async def text(self) -> str:
        return await self._response.text()


class Browser:
    """
    This is a simple browser abstraction that uses `aiohttp` to make requests.
    It will handle cookies and headers for you
    """

    def __init__(self, client_session: ClientSession | None = None) -> None:
        if client_session is None:
            client_session = CachedSession(
                cache=CacheBackend(),
            )
            client_session = ClientSession()

        self._client_session = client_session

    async def __aenter__(self) -> "Browser":
        await self._client_session.__aenter__()

        # Warm up the client session
        async with self._client_session.get(URL(f"{DEFAULT_AMAZON_SCHEME}://{DEFAULT_AMAZON_HOST}")) as response:
            log.debug(f"Initial request: {response.status}")

        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        await self._client_session.__aexit__(exc_type, exc_val, exc_tb)
        # Zero-sleep to allow underlying connections to close
        await asyncio.sleep(0)

    def has_cookies(self, host: str, cookie_names: list[str], scheme: str = DEFAULT_AMAZON_SCHEME) -> bool:
        cookies = self._client_session.cookie_jar.filter_cookies(URL.build(scheme=scheme, host=host))
        for cookie_name in cookie_names:
            if not cookies.get(cookie_name):
                return False
        return True

    @asynccontextmanager
    async def navigate(
        self,
        absolute_url: URL,
        method: str = "get",
        referer: URL | None = None,
        **kwargs: Unpack[RequestOptions],
    ) -> AsyncGenerator[BrowserResponse, None]:
        if not absolute_url.absolute:
            raise ValueError("absolute_url must be absolute")

        updated_headers: CIMultiDict[str] = CIMultiDict()
        if "headers" in kwargs:
            headers = kwargs["headers"]
            if isinstance(headers, dict | CIMultiDict):
                headers = headers.items()

            for key, value in headers:
                updated_headers.add(key, value)

        # Add dynamic default headers
        host = absolute_url.host or DEFAULT_AMAZON_HOST
        if "Origin" not in updated_headers:
            updated_headers.add("Origin", f"{absolute_url.scheme}://{host}")

        if referer is not None:
            updated_headers.add("Referer", str(referer))

        if "Accept-Language" not in updated_headers:
            local_info = HOST_LOCAL_INFO.get(host)
            if local_info is None:
                local_info = HOST_LOCAL_INFO[DEFAULT_AMAZON_HOST]
            accept_language = local_info["accept_language"]

            updated_headers.add("Accept-Language", accept_language)

        # Add static default headers
        for key, value in DEFAULT_HEADERS.items():
            if key not in updated_headers:
                updated_headers.add(key, value)

        kwargs["headers"] = updated_headers

        async with self.fetch(method, absolute_url, **kwargs) as response:
            yield response

    @asynccontextmanager
    async def fetch(
        self, method: str, absolute_url: URL, **kwargs: Unpack[RequestOptions]
    ) -> AsyncGenerator[BrowserResponse, None]:
        if not absolute_url.absolute:
            raise ValueError("absolute_url must be absolute")

        log.debug(f"Requesting {method.upper()}: `{absolute_url}`")

        async with self._client_session.request(method, absolute_url, **kwargs) as response:
            log.debug(f"{response.status}: {response.url}")
            if not response.url.absolute:
                raise ValueError("response.url must be absolute")

            yield BrowserResponse(response)
