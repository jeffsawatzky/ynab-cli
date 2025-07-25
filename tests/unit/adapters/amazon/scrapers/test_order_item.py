from decimal import Decimal

import pytest
from bs4 import BeautifulSoup
from httpx import URL

from ynab_cli.adapters.amazon.scrapers.order_item import OrderItemScraper


@pytest.mark.anyio
async def test_scrape__success_style_1() -> None:
    # GIVEN
    fixture = """
<div class="a-fixed-left-grid">
  <div class="a-fixed-left-grid-inner" style="padding-left:100px">
    <div class="" data-component="purchasedItemsLeftGrid">
      <div class="a-fixed-left-grid-col a-col-left" style="width:100px;margin-left:-100px;float:left;">
        <div class="" data-component="itemImage">
          <div style="position: relative">
            <a class="a-link-normal" href="/dp/B07KF6SSFF?ref_=ppx_hzod_image_dt_b_fed_asin_title_0_0">
              <img alt="Colgate MaxFresh Knockout Breath Freshening Toothpaste, 150 Milliliters" src="https://m.media-amazon.com/images/I/61gfCwth7CL._SS284_.jpg" height="90" width="90" data-a-hires="https://m.media-amazon.com/images/I/61gfCwth7CL._SS568_.jpg">
            </a>
            <div class="od-item-view-qty">
              <span> 2 </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="" data-component="purchasedItemsRightGrid">
      <div class="a-fixed-left-grid-col a-col-right" style="padding-left:1.5%;float:left;">
        <div class="" data-component="itemTitle">
          <div class="a-row">
            <a class="a-link-normal" href="/dp/B07KF6SSFF?ref_=ppx_hzod_title_dt_b_fed_asin_title_0_0">Colgate MaxFresh Knockout Breath Freshening Toothpaste, 150 Milliliters</a>
          </div>
        </div>
        <div class="" data-component="orderedMerchant">
          <span class="a-size-small a-color-secondary">Sold by: Amazon.ca</span>
        </div>
        <div class="" data-component="itemReturnEligibility">
          <div class="a-row">
            <span class="a-size-small">Return or replace items: Eligible through November 21, 2024</span>
          </div>
        </div>
        <div class="" data-component="unitPrice">
          <span class="a-price a-text-price" data-a-size="s" data-a-color="base">
            <span class="a-offscreen">$2.97</span>
            <span aria-hidden="true">$2.97</span>
          </span>
        </div>
        <div class="" data-component="deliveryFrequency"></div>
        <div class="" data-component="customizedItemDetails"></div>
        <div class="" data-component="itemConnections">
          <div class="a-row a-spacing-top-mini">
            <span class="a-button a-button-normal a-spacing-mini a-button-primary" id="a-autoid-0">
              <span class="a-button-inner">
                <a href="/gp/buyagain?ats=eyJjdXN0b21lcklkIjoiQVVKQUoxMDRXTFpQMyIsImV4cGxpY2l0Q2FuZGlkYXRlcyI6IkIwN0tGNlNTRkYifQ%3D%3D&amp;ref_=ppx_hzod_itemconns_dt_b_bia_item_0_0" class="a-button-text" id="a-autoid-0-announce">
                  <div class="od-buy-it-again-button__icon"></div>
                  <div class="od-buy-it-again-button__text">Buy it again</div>
                </a>
              </span>
            </span>
            <span class="a-button a-button-normal a-spacing-mini a-button-base" id="a-autoid-1">
              <span class="a-button-inner">
                <a href="/your-orders/pop?orderId=702-0148470-4601048&amp;shipmentId=QBNS1vYHy&amp;lineItemId=jhljsokonorvxsps&amp;packageId=1&amp;asin=B07KF6SSFF&amp;ref_=ppx_hzod_itemconns_dt_b_pop_0_0" class="a-button-text" id="a-autoid-1-announce"> View your item </a>
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = OrderItemScraper(order_id="123-4567890-1234567")
    order_item = await sut.scrape(URL("https://www.amazon.ca"), html)

    # THEN
    assert order_item is not None
    assert order_item.order_id == "123-4567890-1234567"
    assert order_item.product_id == "B07KF6SSFF"
    assert order_item.product_link == "https://www.amazon.ca/dp/B07KF6SSFF?ref_=ppx_hzod_title_dt_b_fed_asin_title_0_0"
    assert order_item.title == "Colgate MaxFresh Knockout Breath Freshening Toothpaste, 150 Milliliters"
    assert order_item.unit_price == Decimal("2.97")
    assert order_item.quantity == 2
    assert order_item.total_price == Decimal("5.94")


@pytest.mark.anyio
async def test_scrape__success_style_2() -> None:
    # GIVEN
    fixture = """
