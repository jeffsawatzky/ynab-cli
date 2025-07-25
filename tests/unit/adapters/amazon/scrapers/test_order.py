from decimal import Decimal

import pytest
from bs4 import BeautifulSoup
from httpx import URL

from ynab_cli.adapters.amazon.scrapers.order import OrderScraper


@pytest.mark.anyio
async def test_scrape__success_1() -> None:
    # GIVEN
    fixture = TEST_PARSE_ORDER_HTML_1
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = OrderScraper()
    order = await sut.scrape(URL("https://www.amazon.ca"), html)

    # THEN
    assert order is not None
    assert order.order_id == "123-4567890-1234567"
    assert order.refund_link == "https://www.amazon.ca/spr/returns/cart?orderId=123-4567890-1234567"
    assert order.item_subtotal == Decimal("122.17")
    assert order.grand_total == Decimal("135.55")
    assert len(order.shipments) == 2


@pytest.mark.anyio
async def test_scrape__success_2() -> None:
    # GIVEN
    fixture = TEST_PARSE_ORDER_HTML_2
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = OrderScraper()
    order = await sut.scrape(URL("https://www.amazon.ca"), html)

    # THEN
    assert order is not None
    assert order.order_id == "123-4567890-1234567"
    assert order.refund_link == "https://www.amazon.ca/spr/returns/cart?orderId=123-4567890-1234567"
    assert order.item_subtotal == Decimal("10.00")
    assert order.grand_total == Decimal("10.00")
    assert len(order.shipments) == 1


