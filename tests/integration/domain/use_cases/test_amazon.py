from http.cookiejar import MozillaCookieJar

import anyio
import pytest
from httpx import AsyncClient

from ynab_cli.adapters.amazon.client import AmazonBrowser, AmazonClient
from ynab_cli.domain.ports.io import StdIO


@pytest.mark.skipif(False, reason="Set to False if you want to debug amazon list transactions")
@pytest.mark.anyio
async def test_list_transactions() -> None:
    browser = AmazonBrowser(AsyncClient(cookies=MozillaCookieJar(filename=".amazon.cookies.txt")))

    client = AmazonClient(StdIO(), browser)

    async with client:
        try:
            transactions = client.get_transactions()
            async for transaction in transactions:
                print(transaction)
                break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    # This allows you to run the test by running this
    # script directly and debug it outside of pytest
    anyio.run(
        test_list_transactions,
        backend_options={"use_uvloop": True},
    )
