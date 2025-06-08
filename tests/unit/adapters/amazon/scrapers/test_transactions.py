import datetime
from decimal import Decimal

import pytest
from bs4 import BeautifulSoup
from httpx import URL

from ynab_cli.adapters.amazon.scrapers.transactions import TransactionsScraper


@pytest.mark.anyio
async def test_scrape__success() -> None:
    # GIVEN
    fixture = TEST_PARSE_TRANSACTIONS_HTML
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = TransactionsScraper()
    transactions = []
    async_iter = await sut.scrape(URL("https://www.amazon.com"), html)
    async for transaction in async_iter:
        transactions.append(transaction)

    # THEN
    assert len(transactions) == 2
    assert transactions[0].completed_date == datetime.date(2024, 10, 11)
    assert transactions[0].payment_method == "Visa ****1234"
    assert transactions[0].order_link == "https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567"
    assert transactions[0].order_id == "123-4567890-1234567"
    assert transactions[0].grand_total == Decimal("45.19")
    assert transactions[0].seller == "AMZN Mktp CA"
    assert transactions[0].is_refund is False
    assert transactions[0].is_gift_card is False
    assert transactions[1].completed_date == datetime.date(2024, 10, 9)
    assert transactions[1].payment_method == "Mastercard ****1234"
    assert transactions[1].order_link == "https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567"
    assert transactions[1].order_id == "123-4567890-1234567"
    assert transactions[1].grand_total == Decimal("28.79")
    assert transactions[1].seller == "Amazon.ca"
    assert transactions[1].is_refund is True
    assert transactions[1].is_gift_card is False


TEST_PARSE_TRANSACTIONS_HTML = """
<form action="https://www.amazon.com:443/cpe/yourpayments/transactions" class="a-spacing-none" method="post"><input
        name="ppw-widgetState" type="hidden" value="the-ppw-widgetState" /><input name="ie" type="hidden"
        value="UTF-8" />
    <div class="a-box-group a-spacing-base">
        <div class="a-box a-spacing-none a-box-title apx-transactions-sleeve-header-container">
            <div class="a-box-inner a-padding-base"><span class="a-size-base a-text-bold">Completed</span></div>
        </div>
        <div class="a-box a-spacing-base">
            <div class="a-box-inner a-padding-none">
                <div class="a-section a-spacing-base a-padding-base apx-transaction-date-container pmts-portal-component pmts-portal-components-pp-kXMaEm-3"
                    data-pmts-component-id="pp-kXMaEm-3"><span>October 11, 2024</span></div>
                <div class="a-section a-spacing-base pmts-portal-component pmts-portal-components-pp-kXMaEm-3"
                    data-pmts-component-id="pp-kXMaEm-3">
                    <div class="a-section a-spacing-base apx-transactions-line-item-component-container">
                        <div class="a-row pmts-portal-component pmts-portal-components-pp-kXMaEm-4"
                            data-pmts-component-id="pp-kXMaEm-4">
                            <div class="a-column a-span9"><span class="a-size-base a-text-bold">Visa ****1234</span>
                            </div>
                            <div class="a-column a-span3 a-text-right a-span-last"><span
                                    class="a-size-base-plus a-text-bold">-CA$45.19</span></div>
                        </div>
                        <div class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-kXMaEm-4"
                            data-pmts-component-id="pp-kXMaEm-4">
                            <div class="a-row">
                                <div class="a-column a-span12"><a class="a-link-normal"
                                        href="https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567"
                                        id="pp-kXMaEm-50">Order #123-4567890-1234567</a></div>
                            </div>
                        </div>
                        <div class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-kXMaEm-4"
                            data-pmts-component-id="pp-kXMaEm-4">
                            <div class="a-row">
                                <div class="a-column a-span12"><span class="a-size-base">AMZN Mktp CA</span></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="a-section a-spacing-base a-padding-base apx-transaction-date-container pmts-portal-component pmts-portal-components-pp-kXMaEm-8"
                    data-pmts-component-id="pp-kXMaEm-8"><span>October 9, 2024</span></div>
                <div class="a-section a-spacing-base pmts-portal-component pmts-portal-components-pp-kXMaEm-8"
                    data-pmts-component-id="pp-kXMaEm-8">
                    <div class="a-section a-spacing-base apx-transactions-line-item-component-container">
                        <div class="a-row pmts-portal-component pmts-portal-components-pp-kXMaEm-9"
                            data-pmts-component-id="pp-kXMaEm-9">
                            <div class="a-column a-span9"><span class="a-size-base a-text-bold">Mastercard
                                    ****1234</span></div>
                            <div class="a-column a-span3 a-text-right a-span-last"><span
                                    class="a-size-base-plus a-text-bold">+CA$28.79</span></div>
                        </div>
                        <div class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-kXMaEm-9"
                            data-pmts-component-id="pp-kXMaEm-9">
                            <div class="a-row">
                                <div class="a-column a-span12"><a class="a-link-normal"
                                        href="https://www.amazon.ca/gp/css/summary/edit.html?orderID=123-4567890-1234567"
                                        id="pp-kXMaEm-52">Refund: Order #123-4567890-1234567</a></div>
                            </div>
                        </div>
                        <div class="a-section a-spacing-none a-spacing-top-mini pmts-portal-component pmts-portal-components-pp-kXMaEm-9"
                            data-pmts-component-id="pp-kXMaEm-9">
                            <div class="a-row">
                                <div class="a-column a-span12"><span class="a-size-base">Amazon.ca</span></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="a-row a-spacing-top-extra-large">
        <div class="a-column a-span2 a-text-center"><span class="a-button a-button-span12 a-button-base"><span
                    class="a-button-inner"><input class="a-button-input"
                        name='ppw-widgetEvent:DefaultPreviousPageNavigationEvent:{"previousPageKey":"key"}'
                        type="submit" /><span aria-hidden="true" class="a-button-text">Previous
                        Page</span></span></span></div>
        <div class="a-column a-span2 a-text-center a-span-last"><span
                class="a-button a-button-span12 a-button-base"><span class="a-button-inner"><input
                        class="a-button-input"
                        name='ppw-widgetEvent:DefaultNextPageNavigationEvent:{"nextPageKey":"key"}'
                        type="submit" /><span aria-hidden="true" class="a-button-text">Next Page</span></span></span>
        </div>
    </div>
</form>
"""