TEST_PARSE_ORDER_HTML_1 = """
<div id="orderDetails" class="a-section dynamic-width">
  <div class="" data-component="default">
    <div class="" data-component="debugBanner"></div>
    <div class="" data-component="aapiDebug"></div>
    <div class="" data-component="ddtDebug"></div>
    <div class="" data-component="breadcrumb">
      <div class="a-section a-spacing-large a-spacing-top-small">
        <ul class="a-unordered-list a-horizontal od-breadcrumbs">
          <li class="od-breadcrumbs__crumb">
            <span class="a-list-item">
              <a class="a-link-normal" title="Return to Your Account" href="/gp/css/homepage.html/ref=ppx_hzod_bc_dt_b_ya_link">Your Account</a>
            </span>
          </li>
          <li class="od-breadcrumbs__crumb od-breadcrumbs__crumb--divider">
            <span class="a-list-item">&gt;</span>
          </li>
          <li class="od-breadcrumbs__crumb">
            <span class="a-list-item">
              <a class="a-link-normal" title="Return to Your Orders" href="/gp/your-account/order-history/ref=ppx_hzod_bc_dt_b_oh_link">Your Orders</a>
            </span>
          </li>
          <li class="od-breadcrumbs__crumb od-breadcrumbs__crumb--divider">
            <span class="a-list-item">&gt;</span>
          </li>
          <li class="od-breadcrumbs__crumb od-breadcrumbs__crumb--current">
            <span class="a-list-item">
              <span class="a-color-state">Order Details</span>
            </span>
          </li>
        </ul>
      </div>
    </div>
    <div class="" data-component="banner"></div>
    <div class="" data-component="returnsBanner"></div>
    <div class="" data-component="archivedMessage"></div>
    <div class="" data-component="title">
      <div class="a-section">
        <div class="a-row">
          <div class="" data-component="titleLeftGrid">
            <div class="a-column a-span6">
              <div class="" data-component="orderDetailsTitle">
                <h1>Order Details</h1>
              </div>
            </div>
          </div>
          <div class="" data-component="titleRightGrid">
            <div class="a-column a-span6 a-text-right a-span-last">
              <div class="" data-component="brandLogo"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="" data-component="orderDateInvoice">
      <div class="a-row a-spacing-base">
        <div class="a-column a-span9 a-spacing-top-mini">
          <div class="a-row a-spacing-none">
            <span class="order-date-invoice-item"> Ordered on October 4, 2024 <i class="a-icon a-icon-text-separator" role="img"></i>
            </span>
            <span class="order-date-invoice-item"> Order# <bdi dir="ltr">123-4567890-1234567</bdi>
            </span>
          </div>
        </div>
        <div class="a-column a-span3 a-text-right a-spacing-top-none hide-if-no-js a-span-last">
          <div class="a-row a-spacing-none">
            <ul class="a-unordered-list a-nostyle a-vertical">
              <li>
                <span class="a-list-item"> Amazon.com.ca, Inc. </span>
              </li>
              <li>
                <span class="a-list-item"> GST/HST - 85730 5932 RT0001 </span>
              </li>
              <li>
                <span class="a-list-item"> QST - 1201187016 TQ0001 </span>
              </li>
            </ul>
            <div class="a-popover-preload" id="a-popover-invoiceLinks">
              <ul class="a-unordered-list a-vertical a-nowrap">
                <li>
                  <span class="a-list-item">
                    <a class="a-link-normal" href="/documents/download/664c62c2-e80c-44f1-a742-2ad2bffef374/invoice.pdf"> Invoice 1 </a>
                  </span>
                </li>
                <li>
                  <span class="a-list-item">
                    <a class="a-link-normal" href="/documents/download/d499ab89-6d79-475b-a010-34965aef28f6/invoice.pdf"> Credit note 1 </a>
                  </span>
                </li>
                <li>
                  <span class="a-list-item">
                    <a class="a-link-normal" href="/gp/help/contact/contact.html/ref=ppx_od_dt_b_request_invoice?ie=UTF8&amp;orderID=123-4567890-1234567&amp;sellerID=A1IRZ7664JSWXN&amp;subject=30"> Request invoice </a>
                  </span>
                </li>
                <li>
                  <span class="a-list-item">
                    <a class="a-link-normal" href="/gp/css/summary/print.html/ref=ppx_od_dt_b_invoice?ie=UTF8&amp;orderID=123-4567890-1234567"> Printable Order Summary </a>
                  </span>
                </li>
                <li>
                  <span class="a-list-item">
                    <a class="a-link-normal" href="/gp/help/customer/display.html/ref=ppx_od_dt_b_legal_invoice_help?ie=UTF8&amp;nodeId=201516020"> Invoice unavailable for some items. Learn more. </a>
                  </span>
                </li>
              </ul>
            </div>
            <span class="a-declarative" data-action="a-popover" data-a-popover="{&quot;name&quot;:&quot;invoiceLinks&quot;,&quot;position&quot;:&quot;triggerBottom&quot;,&quot;activate&quot;:&quot;onclick&quot;}">
              <a href="javascript:void(0)" class="a-popover-trigger a-declarative">
                <span class="a-size-medium">Invoice</span>
                <i class="a-icon a-icon-popover"></i>
              </a>
            </span>
          </div>
        </div>
      </div>
      <div class="a-row a-spacing-base hide-if-js">
        <div class="a-column a-span12 a-spacing-top-mini">
          <ul class="a-unordered-list a-nostyle a-vertical">
            <li>
              <span class="a-list-item"> Amazon.com.ca, Inc. </span>
            </li>
            <li>
              <span class="a-list-item"> GST/HST - 85730 5932 RT0001 </span>
            </li>
            <li>
              <span class="a-list-item"> QST - 1201187016 TQ0001 </span>
            </li>
          </ul>
          <ul class="a-unordered-list a-nostyle a-vertical">
            <li>
              <span class="a-list-item">
                <a class="a-link-normal" href="/documents/download/664c62c2-e80c-44f1-a742-2ad2bffef374/invoice.pdf"> Invoice 1 </a>
              </span>
            </li>
            <li>
              <span class="a-list-item">
                <a class="a-link-normal" href="/documents/download/d499ab89-6d79-475b-a010-34965aef28f6/invoice.pdf"> Credit note 1 </a>
              </span>
            </li>
            <li>
              <span class="a-list-item">
                <a class="a-link-normal" href="/gp/help/contact/contact.html/ref=ppx_od_dt_b_request_invoice?ie=UTF8&amp;orderID=123-4567890-1234567&amp;sellerID=A1IRZ7664JSWXN&amp;subject=30"> Request invoice </a>
              </span>
            </li>
            <li>
              <span class="a-list-item">
                <a class="a-link-normal" href="/gp/css/summary/print.html/ref=ppx_od_dt_b_invoice?ie=UTF8&amp;orderID=123-4567890-1234567"> Printable Order Summary </a>
              </span>
            </li>
            <li>
              <span class="a-list-item">
                <a class="a-link-normal" href="/gp/help/customer/display.html/ref=ppx_od_dt_b_legal_invoice_help?ie=UTF8&amp;nodeId=201516020"> Invoice unavailable for some items. Learn more. </a>
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="" data-component="mfaMessage"></div>
    <div class="" data-component="orderSummary">
      <div class="a-box-group a-spacing-base">
        <div class="a-box">
          <div class="a-box-inner">
            <div class="a-fixed-right-grid">
              <div class="a-fixed-right-grid-inner" style="padding-right:260px">
                <div class="a-fixed-right-grid-col a-col-left" style="padding-right:0%;float:left;">
                  <div class="a-row">
                    <div class="a-column a-span5">
                      <div class="" data-component="rawShippingAddress">
                        <div class="a-section a-spacing-none od-shipping-address-container">
                          <h5 class="a-spacing-micro"> Shipping Address </h5>
                          <div class="a-row a-spacing-micro">
                            <div class="displayAddressDiv">
                              <ul class="displayAddressUL">
                                <li class="displayAddressLI displayAddressFullName">Some Dude</li>
                                <li class="displayAddressLI displayAddressAddressLine1">1 Street Avenue</li>
                                <li class="displayAddressLI displayAddressCityStateOrRegionPostalCode">City, Province POSTAL CODE</li>
                                <li class="displayAddressLI displayAddressCountryName">Canada</li>
                              </ul>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="a-column a-span7 a-span-last">
                      <div class="a-section a-spacing-base">
                        <div class="" data-component="paymentMethod">
                                                                                                        <div data-pmts-component-id="pp-bM4unV-1" class="a-row pmts-portal-root-NhnhppP4d8pr pmts-portal-component pmts-portal-components-pp-bM4unV-1">
                            <div class="a-column a-span12 pmts-payment-instrument-billing-address">
                              <div data-pmts-component-id="pp-bM4unV-2" class="a-row a-spacing-small pmts-portal-component pmts-portal-components-pp-bM4unV-2">
                                <div class="a-row pmts-payments-instrument-header">
                                  <span class="a-text-bold">Payment Methods</span>
                                </div>
                                <div class="a-row pmts-payments-instrument-details">
                                  <ul class="a-unordered-list a-nostyle a-vertical no-bullet-list pmts-payments-instrument-list">
                                    <li class="a-spacing-micro pmts-payments-instrument-detail-box-paystationpaymentmethod">
                                      <span class="a-list-item">
                                        <img alt="Visa" src="https://m.media-amazon.com/images/G/15/payments-portal/r1/issuer-images/visa._CB413187912_.png" class="pmts-payment-credit-card-instrument-logo" height="23px" width="34px">
                                        <span class="a-letter-space"></span>Visa <span class="a-letter-space"></span>
                                        <span class="a-color-base">ending in 1234</span>
                                      </span>
                                    </li>
                                  </ul>
                                </div>
                              </div>
                            </div>
                          </div>
                          <link rel="stylesheet" type="text/css" href="https://m.media-amazon.com/images/I/11STWhdvr1L._RC|01tEjLkP-OL.css,21pZ9-tDsfL.css,01gqZiFs-tL.css,116LWdTN6UL.css,01cq16REt9L.css,01qk4TdW33L.css,11cVF3U-9BL.css,01cxjPaaTNL.css,01l0V3645dL.css,01SJRGuZivL.css,21jGj3aJ6ZL.css,11HEveYPS1L.css,01hOHsbn7OL.css,01IsDXoRrML.css,11bTAqdlDgL.css,01hIZRtcaHL.css,01NGxBoTbmL.css,01Mv8eppKAL.css,21TuFm4rvyL.css,11aHu4KrBRL.css,01uakdML80L.css,01uHZesS5LL.css,11MhOiv1rNL.css,01rKSjRRIdL.css,018M3caCSzL.css,01Rgr3O5jgL.css,61OrZ4-ie6L.css,01xniGkbKHL.css,01BUQQ2AAFL.css,11+KVSh5kaL.css,018GGCZ05rL.css,01RVwf5E26L.css,018QFljl9NL.css,01RKPCJHpeL.css,01gtkpxWIOL.css,012HRkWTMYL.css,01zEhgDPWUL.css,01le4Wlx71L.css,01NfyFypiAL.css,01x1gcd+b6L.css,21H4c3YVAzL.css,11uTQeLDHRL.css,01vSTBFdADL.css,21F2KqvWKoL.css,01X3lCf9VVL.css,01K72ZPRhdL.css,01SMFqALhuL.css,01Kz8HcbaSL.css,1192eqsMCTL.css,01735fiNhpL.css,01W9cE2pBBL.css,21bUEs5X9dL.css,01ENy2AhhHL.css,01lnEwmkCOL.css,01Epd5A5L9L.css,01i7-FZ2dbL.css,01ONHh8S9QL.css,01NDW5IRowL.css,01Jrep1-A8L.css,013mx6I5MjL.css,01DR-IGztZL.css,01oed2b7XHL.css,21WyWpnsGQL.css,01YgiH4056L.css,01-BlL5QIGL.css,01dkJYlUMlL.css,013gNYW5EZL.css,01Xbi2zDI3L.css,01B8WX2PjrL.css,01Z42xKR4FL.css,0139uaPyFCL.css,01Gtbyceb8L.css,0167aosbt1L.css_.css">
                                                                            </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div id="od-subtotals" class="a-fixed-right-grid-col a-col-right" style="width:260px;margin-right:-260px;float:left;">
                  <div class="" data-component="orderSubtotals">
                    <h5 class="a-spacing-micro a-text-left"> Order Summary </h5>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-base"> Item(s) Subtotal: </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-base"> $122.17 </span>
                      </div>
                    </div>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-base"> Shipping &amp; Handling: </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-base"> $6.99 </span>
                      </div>
                    </div>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-base"> Free Shipping: </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-base"> -$6.99 </span>
                      </div>
                    </div>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-base"> Buy 5, save 5%: </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-base"> -$2.21 </span>
                      </div>
                    </div>
                    <div class="a-row a-spacing-mini"></div>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-base"> Total before tax: </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-base"> $119.96 </span>
                      </div>
                    </div>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-base"> Estimated GST/HST: </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-base"> $15.59 </span>
                      </div>
                    </div>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-base"> Estimated PST/RST/QST: </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-base"> $0.00 </span>
                      </div>
                    </div>
                    <div class="a-row a-spacing-mini"></div>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-base a-text-bold"> Grand Total: </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-base a-text-bold"> $135.55 </span>
                      </div>
                    </div>
                    <div class="a-row">
                      <div class="a-column a-span7 a-text-left">
                        <span class="a-color-success a-text-bold">
                          <span class="a-declarative" data-action="a-popover" data-a-popover="{&quot;width&quot;:&quot;350&quot;,&quot;closeButton&quot;:&quot;false&quot;,&quot;position&quot;:&quot;triggerBottom&quot;,&quot;name&quot;:&quot;orderRefundBreakdown&quot;}">
                            <a href="javascript:void(0)" class="a-popover-trigger a-declarative">
                              <span class="a-color-success">Refund Total</span>
                              <i class="a-icon a-icon-popover"></i>
                            </a>
                          </span>
                          <div class="a-popover-preload" id="a-popover-orderRefundBreakdown">
                            <div class="a-row">
                              <div class="a-column a-span9">
                                <span class="a-color-success"> Item(s) refund: </span>
                              </div>
                              <div class="a-column a-span3 a-text-right a-span-last">
                                <span class="a-color-success"> $45.95 </span>
                              </div>
                            </div>
                            <div class="a-row">
                              <div class="a-column a-span9">
                                <span class="a-color-success"> Tax refund: </span>
                              </div>
                              <div class="a-column a-span3 a-text-right a-span-last">
                                <span class="a-color-success"> $5.97 </span>
                              </div>
                            </div>
                            <div class="a-row a-spacing-top-mini">
                              <div class="a-column a-span9">
                                <span class="a-color-success a-text-bold"> Refund Total: </span>
                              </div>
                              <div class="a-column a-span3 a-text-right a-span-last">
                                <span class="a-color-success a-text-bold"> $51.92 </span>
                              </div>
                            </div>
                          </div>
                        </span>
                      </div>
                      <div class="a-column a-span5 a-text-right a-span-last">
                        <span class="a-color-success a-text-bold"> $51.92 </span>
                      </div>
                    </div>
                  </div>
                  <div class="" data-component="chargeSummary"></div>
                  <div class="" data-component="primeWardrobeChargeMessage"></div>
                </div>
              </div>
            </div>
            <div class="" data-component="financialOfferBonus"></div>
            <div class="" data-component="wirelessDeposits"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="" data-component="orderCard"></div>
    <div class="" data-component="shipments">
      <div class="a-box-group od-shipments">
        <div class="a-box shipment shipment-is-delivered">
          <div class="a-box-inner">
            <div class="a-row shipment-top-row js-shipment-info-container">
              <div style="margin-right:220px; padding-right:20px">
                <div class="a-row">
                  <span class="a-size-medium a-color-base a-text-bold"> Delivered Oct 4, 2024 </span>
                </div>
                <div class="a-row">
                  <div class="a-row"> Package was left near the front door or porch </div>
                  <span data-isstatuswithwarning="0" data-yodeliveryestimate="Delivered Oct 4, 2024" data-yoshortstatuscode="DELIVERED" data-yostatusstring="" class="js-shipment-info aok-hidden"></span>
                </div>
              </div>
              <div class="actions" style="width:220px;">
                <div class="a-row">
                  <div class="a-button-stack">
                    <span class="a-declarative" data-action="set-shipment-info-cookies" data-set-shipment-info-cookies="{}">
                      <span class="a-button a-button-base track-package-button" id="a-autoid-0">
                        <span class="a-button-inner">
                          <a href="/progress-tracker/package/ref=ppx_od_dt_b_track_package?_encoding=UTF8&amp;itemId=jhjpowhrnrlvwup&amp;orderId=123-4567890-1234567&amp;packageIndex=0&amp;shipmentId=GHZ4HHRHh&amp;vt=ORDER_DETAILS" class="a-button-text" role="button" id="a-autoid-0-announce"> Track package </a>
                        </span>
                      </span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="a-fixed-right-grid a-spacing-top-medium">
              <div class="a-fixed-right-grid-inner a-grid-vertical-align a-grid-top">
                <div class="a-fixed-right-grid-col a-col-left" style="padding-right:3.2%;float:left;">
                  <div class="a-row">
                    <div class="a-fixed-left-grid a-spacing-base">
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
                    </div>
                    <div class="a-fixed-left-grid a-spacing-base">
                      <div class="a-fixed-left-grid-inner" style="padding-left:100px">
                        <div class="a-text-center a-fixed-left-grid-col a-col-left" style="width:100px;margin-left:-100px;float:left;">
                          <div class="item-view-left-col-inner">
                            <a class="a-link-normal" href="/gp/product/B0BTTN6JQV/ref=ppx_od_dt_b_asin_image_s00?ie=UTF8&amp;psc=1">
                              <img alt="" src="https://m.media-amazon.com/images/I/51Q2LSGwcvL._SY90_.jpg" aria-hidden="true" class="yo-critical-feature" height="90" width="90" title="LivaClean 240 CT Superstar Holographic Patches Space Edition - Face Patches, Hydrocolloid Patches for Face, Star Face Patch, Hydrocolloid Patches, Patches Star" data-a-hires="https://m.media-amazon.com/images/I/51Q2LSGwcvL._SY180_.jpg" data-already-flushed-csm="true">
                            </a>
                          </div>
                        </div>
                        <div class="a-fixed-left-grid-col yohtmlc-item a-col-right" style="padding-left:1.5%;float:left;">
                          <div class="a-row">
                            <a class="a-link-normal" href="/gp/product/B0BTTN6JQV/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&amp;psc=1"> LivaClean 240 CT Superstar Holographic Patches Space Edition - Face Patches, Hydrocolloid Patches for Face, Star Face Patch, Hydrocolloid Patches, Patches Star </a>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-secondary"> Manufacturer: LivaClean </span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-secondary"> Sold by: <a class="a-link-normal" href="/gp/help/seller/at-a-glance.html/ref=ppx_od_dt_b_sellerprofile_s00?ie=UTF8&amp;isAmazonFulfilled=1&amp;marketplaceSeller=1&amp;orderID=123-4567890-1234567&amp;seller=A23KAG5GKM0NLF"> Livaclean</a>
                            </span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small">
                              <div class="a-row a-size-small">Return window closed on Nov 3, 2024</div>
                            </span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-price"> $18.99 </span>
                          </div>
                          <div class="a-row">
                            <span class="a-declarative" data-action="bia_button" data-bia_button="{}">
                              <span class="a-button a-spacing-mini a-button-primary yohtmlc-buy-it-again" id="a-autoid-2">
                                <span class="a-button-inner">
                                  <a href="/gp/buyagain/ref=ppx_od_dt_b_bia?ie=UTF8&amp;ats=eyJjdXN0b21lcklkIjoiQVVKQUoxMDRXTFpQMyIsImV4cGxpY2l0Q2FuZGlkYXRlcyI6IkIwQlRU%0ATjZKUVYifQ%3D%3D%0A" aria-label="Buy it again" class="a-button-text" role="button" id="a-autoid-2-announce">
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
                    </div>
                    <div class="a-fixed-left-grid a-spacing-base">
                      <div class="a-fixed-left-grid-inner" style="padding-left:100px">
                        <div class="a-text-center a-fixed-left-grid-col a-col-left" style="width:100px;margin-left:-100px;float:left;">
                          <div class="item-view-left-col-inner">
                            <a class="a-link-normal" href="/gp/product/B07L9T8178/ref=ppx_od_dt_b_asin_image_s00?ie=UTF8&amp;psc=1">
                              <img alt="" src="https://m.media-amazon.com/images/I/51Wq9bO1u4S._SY90_.jpg" aria-hidden="true" class="yo-critical-feature" height="90" width="90" title="HUBBA BUBBA, Mixed Fruit Flavoured Bubble Gum Variety Pack, 5 Pieces, 4 Packs" data-a-hires="https://m.media-amazon.com/images/I/51Wq9bO1u4S._SY180_.jpg" data-already-flushed-csm="true">
                            </a>
                            <span class="item-view-qty"> 2 </span>
                          </div>
                        </div>
                        <div class="a-fixed-left-grid-col yohtmlc-item a-col-right" style="padding-left:1.5%;float:left;">
                          <div class="a-row">
                            <a class="a-link-normal" href="/gp/product/B07L9T8178/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&amp;psc=1"> HUBBA BUBBA, Mixed Fruit Flavoured Bubble Gum Variety Pack, 5 Pieces, 4 Packs </a>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-secondary"> Manufacturer: Mars Wrigley Confectionery, TORONTO, ON, M2H 3S8 CA </span>
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
                            <span class="a-size-small a-color-price"> $3.75 </span>
                          </div>
                          <div class="a-row">
                            <span class="a-declarative" data-action="bia_button" data-bia_button="{}">
                              <span class="a-button a-spacing-mini a-button-primary yohtmlc-buy-it-again" id="a-autoid-3">
                                <span class="a-button-inner">
                                  <a href="/gp/buyagain/ref=ppx_od_dt_b_bia?ie=UTF8&amp;ats=eyJjdXN0b21lcklkIjoiQVVKQUoxMDRXTFpQMyIsImV4cGxpY2l0Q2FuZGlkYXRlcyI6IkIwN0w5%0AVDgxNzgifQ%3D%3D%0A" aria-label="Buy it again" class="a-button-text" role="button" id="a-autoid-3-announce">
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
                    </div>
                    <div class="a-fixed-left-grid a-spacing-base">
                      <div class="a-fixed-left-grid-inner" style="padding-left:100px">
                        <div class="a-text-center a-fixed-left-grid-col a-col-left" style="width:100px;margin-left:-100px;float:left;">
                          <div class="item-view-left-col-inner">
                            <a class="a-link-normal" href="/gp/product/B08ZPLYGV6/ref=ppx_od_dt_b_asin_image_s00?ie=UTF8&amp;psc=1">
                              <img alt="" src="https://m.media-amazon.com/images/I/51IPRh8N1dL._SY90_.jpg" aria-hidden="true" class="yo-critical-feature" height="90" width="90" title="BETTY CROCKER GUSHERS - FAMILY PACK SIZE - Gushin Grape and Tropical Flavours, Strawberry Splash Fruit Flavoured Snacks, Pack of 16 Pouches, 368 Grams Package of Fruit Flavoured Snacks, Variety Flavours Pack" data-a-hires="https://m.media-amazon.com/images/I/51IPRh8N1dL._SY180_.jpg" data-already-flushed-csm="true">
                            </a>
                          </div>
                        </div>
                        <div class="a-fixed-left-grid-col yohtmlc-item a-col-right" style="padding-left:1.5%;float:left;">
                          <div class="a-row">
                            <a class="a-link-normal" href="/gp/product/B08ZPLYGV6/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&amp;psc=1"> BETTY CROCKER GUSHERS - FAMILY PACK SIZE - Gushin Grape and Tropical Flavours, Strawberry Splash Fruit Flavoured Snacks, Pack of 16 Pouches, 368 Grams Package of Fruit Flavoured Snacks, Variety Flavours Pack </a>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-secondary"> Manufacturer: General Mills Canada Corporation, MISSISSAUGA, ON, L4W 5N9 CA </span>
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
                            <span class="a-size-small a-color-price"> $6.77 </span>
                          </div>
                          <div class="a-row">
                            <span class="a-declarative" data-action="bia_button" data-bia_button="{}">
                              <span class="a-button a-spacing-mini a-button-primary yohtmlc-buy-it-again" id="a-autoid-4">
                                <span class="a-button-inner">
                                  <a href="/gp/buyagain/ref=ppx_od_dt_b_bia?ie=UTF8&amp;ats=eyJjdXN0b21lcklkIjoiQVVKQUoxMDRXTFpQMyIsImV4cGxpY2l0Q2FuZGlkYXRlcyI6IkIwOFpQ%0ATFlHVjYifQ%3D%3D%0A" aria-label="Buy it again" class="a-button-text" role="button" id="a-autoid-4-announce">
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
                    </div>
                    <div class="a-fixed-left-grid a-spacing-none">
                      <div class="a-fixed-left-grid-inner" style="padding-left:100px">
                        <div class="a-text-center a-fixed-left-grid-col a-col-left" style="width:100px;margin-left:-100px;float:left;">
                          <div class="item-view-left-col-inner">
                            <a class="a-link-normal" href="/gp/product/B09P6RDQJ2/ref=ppx_od_dt_b_asin_image_s00?ie=UTF8&amp;psc=1">
                              <img alt="" src="https://m.media-amazon.com/images/I/5175kweITnL._SY90_.jpg" aria-hidden="true" class="yo-critical-feature" height="90" width="90" title="10 Pack Hand Cream For Chapped Hands,Natural Botanical Fragrance Hand Lotion,Mini Hand Cream For Working Dry Hands,Moisturizing Travel Size Hand Cream Set with Natural Botanical For Women- 30ml" data-a-hires="https://m.media-amazon.com/images/I/5175kweITnL._SY180_.jpg" data-already-flushed-csm="true">
                            </a>
                          </div>
                        </div>
                        <div class="a-fixed-left-grid-col yohtmlc-item a-col-right" style="padding-left:1.5%;float:left;">
                          <div class="a-row">
                            <a class="a-link-normal" href="/gp/product/B09P6RDQJ2/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&amp;psc=1"> 10 Pack Hand Cream For Chapped Hands,Natural Botanical Fragrance Hand Lotion,Mini Hand Cream For Working Dry Hands,Moisturizing Travel Size Hand Cream Set with Natural Botanical For Women- 30ml </a>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-secondary"> Manufacturer: BKPPLZP, 10016 </span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-secondary"> Sold by: <a class="a-link-normal" href="/gp/help/seller/at-a-glance.html/ref=ppx_od_dt_b_sellerprofile_s00?ie=UTF8&amp;isAmazonFulfilled=1&amp;marketplaceSeller=1&amp;orderID=123-4567890-1234567&amp;seller=A358F26MJKLCM6"> BKPPWYBXZ</a>
                            </span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small">
                              <div class="a-row a-size-small">Return window closed on Nov 3, 2024</div>
                            </span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-price"> $12.98 </span>
                          </div>
                          <div class="a-row">
                            <span class="a-declarative" data-action="bia_button" data-bia_button="{}">
                              <span class="a-button a-spacing-mini a-button-primary yohtmlc-buy-it-again" id="a-autoid-5">
                                <span class="a-button-inner">
                                  <a href="/gp/buyagain/ref=ppx_od_dt_b_bia?ie=UTF8&amp;ats=eyJjdXN0b21lcklkIjoiQVVKQUoxMDRXTFpQMyIsImV4cGxpY2l0Q2FuZGlkYXRlcyI6IkIwOVA2%0AUkRRSjIifQ%3D%3D%0A" aria-label="Buy it again" class="a-button-text" role="button" id="a-autoid-5-announce">
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
                    </div>
                  </div>
                </div>
                <div class="a-fixed-right-grid-col a-col-right" style="width:220px;margin-right:-220px;float:left;">
                  <div class="a-row">
                    <div class="a-button-stack yohtmlc-shipment-level-connections">
                      <span class="a-button a-button-normal a-spacing-mini a-button-base" id="a-autoid-6">
                        <span class="a-button-inner">
                          <a id="Leave-seller-feedback_1" href="/gp/feedback/leave-customer-feedback.html/ref=ppx_od_dt_b_sell_feed_s00?ie=UTF8&amp;order=123-4567890-1234567" class="a-button-text" role="button"> Leave seller feedback </a>
                        </span>
                      </span>
                      <span class="a-button a-button-normal a-spacing-mini a-button-base" id="a-autoid-7">
                        <span class="a-button-inner">
                          <a id="Write-a-product-review_1" href="/review/review-your-purchases/ref=ppx_od_dt_b_rev_prod_s00?_encoding=UTF8&amp;asins=B09RKNJWCR%2CB00CXK623E%2CB0BTTN6JQV%2CB07L9T8178%2CB08ZPLYGV6%2CB09P6RDQJ2&amp;channel=YAcc-wr" class="a-button-text" role="button"> Write a product review </a>
                        </span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="a-box shipment shipment-is-delivered">
          <div class="a-box-inner">
            <div class="a-row shipment-top-row js-shipment-info-container">
              <div style="margin-right:220px; padding-right:20px">
                <div class="a-row">
                  <span class="a-size-medium a-text-bold"> Return complete </span>
                </div>
                <div class="a-row">
                  <span class="a-color-secondary"> Your return is complete. Your refund has been issued. </span>
                  <span class="a-declarative" data-action="a-popover" data-a-popover="{&quot;closeButton&quot;:&quot;false&quot;,&quot;position&quot;:&quot;triggerBottom&quot;,&quot;name&quot;:&quot;extra_return_summary_info123-4567890-1234567&quot;}">
                    <a href="javascript:void(0)" class="a-popover-trigger a-declarative hide-if-no-js"> When will I get my refund? <i class="a-icon a-icon-popover"></i>
                    </a>
                  </span>
                </div>
              </div>
              <div class="actions" style="width:220px;"></div>
            </div>
            <div class="a-fixed-right-grid a-spacing-top-medium">
              <div class="a-fixed-right-grid-inner a-grid-vertical-align a-grid-top">
                <div class="a-fixed-right-grid-col a-col-left" style="padding-right:3.2%;float:left;">
                  <div class="a-row">
                    <div class="a-fixed-left-grid a-spacing-none">
                      <div class="a-fixed-left-grid-inner" style="padding-left:100px">
                        <div class="a-text-center a-fixed-left-grid-col a-col-left" style="width:100px;margin-left:-100px;float:left;">
                          <div class="item-view-left-col-inner">
                            <a class="a-link-normal" href="/gp/product/B09RKNJWCR/ref=ppx_od_dt_b_asin_image_s01?ie=UTF8&amp;psc=1">
                              <img alt="" src="https://m.media-amazon.com/images/I/41ubi5vlEbL._SY90_.jpg" aria-hidden="true" class="yo-critical-feature" height="90" width="90" title="grace and stella Under Eye Mask-Reduce Dark Circles, Puffy Eyes, Undereye Bags, Wrinkles-Gel Under Eye Patches, Vegan Cruelty-Free Self Care (72 Pairs, Gold, Pink &amp;amp; Blue)" data-a-hires="https://m.media-amazon.com/images/I/41ubi5vlEbL._SY180_.jpg" data-already-flushed-csm="true">
                            </a>
                          </div>
                        </div>
                        <div class="a-fixed-left-grid-col yohtmlc-item a-col-right" style="padding-left:1.5%;float:left;">
                          <div class="a-row">
                            <a class="a-link-normal" href="/gp/product/B09RKNJWCR/ref=ppx_od_dt_b_asin_title_s01?ie=UTF8&amp;psc=1"> grace and stella Under Eye Mask-Reduce Dark Circles, Puffy Eyes, Undereye Bags, Wrinkles-Gel Under Eye Patches, Vegan Cruelty-Free Self Care (72 Pairs, Gold, Pink &amp; Blue) </a>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-secondary"> Manufacturer: Grace &amp; Stella, support@graceandstella.com </span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-secondary"> Sold by: <a class="a-link-normal" href="/gp/help/seller/at-a-glance.html/ref=ppx_od_dt_b_sellerprofile_s01?ie=UTF8&amp;isAmazonFulfilled=1&amp;marketplaceSeller=1&amp;orderID=123-4567890-1234567&amp;seller=A1IRZ7664JSWXN"> Grace &amp; Stella Co.</a>
                            </span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small"></span>
                          </div>
                          <div class="a-row">
                            <span class="a-size-small a-color-price"> $45.95 </span>
                          </div>
                          <div class="a-row">
                            <span class="a-declarative" data-action="bia_button" data-bia_button="{}">
                              <span class="a-button a-spacing-mini a-button-primary yohtmlc-buy-it-again" id="a-autoid-8">
                                <span class="a-button-inner">
                                  <a href="/gp/buyagain/ref=ppx_od_dt_b_bia?ie=UTF8&amp;ats=eyJjdXN0b21lcklkIjoiQVVKQUoxMDRXTFpQMyIsImV4cGxpY2l0Q2FuZGlkYXRlcyI6IkIwOVJL%0ATkpXQ1IifQ%3D%3D%0A" aria-label="Buy it again" class="a-button-text" role="button" id="a-autoid-8-announce">
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
                    </div>
                  </div>
                </div>
                <div class="a-fixed-right-grid-col a-col-right" style="width:220px;margin-right:-220px;float:left;">
                  <div class="a-row">
                    <div class="a-button-stack yohtmlc-shipment-level-connections">
                      <span class="a-button a-button-normal a-spacing-mini a-button-primary" id="a-autoid-9">
                        <span class="a-button-inner">
                          <a id="View-Return/Refund-Status_2" href="/spr/returns/cart?_encoding=UTF8&amp;orderId=123-4567890-1234567&amp;ref_=ppx_od_dt_b_rr_status_s01" class="a-button-text" role="button"> View Return/Refund Status </a>
                        </span>
                      </span>
                      <span class="a-button a-button-normal a-spacing-mini a-button-base" id="a-autoid-10">
                        <span class="a-button-inner">
                          <a id="Leave-seller-feedback_2" href="/gp/feedback/leave-customer-feedback.html/ref=ppx_od_dt_b_sell_feed_s01?ie=UTF8&amp;order=123-4567890-1234567" class="a-button-text" role="button"> Leave seller feedback </a>
                        </span>
                      </span>
                      <span class="a-button a-button-normal a-spacing-mini a-button-base" id="a-autoid-11">
                        <span class="a-button-inner">
                          <a id="Write-a-product-review_2" href="/review/review-your-purchases/ref=ppx_od_dt_b_rev_prod_s01?_encoding=UTF8&amp;asins=B09RKNJWCR%2CB00CXK623E%2CB0BTTN6JQV%2CB07L9T8178%2CB08ZPLYGV6%2CB09P6RDQJ2&amp;channel=YAcc-wr" class="a-button-text" role="button"> Write a product review </a>
                        </span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="" data-component="deliveries"></div>
    <div class="" data-component="returns"></div>
  </div>
  <div class="" data-component="cancelled"></div>
          <!--&&&Portal&Delimiter&&&-->
  <!-- sp:end-feature:host-atf -->
  <!-- sp:feature:nav-btf -->
  <!-- NAVYAAN BTF START -->
        <!-- NAVYAAN BTF END -->
  <!-- sp:end-feature:nav-btf -->
  <!-- sp:feature:host-btf -->
</div>
"""

