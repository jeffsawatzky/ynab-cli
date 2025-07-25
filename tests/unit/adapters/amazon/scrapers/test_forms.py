from unittest.mock import MagicMock

import pytest
from bs4 import BeautifulSoup
from httpx import URL

from tests import fixture_exists, load_fixture
from ynab_cli.adapters.amazon.models.form import Form
from ynab_cli.adapters.amazon.scrapers.forms import (
    PpwWidgetNextPageFormScraper,
)
from ynab_cli.adapters.browser.browser import Browser
from ynab_cli.domain.ports.io import IO


@pytest.mark.skipif(
    not fixture_exists("adapters/amazon/pages/amazon_cpe_yourpayments_transactions.html"),
    reason="Skipped, to debug the transactions next page form, place it at tests/fixtures/adapters/amazon/pages/amazon_cpe_yourpayments_transactions.html",
)
@pytest.mark.anyio
async def test_ppw_widget_next_page_form_scraper__success() -> None:
    # Given
    mock_browser = MagicMock(spec=Browser)
    mock_io = MagicMock(spec=IO)

    fixture = load_fixture("adapters/amazon/pages/amazon_cpe_yourpayments_transactions.html")
    html = BeautifulSoup(fixture, "html.parser")

    # When
    sut = PpwWidgetNextPageFormScraper(mock_browser, mock_io)
    form = await sut.scrape(URL("https://www.amazon.com"), html)

    # Then
    assert form is not None
    assert form == Form(
        action="https://www.amazon.ca/cpe/yourpayments/transactions",
        method="post",
        data={
            "ppw-widgetState": "dsfgefwc2938r793nyr49cybn",
            "ie": "UTF-8",
            'ppw-widgetEvent:DefaultNextPageNavigationEvent:{"nextPageKey":"skjdfh"}': "",
        },
    )
