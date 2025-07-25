from datetime import date
from decimal import Decimal

import pytest
from bs4 import BeautifulSoup
from httpx import URL

from ynab_cli.adapters.amazon.scrapers.refund import RefundScraper


@pytest.mark.anyio
async def test_scrape__success() -> None:
    # GIVEN
    fixture = TEST_PARSE_REFUND_HTML
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = RefundScraper("123-4567890-1234567", "B0BC1984LV")
    refund = await sut.scrape(URL("https://www.amazon.ca"), html)

    # THEN
    assert refund is not None
    assert refund.order_id == "123-4567890-1234567"
    assert refund.product_id == "B0BC1984LV"
    assert refund.refund_total == Decimal("12.76")
    assert refund.refund_date == date(2024, 10, 29)


TEST_PARSE_REFUND_HTML = """
<div id="jhlmlphmrrluump-Qvrt8b9BY-consumed-orc-item" data-item-key="jhlmlphmrrluump-Qvrt8b9BY-consumed" data-should-preselect-item="false" class="a-section orc-item">
  <div class="a-row">
    <div class="a-column a-span1"></div>
    <div data-item-key="jhlmlphmrrluump-Qvrt8b9BY-consumed" class="a-column a-span6">
      <div class="a-row a-grid-vertical-align a-grid-center">
        <div class="a-column a-span3">
          <div class="a-section a-padding-mini a-text-center">
            <div class="a-row">
              <img alt="" src="https://m.media-amazon.com/images/I/41H18FHAROL._AC_._SS160_.jpg">
            </div>
            <div class="a-row">
              <span class="a-declarative" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;closeButton&quot;:&quot;true&quot;,&quot;dataStrategy&quot;:&quot;preload&quot;,&quot;activate&quot;:&quot;onmouseover&quot;,&quot;name&quot;:&quot;jhlmlphmrrluump-Qvrt8b9BY-consumed-itemDetails-popover&quot;,&quot;header&quot;:&quot;&quot;,&quot;position&quot;:&quot;triggerTop&quot;,&quot;popoverLabel&quot;:&quot;Details&quot;,&quot;url&quot;:&quot;&quot;}" data-csa-c-id="v045cx-u3j9kz-e394iu-zieeid">
                <a href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative">
                  <span aria-label="Product details for Choker Necklace for Women Layered Gold..." class="a-size-small"> Details </span>
                  <i class="a-icon a-icon-popover"></i>
                </a>
              </span>
            </div>
          </div>
        </div>
        <div class="a-column a-span8 a-spacing-top-small a-span-last">
          <div class="a-row">
            <span class="a-size-base a-text-bold"> Choker Necklace for Women Layered Gold... </span>
          </div>
          <div class="a-row">
            <span class="a-size-small"> Colour: </span>
            <span class="a-size-small"> B:silver Coin Necklace </span>
          </div>
          <div class="a-row">
            <span class="a-size-small"> $11.29 </span>
          </div>
          <div class="a-row"></div>
        </div>
      </div>
    </div>
    <div class="a-column a-span5 a-span-last">
      <div id="consumed-unit-spinner" class="a-section a-padding-medium a-text-center aok-hidden">
        <span class="a-spinner a-spinner-medium"></span>
      </div>
      <div id="consumed-unit-section" class="a-section">
        <div class="a-box a-alert-inline a-alert-inline-success" aria-live="polite" aria-atomic="true">
          <div class="a-box-inner a-alert-container">
            <i class="a-icon a-icon-alert"></i>
            <div class="a-alert-content">
              <span class="a-size-base a-text-bold"> Refund issued </span>
              <ul class="a-unordered-list a-nostyle a-vertical a-spacing-micro">
                <li>
                  <span class="a-list-item">
                    <div class="a-section a-spacing-micro a-text-left">
                      <span class="a-size-small a-color-secondary">
                        <b>
                          <font color="#008500">$12.76</font>
                        </b> refund issued on Oct 29, 2024. </span>
                    </div>
                  </span>
                </li>
                <li>
                  <span class="a-list-item">
                    <div class="a-section a-spacing-micro a-text-left">
                      <span class="a-size-small a-color-secondary"> Return received on: Nov 2, 2024 </span>
                    </div>
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <hr aria-hidden="true" class="a-spacing-top-large a-divider-normal">
</div>
"""
