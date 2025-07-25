from datetime import date

import pytest
from bs4 import BeautifulSoup
from httpx import URL

from ynab_cli.adapters.amazon.scrapers.transaction import TransactionScraper


@pytest.mark.anyio
async def test_scrape__success() -> None:
    # GIVEN
    fixture = """
<div class="a-section a-spacing-base apx-transactions-line-item-component-container">
    <div data-pmts-component-id="pp-YMKD22-4" class="a-row pmts-portal-component pmts-portal-components-pp-YMKD22-4">
        <div class="a-column a-span9"><span class="a-size-base a-text-bold">Visa ****1234</span></div>
        <div class="a-column a-span3 a-text-right a-span-last"><span class="a-size-base-plus a-text-bold">-$20.50</span>
        </div>
    </div>
    <div data-pmts-component-id="pp-YMKD22-4"
        class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-YMKD22-4">
        <div class="a-row">
            <div class="a-column a-span12"><a id="pp-YMKD22-51" class="a-link-normal"
                    href="https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567">Order
                    #123-4567890-1234567</a></div>
        </div>
    </div>
    <div data-pmts-component-id="pp-YMKD22-4"
        class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-YMKD22-4">
        <div class="a-row">
            <div class="a-column a-span12"><span class="a-size-base">AMZN Mktp CA</span></div>
        </div>
    </div>
</div>
"""
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = TransactionScraper(date(2024, 1, 1))
    transaction = await sut.scrape(URL("https://www.amazon.ca"), html)

    # THEN
    assert transaction is not None
    assert transaction.completed_date == date(2024, 1, 1)
    assert transaction.payment_method == "Visa ****1234"
    assert transaction.order_link == "https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567"
    assert transaction.order_id == "123-4567890-1234567"
    assert transaction.grand_total == 20.50
    assert transaction.seller == "AMZN Mktp CA"
    assert transaction.is_refund is False
    assert transaction.is_gift_card is False


@pytest.mark.anyio
async def test_scrape__success_order_link_relative() -> None:
    # GIVEN
    fixture = """
<div class="a-section a-spacing-base apx-transactions-line-item-component-container">
    <div data-pmts-component-id="pp-YMKD22-4" class="a-row pmts-portal-component pmts-portal-components-pp-YMKD22-4">
        <div class="a-column a-span9"><span class="a-size-base a-text-bold">Visa ****1234</span></div>
        <div class="a-column a-span3 a-text-right a-span-last"><span class="a-size-base-plus a-text-bold">-$20.50</span>
        </div>
    </div>
    <div data-pmts-component-id="pp-YMKD22-4"
        class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-YMKD22-4">
        <div class="a-row">
            <div class="a-column a-span12"><a id="pp-YMKD22-51" class="a-link-normal"
                    href="/gp/css/summary/edit.html?orderID=123-4567890-1234567">Order
                    #123-4567890-1234567</a></div>
        </div>
    </div>
    <div data-pmts-component-id="pp-YMKD22-4"
        class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-YMKD22-4">
        <div class="a-row">
            <div class="a-column a-span12"><span class="a-size-base">AMZN Mktp CA</span></div>
        </div>
    </div>
</div>
"""

    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = TransactionScraper(date(2024, 1, 1))
    transaction = await sut.scrape(URL("https://www.amazon.ca"), html)

    # THEN
    assert transaction is not None
    assert transaction.completed_date == date(2024, 1, 1)
    assert transaction.payment_method == "Visa ****1234"
    assert transaction.order_link == "https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567"
    assert transaction.order_id == "123-4567890-1234567"
    assert transaction.grand_total == 20.50
    assert transaction.seller == "AMZN Mktp CA"
    assert transaction.is_refund is False
    assert transaction.is_gift_card is False


@pytest.mark.anyio
async def test_scrape__success_order_link_localized() -> None:
    # GIVEN
    fixture = """
<div class="a-section a-spacing-base apx-transactions-line-item-component-container">
    <div data-pmts-component-id="pp-QjPJkd-4" class="a-row pmts-portal-component pmts-portal-components-pp-QjPJkd-4">
        <div class="a-column a-span9"><span class="a-size-base a-text-bold">Visa ****1234</span></div>
        <div class="a-column a-span3 a-text-right a-span-last"><span
                class="a-size-base-plus a-text-bold">-CA$20.50</span></div>
    </div>
    <div data-pmts-component-id="pp-QjPJkd-4"
        class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-QjPJkd-4">
        <div class="a-row">
            <div class="a-column a-span12"><a id="pp-QjPJkd-51" class="a-link-normal"
                    href="https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567">Order
                    #123-4567890-1234567</a></div>
        </div>
    </div>
    <div data-pmts-component-id="pp-QjPJkd-4"
        class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-QjPJkd-4">
        <div class="a-row">
            <div class="a-column a-span12"><span class="a-size-base">AMZN Mktp CA</span></div>
        </div>
    </div>
</div>
"""

    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = TransactionScraper(date(2024, 1, 1))
    transaction = await sut.scrape(URL("https://www.amazon.com"), html)

    # THEN
    assert transaction is not None
    assert transaction.completed_date == date(2024, 1, 1)
    assert transaction.payment_method == "Visa ****1234"
    assert transaction.order_link == "https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567"
    assert transaction.order_id == "123-4567890-1234567"
    assert transaction.grand_total == 20.50
    assert transaction.seller == "AMZN Mktp CA"
    assert transaction.is_refund is False
    assert transaction.is_gift_card is False
