import asyncio
import os

import pytest

from ynab_cli.domain.ports.io import StdinIO
from ynab_cli.domain.settings import AmazonSettings, Settings
from ynab_cli.domain.use_cases import amazon


@pytest.mark.skipif(True, reason="Set to False if you want to debug amazon list transactions")
@pytest.mark.asyncio
async def test_list_transactions() -> None:
    amazon_username = os.environ["YNAB_CLI_AMAZON_USERNAME"]
    amazon_password = os.environ["YNAB_CLI_AMAZON_PASSWORD"]
    amazon_host = os.environ["YNAB_CLI_AMAZON_HOST"]

    io = StdinIO()

    settings = Settings(
        amazon=AmazonSettings(username=amazon_username, password=amazon_password, host=amazon_host),
    )

    async for transaction_group in amazon.list_transactions(settings, io, {}):
        assert transaction_group is not None


if __name__ == "__main__":
    # This allows you to run the test by running this
    # script directly and debug it outside of pytest
    asyncio.run(test_list_transactions())
