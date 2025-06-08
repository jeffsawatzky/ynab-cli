import anyio
import pytest

from ynab_cli.adapters.amazon.client import Client


@pytest.mark.skipif(True, reason="Set to False if you want to debug amazon list transactions")
@pytest.mark.anyio
async def test_list_transactions() -> None:
    client = Client()
    async with client:
        transactions = client.get_transactions()
        async for transaction in transactions:
            print(transaction)


if __name__ == "__main__":
    # This allows you to run the test by running this
    # script directly and debug it outside of pytest
    anyio.run(
        test_list_transactions,
        backend_options={"use_uvloop": True},
    )