TEST_PARSE_ORDER_HTML_2 = """
<div id="orderDetails" class="a-section dynamic-width">
   <div class="a-cardui-deck" data-a-remove-top-gutter="" data-a-remove-bottom-gutter="" name="a-cardui-deck-autoname-0">
      <div class="a-teaser-describedby-collapsed a-hidden" id="a-cardui-deck-autoname-0-teaser-describedby-collapsed">Brief content visible, double tap to read full content.</div>
      <div class="a-teaser-describedby-expanded a-hidden" id="a-cardui-deck-autoname-0-teaser-describedby-expanded">Full content visible, double tap to read brief content.</div>
      <div class="a-cardui" data-a-card-type="basic" name="a-cardui-deck-autoname-0-card0">
         <div class="a-cardui-body">
            <div class="" data-component="default">
               <div class="" data-component="debugBanner">
               </div>
               <div class="" data-component="aapiDebug">
               </div>
               <div class="" data-component="ddtDebug">
               </div>
               <div class="" data-component="breadcrumb">
                  <div class="a-section a-spacing-base">
                     <ul class="a-unordered-list a-horizontal od-breadcrumbs">
                        <li class="od-breadcrumbs__crumb"><span class="a-list-item"><a class="a-link-normal" title="Return to Your Account" href="/gp/css/homepage.html/ref=ppx_hzod_bc_dt_b_ya_link">Your Account</a></span></li>
                        <li class="od-breadcrumbs__crumb od-breadcrumbs__crumb--divider"><span class="a-list-item">&gt;</span></li>
                        <li class="od-breadcrumbs__crumb"><span class="a-list-item"><a class="a-link-normal" title="Return to Your Orders" href="/gp/your-account/order-history/ref=ppx_hzod_bc_dt_b_oh_link">Your Orders</a></span></li>
                        <li class="od-breadcrumbs__crumb od-breadcrumbs__crumb--divider"><span class="a-list-item">&gt;</span></li>
                        <li class="od-breadcrumbs__crumb od-breadcrumbs__crumb--current"><span class="a-list-item"><span class="a-color-state">Order Details</span></span></li>
                     </ul>
                  </div>
               </div>
               <div class="" data-component="banner">
               </div>
               <div class="" data-component="returnsBanner">
               </div>
               <div class="" data-component="archivedMessage">
               </div>
               <div class="" data-component="title">
                  <div class="a-section">
                     <div class="a-row">
                        <div class="" data-component="titleLeftGrid">
                           <div class="a-column a-span6">
                              <div class="" data-component="orderDetailsTitle">
                                 <h1>Order Details</h1>
                              </div>
                           </div>
                        </div>
                        <div class="" data-component="titleRightGrid">
                           <div class="a-column a-span6 a-text-right a-span-last">
                              <div class="" data-component="brandLogo">
                              </div>
                           </div>
                        </div>
                     </div>
                  </div>
               </div>
               <div class="" data-component="orderDateInvoice">
                  <div class="a-row a-spacing-base">
                     <div class="a-column a-span9 a-spacing-top-mini">
                        <div class="a-row a-spacing-none">
                           <span class="order-date-invoice-item">
                           Ordered on December 17, 2024
                           <i class="a-icon a-icon-text-separator" role="img"></i>
                           </span>
                           <span class="order-date-invoice-item">
                           Order#
                           <bdi dir="ltr">123-4567890-1234567</bdi>
                           </span>
                        </div>
                     </div>
                     <div class="a-column a-span3 a-text-right a-spacing-top-none hide-if-no-js a-span-last">
                        <div class="a-row a-spacing-none">
                           <ul class="a-unordered-list a-nostyle a-vertical">
                              <li><span class="a-list-item">
                                 Amazon.com.ca, Inc.
                                 </span>
                              </li>
                              <li><span class="a-list-item">
                                 GST/HST - 85730 5932 RT0001
                                 </span>
                              </li>
                              <li><span class="a-list-item">
                                 QST - 1201187016 TQ0001
                                 </span>
                              </li>
                           </ul>
                           <div class="a-popover-preload" id="a-popover-invoiceLinks">
                              <ul class="a-unordered-list a-vertical a-nowrap">
                                 <li><span class="a-list-item">
                                    <a class="a-link-normal" href="/gp/css/summary/print.html/ref=ppx_od_dt_b_invoice?ie=UTF8&amp;orderID=123-4567890-1234567">
                                    Printable Order Summary
                                    </a>
                                    </span>
                                 </li>
                                 <li><span class="a-list-item">
                                    <a class="a-link-normal" href="/gp/help/customer/display.html/ref=ppx_od_dt_b_legal_invoice_help?ie=UTF8&amp;nodeId=201516020">
                                    Invoice not available. Learn more.
                                    </a>
                                    </span>
                                 </li>
                              </ul>
                           </div>
                           <span class="a-declarative" data-action="a-popover" data-a-popover="{&quot;name&quot;:&quot;invoiceLinks&quot;,&quot;position&quot;:&quot;triggerBottom&quot;,&quot;activate&quot;:&quot;onclick&quot;}">
                           <a href="javascript:void(0)" class="a-popover-trigger a-declarative">
                           <span class="a-size-medium">Invoice</span>
                           <i class="a-icon a-icon-popover"></i></a>
                           </span>
                        </div>
                     </div>
                  </div>
                  <div class="a-row a-spacing-base hide-if-js">
                     <div class="a-column a-span12 a-spacing-top-mini">
                        <ul class="a-unordered-list a-nostyle a-vertical">
                           <li><span class="a-list-item">
                              Amazon.com.ca, Inc.
                              </span>
                           </li>
                           <li><span class="a-list-item">
                              GST/HST - 85730 5932 RT0001
                              </span>
                           </li>
                           <li><span class="a-list-item">
                              QST - 1201187016 TQ0001
                              </span>
                           </li>
                        </ul>
                        <ul class="a-unordered-list a-nostyle a-vertical">
                           <li><span class="a-list-item">
                              <a class="a-link-normal" href="/gp/css/summary/print.html/ref=ppx_od_dt_b_invoice?ie=UTF8&amp;orderID=123-4567890-1234567">
                              Printable Order Summary
                              </a>
                              </span>
                           </li>
                           <li><span class="a-list-item">
                              <a class="a-link-normal" href="/gp/help/customer/display.html/ref=ppx_od_dt_b_legal_invoice_help?ie=UTF8&amp;nodeId=201516020">
                              Invoice not available. Learn more.
                              </a>
                              </span>
                           </li>
                        </ul>
                     </div>
                  </div>
               </div>
               <div class="" data-component="mfaMessage">
               </div>
               <div class="" data-component="orderSummary">
                  <div class="a-box-group a-spacing-base">
                     <div class="a-box">
                        <div class="a-box-inner">
                           <div class="a-fixed-right-grid">
                              <div class="a-fixed-right-grid-inner" style="padding-right:260px">
                                 <div class="a-fixed-right-grid-col a-col-left" style="padding-right:0%;float:left;">
                                    <div class="a-row">
                                       <div class="a-column a-span5">
                                          <div class="" data-component="paymentMethod">
                                             <div data-pmts-component-id="pp-fLSs7N-1" class="a-row pmts-portal-root-wuUKv496Eji9 pmts-portal-component pmts-portal-components-pp-fLSs7N-1">
                                                <div class="a-column a-span12 pmts-payment-instrument-billing-address">
                                                   <div data-pmts-component-id="pp-fLSs7N-2" class="a-row a-spacing-small pmts-portal-component pmts-portal-components-pp-fLSs7N-2">
                                                      <div class="a-row pmts-payments-instrument-header">
                                                         <h5>Payment Methods</h5>
                                                      </div>
                                                      <div class="a-row pmts-payments-instrument-details">
                                                         <ul class="a-unordered-list a-nostyle a-vertical no-bullet-list pmts-payments-instrument-list">
                                                            <li class="a-spacing-micro pmts-payments-instrument-detail-box-paystationpaymentmethod"><span class="a-list-item"><img alt="Mastercard" src="https://m.media-amazon.com/images/G/15/payments-portal/r1/issuer-images/mc._CB404661596_.gif" class="pmts-payment-credit-card-instrument-logo" height="23px" width="34px"><span class="a-letter-space"></span>CC<span class="a-letter-space"></span><span class="a-color-base">ending in 1234</span></span></li>
                                                         </ul>
                                                      </div>
                                                   </div>
                                                </div>
                                             </div>
                                             <link rel="stylesheet" type="text/css" href="https://m.media-amazon.com/images/I/11STWhdvr1L._RC|01tEjLkP-OL.css,21pZ9-tDsfL.css,01gqZiFs-tL.css,116LWdTN6UL.css,01cq16REt9L.css,01qk4TdW33L.css,11cVF3U-9BL.css,01cxjPaaTNL.css,01l0V3645dL.css,01SJRGuZivL.css,21jGj3aJ6ZL.css,11HEveYPS1L.css,01hOHsbn7OL.css,01IsDXoRrML.css,21tuuSEU3FL.css,01hIZRtcaHL.css,01NGxBoTbmL.css,01Mv8eppKAL.css,21TuFm4rvyL.css,11G1qAKAppL.css,01uakdML80L.css,01uHZesS5LL.css,11MhOiv1rNL.css,01rKSjRRIdL.css,018M3caCSzL.css,01Rgr3O5jgL.css,61PdPZU+9CL.css,01xniGkbKHL.css,01BUQQ2AAFL.css,11+KVSh5kaL.css,018GGCZ05rL.css,01RVwf5E26L.css,018QFljl9NL.css,01RKPCJHpeL.css,01gtkpxWIOL.css,012HRkWTMYL.css,01zEhgDPWUL.css,01le4Wlx71L.css,01NfyFypiAL.css,01x1gcd+b6L.css,21H4c3YVAzL.css,11uTQeLDHRL.css,01vSTBFdADL.css,21F2KqvWKoL.css,01X3lCf9VVL.css,01K72ZPRhdL.css,01CW6WWqlzL.css,01Kz8HcbaSL.css,1192eqsMCTL.css,01735fiNhpL.css,01W9cE2pBBL.css,31fUQODWjBL.css,01ENy2AhhHL.css,01lnEwmkCOL.css,01Epd5A5L9L.css,01i7-FZ2dbL.css,01ONHh8S9QL.css,01NDW5IRowL.css,01Jrep1-A8L.css,013mx6I5MjL.css,01DR-IGztZL.css,01oed2b7XHL.css,21nMzYiVcGL.css,01YgiH4056L.css,01-BlL5QIGL.css,01dkJYlUMlL.css,013gNYW5EZL.css,01Xbi2zDI3L.css,01B8WX2PjrL.css,01Z42xKR4FL.css,0139uaPyFCL.css,01Gtbyceb8L.css,0167aosbt1L.css_.css">
                                          </div>
                                       </div>
                                    </div>
                                 </div>
                                 <div class="a-fixed-right-grid-col a-col-right" style="width:260px;margin-right:-260px;float:left;">
                                    <div class="" data-component="orderSubtotals">
                                       <h5 class="a-spacing-micro a-text-left">
                                          Order Summary
                                       </h5>
                                       <div class="a-row">
                                          <div class="a-column a-span7 a-text-left">
                                             <span class="a-color-base">
                                             Item(s) Subtotal:
                                             </span>
                                          </div>
                                          <div class="a-column a-span5 a-text-right a-span-last">
                                             <span class="a-color-base">
                                             $10.00
                                             </span>
                                          </div>
                                       </div>
                                       <div class="a-row a-spacing-mini"></div>
                                       <div class="a-row">
                                          <div class="a-column a-span7 a-text-left">
                                             <span class="a-color-base">
                                             Total before tax:
                                             </span>
                                          </div>
                                          <div class="a-column a-span5 a-text-right a-span-last">
                                             <span class="a-color-base">
                                             $10.00
                                             </span>
                                          </div>
                                       </div>
                                       <div class="a-row">
                                          <div class="a-column a-span7 a-text-left">
                                             <span class="a-color-base">
                                             Estimated GST/HST:
                                             </span>
                                          </div>
                                          <div class="a-column a-span5 a-text-right a-span-last">
                                             <span class="a-color-base">
                                             $0.00
                                             </span>
                                          </div>
                                       </div>
                                       <div class="a-row">
                                          <div class="a-column a-span7 a-text-left">
                                             <span class="a-color-base">
                                             Estimated PST/RST/QST:
                                             </span>
                                          </div>
                                          <div class="a-column a-span5 a-text-right a-span-last">
                                             <span class="a-color-base">
                                             $0.00
                                             </span>
                                          </div>
                                       </div>
                                       <div class="a-row a-spacing-mini"></div>
                                       <div class="a-row">
                                          <div class="a-column a-span7 a-text-left">
                                             <span class="a-color-base a-text-bold">
                                             Grand Total:
                                             </span>
                                          </div>
                                          <div class="a-column a-span5 a-text-right a-span-last">
                                             <span class="a-color-base a-text-bold">
                                             $10.00
                                             </span>
                                          </div>
                                       </div>
                                    </div>
                                    <div class="" data-component="chargeSummary">
                                    </div>
                                 </div>
                              </div>
                           </div>
                           <div class="" data-component="wirelessDeposits">
                           </div>
                        </div>
                     </div>
                  </div>
               </div>
               <div class="" data-component="orderCard">
               </div>
               <div class="" data-component="shipments">
                  <div class="a-box">
                     <div class="a-box-inner">
                        <div class="a-row shipment-top-row js-shipment-info-container">
                           <div style="margin-right:220px; padding-right:20px">
                              <div class="a-row">
                                 <span class="a-size-medium a-text-bold">
                                 Sent
                                 </span>
                              </div>
                           </div>
                           <div class="actions" style="width:220px;">
                           </div>
                        </div>
                        <div class="a-fixed-right-grid a-spacing-top-medium">
                           <div class="a-fixed-right-grid-inner a-grid-vertical-align a-grid-top">
                              <div class="a-fixed-right-grid-col a-col-left" style="padding-right:3.2%;float:left;">
                                 <div class="a-row">
                                    <div class="a-fixed-left-grid a-spacing-base">
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
                                    </div>
                                 </div>
                              </div>
                              <div class="a-fixed-right-grid-col a-col-right" style="width:220px;margin-right:-220px;float:left;">
                                 <div class="a-row">
                                    <div class="a-button-stack yohtmlc-shipment-level-connections">
                                       <span class="a-button a-button-normal a-spacing-mini a-button-base" id="a-autoid-0"><span class="a-button-inner"><a id="Print-Gift-Card(s)_1" href="/gp/gc/print/ref=ppx_od_dt_b_gc_print?ie=UTF8&amp;orderID=123-4567890-1234567&amp;referrer=ya&amp;sessionID=123-4567890-1234567" class="a-button-text" role="button">
                                       Print Gift Card(s)
                                       </a></span></span>
                                       <span class="a-declarative" data-action="a-modal" data-a-modal="{&quot;width&quot;:600,&quot;name&quot;:&quot;archive-order-modal&quot;,&quot;url&quot;:&quot;/gp/css/order-history/archive/archiveModal.html?orderId=123-4567890-1234567&amp;shellOrderId=&quot;,&quot;header&quot;:&quot;Archive this order&quot;}">
                                       <span class="a-button a-button-normal a-spacing-mini a-button-base" id="a-autoid-1"><span class="a-button-inner"><a id="Archive-order_1" href="/gp/css/order-history/archive/ref=ppx_od_dt_b_archive_order?ie=UTF8&amp;archiveRequest=1&amp;orderIds=123-4567890-1234567&amp;token=123-4567890-1234567" class="a-button-text" role="button">
                                       Archive order
                                       </a></span></span>
                                       </span>
                                    </div>
                                 </div>
                              </div>
                           </div>
                        </div>
                     </div>
                  </div>
               </div>
               <div class="" data-component="deliveries">
               </div>
               <div class="" data-component="returns">
               </div>
            </div>
            <div class="" data-component="cancelled">
            </div>
         </div>
      </div>
   </div>
</div>
"""