<div class="a-fixed-left-grid-inner" style="padding-left:100px">
   <div class="a-text-center a-fixed-left-grid-col a-col-left" style="width:100px;margin-left:-100px;float:left;">
      <div class="item-view-left-col-inner">
         <a class="a-link-normal" href="/gp/product/B00CXK623E/ref=ppx_od_dt_b_asin_image_s00?ie=UTF8&amp;psc=1">
         <img alt="" src="https://m.media-amazon.com/images/I/414MHoV2IZL._SY90_.jpg" aria-hidden="true" class="yo-critical-feature" height="90" width="90" title="Lip Smacker Coca-Cola Party Pack Lip Glosses, 8 Count, Coca Cola, Variety 1 (SFS Only)" data-a-hires="https://m.media-amazon.com/images/I/414MHoV2IZL._SY180_.jpg" data-already-flushed-csm="true">
         </a>
         <span class="item-view-qty"> 2 </span>
      </div>
   </div>
   <div class="a-fixed-left-grid-col yohtmlc-item a-col-right" style="padding-left:1.5%;float:left;">
      <div class="a-row">
         <a class="a-link-normal" href="/gp/product/B00CXK623E/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&amp;psc=1"> Lip Smacker Coca-Cola Party Pack Lip Glosses, 8 Count, Coca Cola, Variety 1 (SFS Only) </a>
      </div>
      <div class="a-row">
         <span class="a-size-small a-color-secondary"> Manufacturer: Lip Smacker, CITY OF INDUSTRY, CA, 91789 US </span>
      </div>
      <div class="a-row">
         <span class="a-size-small a-color-secondary"> Sold by: Amazon.com.ca ULC </span>
      </div>
      <div class="a-row">
         <span class="a-size-small">
            <div class="a-row a-size-small">Return window closed on Nov 3, 2024</div>
         </span>
      </div>
      <div class="a-row">
         <span class="a-size-small a-color-price"> $14.99 </span>
      </div>
      <div class="a-row">
         <span class="a-declarative" data-action="bia_button" data-bia_button="{}">
            <span class="a-button a-spacing-mini a-button-primary yohtmlc-buy-it-again" id="a-autoid-1">
               <span class="a-button-inner">
                  <a href="/gp/buyagain/ref=ppx_od_dt_b_bia?ie=UTF8&amp;ats=eyJjdXN0b21lcklkIjoiQVVKQUoxMDRXTFpQMyIsImV4cGxpY2l0Q2FuZGlkYXRlcyI6IkIwMENY%0ASzYyM0UifQ%3D%3D%0A" aria-label="Buy it again" class="a-button-text" role="button" id="a-autoid-1-announce">
                     <div class="reorder-modal-trigger-text">
                        <i class="reorder-modal-trigger-icon"></i> Buy it again
                     </div>
                  </a>
               </span>
            </span>
         </span>
      </div>
   </div>
</div>
"""
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = OrderItemScraper(order_id="123-4567890-1234567")
    order_item = await sut.scrape(URL("https://www.amazon.ca"), html)

    # THEN
    assert order_item is not None
    assert order_item.order_id == "123-4567890-1234567"
    assert order_item.product_id == "B00CXK623E"
    assert (
        order_item.product_link
        == "https://www.amazon.ca/gp/product/B00CXK623E/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1"
    )
    assert order_item.title == "Lip Smacker Coca-Cola Party Pack Lip Glosses, 8 Count, Coca Cola, Variety 1 (SFS Only)"
    assert order_item.unit_price == Decimal("14.99")
    assert order_item.quantity == 2
    assert order_item.total_price == Decimal("29.98")


@pytest.mark.anyio
async def test_scrape__success_style_3() -> None:
    # GIVEN
    fixture = """
<div class="a-fixed-left-grid-inner" style="padding-left:100px">
   <div class="a-text-center a-fixed-left-grid-col a-col-left" style="width:100px;margin-left:-100px;float:left;">
      <div class="item-view-left-col-inner">
         <a class="a-link-normal" href="/gp/product/B0BHWHVJ66/ref=ppx_od_dt_b_asin_image?ie=UTF8&amp;psc=1">
         <img alt="" src="https://m.media-amazon.com/images/I/41gC9MeZ0TL._SY180_.jpg" aria-hidden="true" class="yo-critical-feature" height="90" width="90" title="Amazon.ca Gift Card - Print - Paper Snowflakes (Print at Home)" data-a-hires="https://m.media-amazon.com/images/I/41gC9MeZ0TL._SY180_.jpg" data-already-flushed-csm="true">
         </a>
      </div>
   </div>
   <div class="a-fixed-left-grid-col yohtmlc-item a-col-right" style="padding-left:1.5%;float:left;">
      <div class="a-row">
         <a class="a-link-normal" href="/gp/product/B0BHWHVJ66/ref=ppx_od_dt_b_asin_title?ie=UTF8&amp;psc=1">
         Amazon.ca Gift Card - Print - Paper Snowflakes (Print at Home)
         </a>
      </div>
      <div class="a-row">
         <div class="a-row a-spacing-top-small">
            <span class="a-color-secondary">
            Message:
            </span>
            <div class="a-row">
               Merry Christmas and Happy Holidays!
            </div>
         </div>
      </div>
      <div class="a-row">
         <div class="a-row a-spacing-top-small">
            <div class="a-column a-span2">
               <span class="a-color-secondary">Amount</span>
            </div>
            <div class="a-column a-span5">
               <span class="a-color-secondary"></span>
            </div>
            <div class="a-column a-span5 a-span-last">
               <span class="a-color-secondary">Status</span>
            </div>
         </div>
         <div class="a-row a-spacing-top-mini gift-card-instance">
            <div class="a-column a-span2">
               $10.00
            </div>
            <div class="a-column a-span5 recipient">
            </div>
            <div class="a-column a-span5 a-span-last">
               Ready to print
            </div>
         </div>
      </div>
   </div>
</div>
"""
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = OrderItemScraper(order_id="123-4567890-1234567")
    order_item = await sut.scrape(URL("https://www.amazon.ca"), html)

    # THEN
    assert order_item is not None
    assert order_item.order_id == "123-4567890-1234567"
    assert order_item.product_id == "B0BHWHVJ66"
    assert (
        order_item.product_link
        == "https://www.amazon.ca/gp/product/B0BHWHVJ66/ref=ppx_od_dt_b_asin_title?ie=UTF8&psc=1"
    )
    assert order_item.title == "Amazon.ca Gift Card - Print - Paper Snowflakes (Print at Home)"
    assert order_item.unit_price == Decimal("10.00")
    assert order_item.quantity == 1
    assert order_item.total_price == Decimal("10.00")
