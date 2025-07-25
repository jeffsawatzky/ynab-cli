from decimal import Decimal

import pytest
from bs4 import BeautifulSoup
from httpx import URL

from ynab_cli.adapters.amazon.scrapers.refunds import RefundsScraper


@pytest.mark.anyio
async def test_scrape__success() -> None:
    # GIVEN
    fixture = TEST_PARSE_REFUNDS_HTML
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = RefundsScraper()
    refunds = []
    async_iter = await sut.scrape(URL("https://www.amazon.com"), html)
    async for refund in async_iter:
        refunds.append(refund)

    # THEN
    assert len(refunds) == 1
    assert refunds[0].order_id == "702-2870979-3753811"
    assert refunds[0].product_id == "B0BC1984LV"
    assert refunds[0].refund_total == Decimal("12.76")


TEST_PARSE_REFUNDS_HTML = """
<div id="rex-items-section-expanded-view-celWidget" class="celwidget" cel_widget_id="rex-items-section-expanded-view" data-csa-c-id="nonj4l-fxye84-jnw5a7-rmzcep" data-cel-widget="rex-items-section-expanded-view">
  <script type="a-state" data-a-state="{&quot;key&quot;:&quot;eventDataForItemsV2&quot;}">{"jhlmlphmrrluump-Qvrt8b9BY-consumed":{"unitIdToUnitDataMap":"{\\"miq://document:1.0/Contract/amazon:1.0/Unit:1.0/9d370cf0-b8f8-4cc1-808c-808ec900a65c#8ffd804d-1d19-41ac-a49f-a6837b650a50\\":{\\"asin\\":\\"B0BC1984LV\\"}}","orderId":"702-2870979-3753811","returnability":"CONSUMED","unitGroupIdToUnitGroupDataMap":"{}","subUnitGroups":"[]","subUnitIds":"[]"},"jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable":{"unitIdToUnitDataMap":"{\\"miq://document:1.0/AssociatedContract/amazon:1.0/Unit:1.0/A2EUQ1WTGCTBG2#702-2870979-3753811#FL#1729745400602270964#1\\":{\\"asin\\":\\"B08SF725S3\\"}}","orderId":"702-2870979-3753811","returnability":"SELF_SERVICEABLE","unitGroupIdToUnitGroupDataMap":"{}","subUnitGroups":"[]","subUnitIds":"[]"},"jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable":{"unitIdToUnitDataMap":"{\\"miq://document:1.0/AssociatedContract/amazon:1.0/Unit:1.0/A2EUQ1WTGCTBG2#702-2870979-3753811#FL#1729745400602269964#1\\":{\\"asin\\":\\"B0CL75VSHS\\"}}","orderId":"702-2870979-3753811","returnability":"SELF_SERVICEABLE","unitGroupIdToUnitGroupDataMap":"{}","subUnitGroups":"[]","subUnitIds":"[]"}}</script>
  <script type="a-state" data-a-state="{&quot;key&quot;:&quot;itemsPageCommonDataV2&quot;}">{"abuseRiskSignal":"","subPageType":"SPRLandingPage"}</script>
  <div class="a-section">
    <h1>Return/Refund Status</h1>
  </div>
  <div data-actor-behavior-id="banner-actor-behaviour" data-actor-configuration-id="banner-actor-configuration" id="ItemsSectionBulkBannerElement" class="a-box a-alert a-alert-error stiti-actor aok-hidden alert-banner-content" role="alert">
    <div class="a-box-inner a-alert-container">
      <i class="a-icon a-icon-alert"></i>
      <div class="a-alert-content">
        <span> You can return up to 250 quantities at a time. </span>
      </div>
    </div>
  </div>
  <form id="items-section-form-v2" method="post" action="/spr/returns/resolutions" class="items-section-form-v2">
    <div id="orc-returning-items-section" data-actor-behavior-id="item-selection-actor-behavior" data-actor-configuration-id="item-selection-actor-configuration" data-instance-id="orc-returning-items-section" data-items-post-url="/spr/returns/resolutions" aria-label="Return/Refund Status" class="a-section stiti-actor" role="radiogroup">
      <div class="a-section"></div>
      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-orc-item" data-item-key="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-should-preselect-item="false" class="a-section orc-item">
        <div class="a-row">
          <div class="a-column a-span1">
            <div class="a-section a-spacing-top-extra-large a-padding-medium">
              <div data-a-input-name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-orc-item-selection-checkbox" data-item-key="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" class="a-checkbox orc-item-selection-checkbox">
                <label for="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-orc-item-selection-checkbox">
                  <input id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-orc-item-selection-checkbox" type="checkbox" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-orc-item-selection-checkbox" value="" aria-label="ClIF BAR, Variety Pack, Individually...">
                  <i class="a-icon a-icon-checkbox"></i>
                  <span class="a-label a-checkbox-label">
                    <label aria-labelledby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-itemDetails" class="a-form-label"></label>
                  </span>
                </label>
              </div>
            </div>
          </div>
          <div data-item-key="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" class="a-column a-span6 orc-returnable-item-details">
            <div class="a-row a-grid-vertical-align a-grid-center">
              <div class="a-column a-span3">
                <div class="a-section a-padding-mini a-text-center">
                  <div class="a-row">
                    <img alt="" src="https://m.media-amazon.com/images/I/91YMNRcUaHL._AC_._SS160_.jpg">
                  </div>
                  <div class="a-row">
                    <span class="a-declarative" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;closeButton&quot;:&quot;true&quot;,&quot;dataStrategy&quot;:&quot;preload&quot;,&quot;activate&quot;:&quot;onmouseover&quot;,&quot;name&quot;:&quot;jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-itemDetails-popover&quot;,&quot;header&quot;:&quot;&quot;,&quot;position&quot;:&quot;triggerTop&quot;,&quot;popoverLabel&quot;:&quot;Details&quot;,&quot;url&quot;:&quot;&quot;}" data-csa-c-id="qkgglb-hh9gcp-92hkyj-rq8wl2">
                      <a href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative">
                        <span aria-label="Product details for ClIF BAR, Variety Pack, Individually..." class="a-size-small"> Details </span>
                        <i class="a-icon a-icon-popover"></i>
                      </a>
                    </span>
                    <div class="a-popover-preload" id="a-popover-jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-itemDetails-popover">
                      <h4 class="a-size-medium"> ClIF BAR, Variety Pack, Individually...</h4>
                      <div class="a-row">
                        <span class="a-size-small"> Size: </span>
                        <span class="a-size-small"> 68 g (Pack of 16) </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Order #: </span>
                        <span class="a-size-small"> 702-2870979-3753811 </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Sold by: </span>
                        <span class="a-size-small"> Amazon.com.ca ULC </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Quantity: </span>
                        <span class="a-size-small"> 1 </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Item price: </span>
                        <span class="a-size-small"> $29.29 </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="a-column a-span8 a-spacing-top-small a-span-last">
                <div class="a-row">
                  <span class="a-size-base a-text-bold"> ClIF BAR, Variety Pack, Individually... </span>
                </div>
                <div class="a-row">
                  <span class="a-size-small"> Size: </span>
                  <span class="a-size-small"> 68 g (Pack of 16) </span>
                </div>
                <div class="a-row">
                  <span class="a-size-small"> $29.29 </span>
                </div>
                <div class="a-row"></div>
              </div>
            </div>
          </div>
          <div class="a-column a-span5 a-span-last">
            <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-selfserviceable-item-form-fields" class="a-section a-spacing-top-extra-large">
              <div class="a-section orc-quantity-selection-widget"></div>
              <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionnaire-widget" data-actor-behavior-id="questionnaire-actor-behavior" data-actor-configuration-id="questionnaire-actor-configuration" data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-instance-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionnaire-widget" data-is-for-fallback-questionnaire="false" data-primary-question-set-id="AmazonDefault" data-questionnaire-json="{&quot;additionalComments&quot;:{&quot;values&quot;:[{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-optional&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_OPTIONAL&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;displayableStringId&quot;:&quot;orc-describe-whats-wrong-with-website-v1&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;displayableStringId&quot;:&quot;orc-name-of-item-received-in-error_56336&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED_ITEM_RECEIVED_IN_ERROR&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;displayableStringId&quot;:&quot;orc-name-of-store-and-price_56337&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED_STORE_AND_PRICE&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;displayableStringId&quot;:&quot;orc-describe-whats-wrong-with-item_57802&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED&quot;}],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalCommentList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalCommentList&quot;},&quot;questions&quot;:{&quot;values&quot;:[{&quot;questionId&quot;:&quot;Q_AmazonDefault&quot;,&quot;displayableStringId&quot;:&quot;orc-return-reason&quot;,&quot;responseOptionIds&quot;:{&quot;values&quot;:[&quot;RO_CR-UNAUTHORIZED_PURCHASE&quot;,&quot;RO_CR-QUALITY_UNACCEPTABLE&quot;,&quot;RO_CR-DAMAGED_BY_CARRIER&quot;,&quot;RO_CR-ORDERED_WRONG_ITEM&quot;,&quot;RO_CR-SWITCHEROO&quot;,&quot;RO_CR-NOT_COMPATIBLE&quot;,&quot;RO_CR-UNWANTED_ITEM&quot;,&quot;RO_CR-DAMAGED_BY_FC&quot;,&quot;RO_CR-FOUND_BETTER_PRICE&quot;,&quot;RO_CR-DEFECTIVE&quot;,&quot;RO_CR-MISSING_PARTS&quot;,&quot;RO_CR-EXTRA_ITEM&quot;,&quot;RO_AMZ-PG-BAD-DESC&quot;,&quot;RO_CR-MISSED_ESTIMATED_DELIVERY&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.Question&quot;,&quot;java.lang.Object&quot;],&quot;isOptional&quot;:false,&quot;questionType&quot;:&quot;SingleChoice&quot;,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.Question&quot;}],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.QuestionList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.QuestionList&quot;},&quot;responseOptions&quot;:{&quot;values&quot;:[{&quot;displayableStringId&quot;:&quot;orc_rc_CR-QUALITY_UNACCEPTABLE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-QUALITY_UNACCEPTABLE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:2,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-DEFECTIVE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-DEFECTIVE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:10,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-EXTRA_ITEM&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-EXTRA_ITEM&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:12,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_ITEM_RECEIVED_IN_ERROR&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-MISSED_ESTIMATED_DELIVERY&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-MISSED_ESTIMATED_DELIVERY&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:14,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-FOUND_BETTER_PRICE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-FOUND_BETTER_PRICE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:9,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_STORE_AND_PRICE&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-UNWANTED_ITEM&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-UNWANTED_ITEM&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:7,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-UNAUTHORIZED_PURCHASE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-UNAUTHORIZED_PURCHASE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:1,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_OPTIONAL&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-DAMAGED_BY_CARRIER&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-DAMAGED_BY_CARRIER&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:3,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_AMZ-PG-BAD-DESC&quot;,&quot;responseOptionId&quot;:&quot;RO_AMZ-PG-BAD-DESC&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:13,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-ORDERED_WRONG_ITEM&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-ORDERED_WRONG_ITEM&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:4,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_OPTIONAL&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-NOT_COMPATIBLE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-NOT_COMPATIBLE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:6,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-DAMAGED_BY_FC&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-DAMAGED_BY_FC&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:8,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-SWITCHEROO&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-SWITCHEROO&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:5,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_ITEM_RECEIVED_IN_ERROR&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-MISSING_PARTS&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-MISSING_PARTS&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:11,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;}],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOptionList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOptionList&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.Questionnaire&quot;,&quot;java.lang.Object&quot;],&quot;questionSets&quot;:{&quot;values&quot;:[{&quot;questionSetId&quot;:&quot;AmazonDefault&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.QuestionSet&quot;,&quot;java.lang.Object&quot;],&quot;questionIds&quot;:{&quot;values&quot;:[&quot;Q_AmazonDefault&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.QuestionSet&quot;}],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.QuestionSetList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.QuestionSetList&quot;},&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.Questionnaire&quot;,&quot;primaryQuestionSetId&quot;:&quot;AmazonDefault&quot;}" data-resolvable-response-option-subscribers="{&quot;AmazonDefault-Q_AmazonDefault&quot;:{}}" data-subscribed-question-set-registry="{&quot;AmazonDefault&quot;:{&quot;Q_AmazonDefault&quot;:[]}}" class="a-section a-spacing-top-extra-large questionnaire-widget stiti-actor">
                <div class="a-row">
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionnaire-widget-questions-and-responses" class="a-column a-span12">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-questionnaire-widget" class="a-row">
                      <div class="a-column a-span12">
                        <div class="a-row a-spacing-base">
                          <span> Why are you returning this? </span>
                        </div>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-section" class="a-row a-spacing-mini">
                          <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-data-section" class="a-column a-span12 a-spacing-base">
                            <span class="a-dropdown-container">
                              <select name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget" autocomplete="off" role="combobox" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-native-dropdown" tabindex="0" data-action="a-dropdown-select" aria-required="true" class="a-native-dropdown a-button-span10 a-declarative">
                                <option class="a-prompt" value="">Choose a response</option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-UNAUTHORIZED_PURCHASE" data-response-option-rank="1" value="RO_CR-UNAUTHORIZED_PURCHASE" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-UNAUTHORIZED_PURCHASE-native-dropdown-option"> Didn't approve purchase </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-QUALITY_UNACCEPTABLE" data-response-option-rank="2" value="RO_CR-QUALITY_UNACCEPTABLE" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-QUALITY_UNACCEPTABLE-native-dropdown-option"> Performance or quality not adequate </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-DAMAGED_BY_CARRIER" data-response-option-rank="3" value="RO_CR-DAMAGED_BY_CARRIER" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-DAMAGED_BY_CARRIER-native-dropdown-option"> Product and shipping box both damaged </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-ORDERED_WRONG_ITEM" data-response-option-rank="4" value="RO_CR-ORDERED_WRONG_ITEM" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-ORDERED_WRONG_ITEM-native-dropdown-option"> Bought by mistake </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-SWITCHEROO" data-response-option-rank="5" value="RO_CR-SWITCHEROO" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-SWITCHEROO-native-dropdown-option"> Wrong item was sent </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-NOT_COMPATIBLE" data-response-option-rank="6" value="RO_CR-NOT_COMPATIBLE" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-NOT_COMPATIBLE-native-dropdown-option"> Incompatible or not useful </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-UNWANTED_ITEM" data-response-option-rank="7" value="RO_CR-UNWANTED_ITEM" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-UNWANTED_ITEM-native-dropdown-option"> No longer needed </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-DAMAGED_BY_FC" data-response-option-rank="8" value="RO_CR-DAMAGED_BY_FC" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-DAMAGED_BY_FC-native-dropdown-option"> Product damaged, but shipping box OK </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-FOUND_BETTER_PRICE" data-response-option-rank="9" value="RO_CR-FOUND_BETTER_PRICE" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-FOUND_BETTER_PRICE-native-dropdown-option"> Better price available </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-DEFECTIVE" data-response-option-rank="10" value="RO_CR-DEFECTIVE" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-DEFECTIVE-native-dropdown-option"> Item defective or doesn't work </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-MISSING_PARTS" data-response-option-rank="11" value="RO_CR-MISSING_PARTS" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-MISSING_PARTS-native-dropdown-option"> Missing parts or accessories </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-EXTRA_ITEM" data-response-option-rank="12" value="RO_CR-EXTRA_ITEM" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-EXTRA_ITEM-native-dropdown-option"> Received extra item I didn't buy (no refund needed) </option>
                                <option data-response-option-displayable-string-id="orc_rc_AMZ-PG-BAD-DESC" data-response-option-rank="13" value="RO_AMZ-PG-BAD-DESC" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_AMZ-PG-BAD-DESC-native-dropdown-option"> Inaccurate website description </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-MISSED_ESTIMATED_DELIVERY" data-response-option-rank="14" value="RO_CR-MISSED_ESTIMATED_DELIVERY" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-MISSED_ESTIMATED_DELIVERY-native-dropdown-option"> Item arrived too late </option>
                              </select>
                              <span tabindex="-1" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-dropdown" data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-is-question-optional="false" data-primary-question-set-id="AmazonDefault" data-question-element-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-question-set-tier="first" data-a-class="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionnaire-widget-question questionnaire-widget-question" class="a-button a-button-dropdown a-button-span10 jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionnaire-widget-question questionnaire-widget-question" aria-hidden="true" style="min-width: 0%;">
                                <span class="a-button-inner">
                                  <span class="a-button-text a-declarative" data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-csa-c-func-deps="aui-da-a-dropdown-button" data-csa-c-type="widget" data-csa-interaction-events="click" data-is-question-optional="false" data-primary-question-set-id="AmazonDefault" data-question-element-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-question-set-tier="first" data-action="a-dropdown-button" aria-hidden="true" data-csa-c-id="4mfmzp-dlsnrx-cggqsp-cknyfr">
                                    <span class="a-dropdown-prompt">Choose a response</span>
                                  </span>
                                  <i class="a-icon a-icon-dropdown"></i>
                                </span>
                              </span>
                            </span>
                          </div>
                          <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-return-reason-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                            <div class="a-box-inner a-alert-container">
                              <i class="a-icon a-icon-alert"></i>
                              <div class="a-alert-content"> Please select a reason for initiating return </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="a-row"></div>
              <div class="a-row">
                <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget" data-actor-behavior-id="comments-actor-behavior" data-actor-configuration-id="comments-actor-configuration" data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-instance-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget" class="a-section stiti-actor">
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-UNAUTHORIZED_PURCHASE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-section" data-additional-comment-id="AC_OPTIONAL" data-is-comment-required="false" class="a-section">
                      <span> Comments (optional): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL" data-comment-local-id="AC_OPTIONAL" data-is-comment-description-overridden="false" data-is-comment-required="false" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-UNAUTHORIZED_PURCHASE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (optional):" aria-required="false"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-QUALITY_UNACCEPTABLE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-QUALITY_UNACCEPTABLE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DAMAGED_BY_CARRIER" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DAMAGED_BY_CARRIER" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-ORDERED_WRONG_ITEM" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-section" data-additional-comment-id="AC_OPTIONAL" data-is-comment-required="false" class="a-section">
                      <span> Comments (optional): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL" data-comment-local-id="AC_OPTIONAL" data-is-comment-description-overridden="false" data-is-comment-required="false" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-ORDERED_WRONG_ITEM" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (optional):" aria-required="false"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-SWITCHEROO" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-section" data-additional-comment-id="AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-comment-local-id="AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Provide the name of the item received in error:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-SWITCHEROO" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Provide the name of the item received in error:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-NOT_COMPATIBLE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-NOT_COMPATIBLE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-UNWANTED_ITEM" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-section" data-additional-comment-id="AC_REQUIRED" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED" data-comment-local-id="AC_REQUIRED" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-UNWANTED_ITEM" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DAMAGED_BY_FC" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DAMAGED_BY_FC" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-FOUND_BETTER_PRICE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-section" data-additional-comment-id="AC_REQUIRED_STORE_AND_PRICE" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE" data-comment-local-id="AC_REQUIRED_STORE_AND_PRICE" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="List the name of the store and the lower price offered:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-FOUND_BETTER_PRICE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="List the name of the store and the lower price offered:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DEFECTIVE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DEFECTIVE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-MISSING_PARTS" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-MISSING_PARTS" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-EXTRA_ITEM" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-section" data-additional-comment-id="AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-comment-local-id="AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Provide the name of the item received in error:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-EXTRA_ITEM" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Provide the name of the item received in error:" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_AMZ-PG-BAD-DESC" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Explain what's wrong with the website description" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_AMZ-PG-BAD-DESC" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Explain what's wrong with the website description" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-MISSED_ESTIMATED_DELIVERY" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-section" data-additional-comment-id="AC_REQUIRED" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-comment-text-box-section" class="a-section jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED" data-comment-local-id="AC_REQUIRED" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-MISSED_ESTIMATED_DELIVERY" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED" name="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED" aria-describedby="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-read-only-section" class="a-section aok-hidden jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-comment-section-read-only-section">
                        <span id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-pii-note" class="a-section aok-hidden">
                    <span class="a-size-base a-color-secondary">
                      <b>NOTE:</b> We aren't able to offer policy exceptions in response to comments. Do not include personal information as these comments may be shared with external service providers to identify product defects. </span>
                  </div>
                </div>
              </div>
              <div id="jhlmlphmrrlutsp-QW9tlDQdY-self_serviceable-llm-question-main-section" class="a-section a-spacing-none llm-question-main-section"></div>
            </div>
          </div>
        </div>
        <hr aria-hidden="true" class="a-spacing-top-large a-divider-normal">
      </div>
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
                    <span class="a-declarative" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;closeButton&quot;:&quot;true&quot;,&quot;dataStrategy&quot;:&quot;preload&quot;,&quot;activate&quot;:&quot;onmouseover&quot;,&quot;name&quot;:&quot;jhlmlphmrrluump-Qvrt8b9BY-consumed-itemDetails-popover&quot;,&quot;header&quot;:&quot;&quot;,&quot;position&quot;:&quot;triggerTop&quot;,&quot;popoverLabel&quot;:&quot;Details&quot;,&quot;url&quot;:&quot;&quot;}" data-csa-c-id="tbk3pu-ql4zlv-vb8dzn-4r6d2s">
                      <a href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative">
                        <span aria-label="Product details for Choker Necklace for Women Layered Gold..." class="a-size-small"> Details </span>
                        <i class="a-icon a-icon-popover"></i>
                      </a>
                    </span>
                    <div class="a-popover-preload" id="a-popover-jhlmlphmrrluump-Qvrt8b9BY-consumed-itemDetails-popover">
                      <h4 class="a-size-medium"> Choker Necklace for Women Layered Gold...</h4>
                      <div class="a-row">
                        <span class="a-size-small"> Colour: </span>
                        <span class="a-size-small"> B:silver Coin Necklace </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Order #: </span>
                        <span class="a-size-small"> 702-2870979-3753811 </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Sold by: </span>
                        <span class="a-size-small"> YANCHUN JEWELLRY </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Quantity: </span>
                        <span class="a-size-small"> 1 </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Item price: </span>
                        <span class="a-size-small"> $11.29 </span>
                      </div>
                    </div>
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
      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-orc-item" data-item-key="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-should-preselect-item="false" class="a-section orc-item">
        <div class="a-row">
          <div class="a-column a-span1">
            <div class="a-section a-spacing-top-extra-large a-padding-medium">
              <div data-a-input-name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-orc-item-selection-checkbox" data-item-key="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" class="a-checkbox orc-item-selection-checkbox">
                <label for="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-orc-item-selection-checkbox">
                  <input id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-orc-item-selection-checkbox" type="checkbox" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-orc-item-selection-checkbox" value="" aria-label="Slimpal Heating Pad for Period Cramps,...">
                  <i class="a-icon a-icon-checkbox"></i>
                  <span class="a-label a-checkbox-label">
                    <label aria-labelledby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-itemDetails" class="a-form-label"></label>
                  </span>
                </label>
              </div>
            </div>
          </div>
          <div data-item-key="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" class="a-column a-span6 orc-returnable-item-details">
            <div class="a-row a-grid-vertical-align a-grid-center">
              <div class="a-column a-span3">
                <div class="a-section a-padding-mini a-text-center">
                  <div class="a-row">
                    <img alt="" src="https://m.media-amazon.com/images/I/718hd+cwSVL._AC_._SS160_.jpg">
                  </div>
                  <div class="a-row">
                    <span class="a-declarative" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;closeButton&quot;:&quot;true&quot;,&quot;dataStrategy&quot;:&quot;preload&quot;,&quot;activate&quot;:&quot;onmouseover&quot;,&quot;name&quot;:&quot;jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-itemDetails-popover&quot;,&quot;header&quot;:&quot;&quot;,&quot;position&quot;:&quot;triggerTop&quot;,&quot;popoverLabel&quot;:&quot;Details&quot;,&quot;url&quot;:&quot;&quot;}" data-csa-c-id="w1l6ug-9g14l9-i8aff1-92prkz">
                      <a href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative">
                        <span aria-label="Product details for Slimpal Heating Pad for Period Cramps,..." class="a-size-small"> Details </span>
                        <i class="a-icon a-icon-popover"></i>
                      </a>
                    </span>
                    <div class="a-popover-preload" id="a-popover-jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-itemDetails-popover">
                      <h4 class="a-size-medium"> Slimpal Heating Pad for Period Cramps,...</h4>
                      <div class="a-row">
                        <span class="a-size-small"> Size: </span>
                        <span class="a-size-small"> SPC023-S2 </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Colour: </span>
                        <span class="a-size-small"> Aqua </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Order #: </span>
                        <span class="a-size-small"> 702-2870979-3753811 </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Sold by: </span>
                        <span class="a-size-small"> Simply Fitness </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Quantity: </span>
                        <span class="a-size-small"> 1 </span>
                      </div>
                      <div class="a-row">
                        <span class="a-size-small"> Item price: </span>
                        <span class="a-size-small"> $33.99 </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="a-column a-span8 a-spacing-top-small a-span-last">
                <div class="a-row">
                  <span class="a-size-base a-text-bold"> Slimpal Heating Pad for Period Cramps,... </span>
                </div>
                <div class="a-row">
                  <span class="a-size-small"> Size: </span>
                  <span class="a-size-small"> SPC023-S2 </span>
                </div>
                <div class="a-row">
                  <span class="a-size-small"> Colour: </span>
                  <span class="a-size-small"> Aqua </span>
                </div>
                <div class="a-row">
                  <span class="a-size-small"> $33.99 </span>
                </div>
                <div class="a-row"></div>
              </div>
            </div>
          </div>
          <div class="a-column a-span5 a-span-last">
            <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-selfserviceable-item-form-fields" class="a-section a-spacing-top-extra-large aok-hidden">
              <div class="a-section orc-quantity-selection-widget"></div>
              <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionnaire-widget" data-actor-behavior-id="questionnaire-actor-behavior" data-actor-configuration-id="questionnaire-actor-configuration" data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-instance-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionnaire-widget" data-is-for-fallback-questionnaire="false" data-primary-question-set-id="AmazonDefault" data-questionnaire-json="{&quot;additionalComments&quot;:{&quot;values&quot;:[{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-optional&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_OPTIONAL&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;displayableStringId&quot;:&quot;orc-describe-whats-wrong-with-website-v1&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;displayableStringId&quot;:&quot;orc-name-of-item-received-in-error_56336&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED_ITEM_RECEIVED_IN_ERROR&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;displayableStringId&quot;:&quot;orc-name-of-store-and-price_56337&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED_STORE_AND_PRICE&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;displayableStringId&quot;:&quot;orc-describe-whats-wrong-with-item_57802&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;},{&quot;commentTitle&quot;:{&quot;displayableStringId&quot;:&quot;orc-comments-required&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentTitle&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;java.lang.Object&quot;],&quot;commentDescription&quot;:{&quot;maximumCommentLength&quot;:200,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.CommentDescription&quot;},&quot;isCommentRequired&quot;:true,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalComment&quot;,&quot;additionalCommentId&quot;:&quot;AC_REQUIRED&quot;}],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.AdditionalCommentList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.AdditionalCommentList&quot;},&quot;questions&quot;:{&quot;values&quot;:[{&quot;questionId&quot;:&quot;Q_AmazonDefault&quot;,&quot;displayableStringId&quot;:&quot;orc-return-reason&quot;,&quot;responseOptionIds&quot;:{&quot;values&quot;:[&quot;RO_CR-UNAUTHORIZED_PURCHASE&quot;,&quot;RO_CR-QUALITY_UNACCEPTABLE&quot;,&quot;RO_CR-DAMAGED_BY_CARRIER&quot;,&quot;RO_CR-ORDERED_WRONG_ITEM&quot;,&quot;RO_CR-SWITCHEROO&quot;,&quot;RO_CR-NOT_COMPATIBLE&quot;,&quot;RO_CR-UNWANTED_ITEM&quot;,&quot;RO_CR-DAMAGED_BY_FC&quot;,&quot;RO_CR-FOUND_BETTER_PRICE&quot;,&quot;RO_CR-DEFECTIVE&quot;,&quot;RO_CR-MISSING_PARTS&quot;,&quot;RO_CR-EXTRA_ITEM&quot;,&quot;RO_AMZ-PG-BAD-DESC&quot;,&quot;RO_CR-MISSED_ESTIMATED_DELIVERY&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.Question&quot;,&quot;java.lang.Object&quot;],&quot;isOptional&quot;:false,&quot;questionType&quot;:&quot;SingleChoice&quot;,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.Question&quot;}],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.QuestionList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.QuestionList&quot;},&quot;responseOptions&quot;:{&quot;values&quot;:[{&quot;displayableStringId&quot;:&quot;orc_rc_CR-QUALITY_UNACCEPTABLE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-QUALITY_UNACCEPTABLE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:2,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-DEFECTIVE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-DEFECTIVE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:10,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-EXTRA_ITEM&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-EXTRA_ITEM&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:12,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_ITEM_RECEIVED_IN_ERROR&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-MISSED_ESTIMATED_DELIVERY&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-MISSED_ESTIMATED_DELIVERY&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:14,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-FOUND_BETTER_PRICE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-FOUND_BETTER_PRICE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:9,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_STORE_AND_PRICE&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-UNWANTED_ITEM&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-UNWANTED_ITEM&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:7,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-UNAUTHORIZED_PURCHASE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-UNAUTHORIZED_PURCHASE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:1,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_OPTIONAL&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-DAMAGED_BY_CARRIER&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-DAMAGED_BY_CARRIER&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:3,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_AMZ-PG-BAD-DESC&quot;,&quot;responseOptionId&quot;:&quot;RO_AMZ-PG-BAD-DESC&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:13,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-ORDERED_WRONG_ITEM&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-ORDERED_WRONG_ITEM&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:4,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_OPTIONAL&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-NOT_COMPATIBLE&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-NOT_COMPATIBLE&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:6,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-DAMAGED_BY_FC&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-DAMAGED_BY_FC&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:8,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-SWITCHEROO&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-SWITCHEROO&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:5,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_ITEM_RECEIVED_IN_ERROR&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;},{&quot;displayableStringId&quot;:&quot;orc_rc_CR-MISSING_PARTS&quot;,&quot;responseOptionId&quot;:&quot;RO_CR-MISSING_PARTS&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;,&quot;java.lang.Object&quot;],&quot;rank&quot;:11,&quot;additionalCommentIds&quot;:{&quot;values&quot;:[&quot;AC_REQUIRED_WHAT_IS_WRONG&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;isDisplayableByDefault&quot;:false,&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOption&quot;}],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.ResponseOptionList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.ResponseOptionList&quot;},&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.Questionnaire&quot;,&quot;java.lang.Object&quot;],&quot;questionSets&quot;:{&quot;values&quot;:[{&quot;questionSetId&quot;:&quot;AmazonDefault&quot;,&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.QuestionSet&quot;,&quot;java.lang.Object&quot;],&quot;questionIds&quot;:{&quot;values&quot;:[&quot;Q_AmazonDefault&quot;],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.StringIdentifierList&quot;},&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.QuestionSet&quot;}],&quot;*classHierarchy*&quot;:[&quot;comet.aspect.ReturnReason.types.QuestionSetList&quot;,&quot;java.lang.Object&quot;],&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.QuestionSetList&quot;},&quot;*className*&quot;:&quot;comet.aspect.ReturnReason.types.Questionnaire&quot;,&quot;primaryQuestionSetId&quot;:&quot;AmazonDefault&quot;}" data-resolvable-response-option-subscribers="{&quot;AmazonDefault-Q_AmazonDefault&quot;:{}}" data-subscribed-question-set-registry="{&quot;AmazonDefault&quot;:{&quot;Q_AmazonDefault&quot;:[]}}" class="a-section a-spacing-top-extra-large questionnaire-widget stiti-actor">
                <div class="a-row">
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionnaire-widget-questions-and-responses" class="a-column a-span12">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-questionnaire-widget" class="a-row">
                      <div class="a-column a-span12">
                        <div class="a-row a-spacing-base">
                          <span> Why are you returning this? </span>
                        </div>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-section" class="a-row a-spacing-mini">
                          <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-data-section" class="a-column a-span12 a-spacing-base">
                            <span class="a-dropdown-container">
                              <select name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget" autocomplete="off" role="combobox" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-native-dropdown" tabindex="0" data-action="a-dropdown-select" aria-required="true" class="a-native-dropdown a-button-span10 a-declarative">
                                <option class="a-prompt" value="">Choose a response</option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-UNAUTHORIZED_PURCHASE" data-response-option-rank="1" value="RO_CR-UNAUTHORIZED_PURCHASE" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-UNAUTHORIZED_PURCHASE-native-dropdown-option"> Didn't approve purchase </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-QUALITY_UNACCEPTABLE" data-response-option-rank="2" value="RO_CR-QUALITY_UNACCEPTABLE" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-QUALITY_UNACCEPTABLE-native-dropdown-option"> Performance or quality not adequate </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-DAMAGED_BY_CARRIER" data-response-option-rank="3" value="RO_CR-DAMAGED_BY_CARRIER" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-DAMAGED_BY_CARRIER-native-dropdown-option"> Product and shipping box both damaged </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-ORDERED_WRONG_ITEM" data-response-option-rank="4" value="RO_CR-ORDERED_WRONG_ITEM" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-ORDERED_WRONG_ITEM-native-dropdown-option"> Bought by mistake </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-SWITCHEROO" data-response-option-rank="5" value="RO_CR-SWITCHEROO" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-SWITCHEROO-native-dropdown-option"> Wrong item was sent </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-NOT_COMPATIBLE" data-response-option-rank="6" value="RO_CR-NOT_COMPATIBLE" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-NOT_COMPATIBLE-native-dropdown-option"> Incompatible or not useful </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-UNWANTED_ITEM" data-response-option-rank="7" value="RO_CR-UNWANTED_ITEM" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-UNWANTED_ITEM-native-dropdown-option"> No longer needed </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-DAMAGED_BY_FC" data-response-option-rank="8" value="RO_CR-DAMAGED_BY_FC" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-DAMAGED_BY_FC-native-dropdown-option"> Product damaged, but shipping box OK </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-FOUND_BETTER_PRICE" data-response-option-rank="9" value="RO_CR-FOUND_BETTER_PRICE" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-FOUND_BETTER_PRICE-native-dropdown-option"> Better price available </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-DEFECTIVE" data-response-option-rank="10" value="RO_CR-DEFECTIVE" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-DEFECTIVE-native-dropdown-option"> Item defective or doesn't work </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-MISSING_PARTS" data-response-option-rank="11" value="RO_CR-MISSING_PARTS" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-MISSING_PARTS-native-dropdown-option"> Missing parts or accessories </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-EXTRA_ITEM" data-response-option-rank="12" value="RO_CR-EXTRA_ITEM" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-EXTRA_ITEM-native-dropdown-option"> Received extra item I didn't buy (no refund needed) </option>
                                <option data-response-option-displayable-string-id="orc_rc_AMZ-PG-BAD-DESC" data-response-option-rank="13" value="RO_AMZ-PG-BAD-DESC" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_AMZ-PG-BAD-DESC-native-dropdown-option"> Inaccurate website description </option>
                                <option data-response-option-displayable-string-id="orc_rc_CR-MISSED_ESTIMATED_DELIVERY" data-response-option-rank="14" value="RO_CR-MISSED_ESTIMATED_DELIVERY" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-RO_CR-MISSED_ESTIMATED_DELIVERY-native-dropdown-option"> Item arrived too late </option>
                              </select>
                              <span tabindex="-1" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-dropdown" data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-is-question-optional="false" data-primary-question-set-id="AmazonDefault" data-question-element-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-question-set-tier="first" data-a-class="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionnaire-widget-question questionnaire-widget-question" class="a-button a-button-dropdown a-button-span10 jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionnaire-widget-question questionnaire-widget-question" aria-hidden="true" style="min-width: 0%;">
                                <span class="a-button-inner">
                                  <span class="a-button-text a-declarative" data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-csa-c-func-deps="aui-da-a-dropdown-button" data-csa-c-type="widget" data-csa-interaction-events="click" data-is-question-optional="false" data-primary-question-set-id="AmazonDefault" data-question-element-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-question-set-tier="first" data-action="a-dropdown-button" aria-hidden="true" data-csa-c-id="bzz9x9-vyom7-eer3un-hssmzt">
                                    <span class="a-dropdown-prompt">Choose a response</span>
                                  </span>
                                  <i class="a-icon a-icon-dropdown"></i>
                                </span>
                              </span>
                            </span>
                          </div>
                          <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-questionSet-AmazonDefault-question-Q_AmazonDefault-questionnaire-widget-return-reason-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                            <div class="a-box-inner a-alert-container">
                              <i class="a-icon a-icon-alert"></i>
                              <div class="a-alert-content"> Please select a reason for initiating return </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="a-row"></div>
              <div class="a-row">
                <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget" data-actor-behavior-id="comments-actor-behavior" data-actor-configuration-id="comments-actor-configuration" data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-instance-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget" class="a-section stiti-actor">
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-UNAUTHORIZED_PURCHASE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-section" data-additional-comment-id="AC_OPTIONAL" data-is-comment-required="false" class="a-section">
                      <span> Comments (optional): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL" data-comment-local-id="AC_OPTIONAL" data-is-comment-description-overridden="false" data-is-comment-required="false" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-UNAUTHORIZED_PURCHASE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (optional):" aria-required="false"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNAUTHORIZED_PURCHASE-AC_OPTIONAL-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-QUALITY_UNACCEPTABLE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-QUALITY_UNACCEPTABLE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-QUALITY_UNACCEPTABLE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DAMAGED_BY_CARRIER" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DAMAGED_BY_CARRIER" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_CARRIER-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-ORDERED_WRONG_ITEM" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-section" data-additional-comment-id="AC_OPTIONAL" data-is-comment-required="false" class="a-section">
                      <span> Comments (optional): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL" data-comment-local-id="AC_OPTIONAL" data-is-comment-description-overridden="false" data-is-comment-required="false" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-ORDERED_WRONG_ITEM" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (optional):" aria-required="false"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-ORDERED_WRONG_ITEM-AC_OPTIONAL-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-SWITCHEROO" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-section" data-additional-comment-id="AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-comment-local-id="AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Provide the name of the item received in error:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-SWITCHEROO" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Provide the name of the item received in error:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-SWITCHEROO-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-NOT_COMPATIBLE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-NOT_COMPATIBLE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-NOT_COMPATIBLE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-UNWANTED_ITEM" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-section" data-additional-comment-id="AC_REQUIRED" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED" data-comment-local-id="AC_REQUIRED" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-UNWANTED_ITEM" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-UNWANTED_ITEM-AC_REQUIRED-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DAMAGED_BY_FC" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DAMAGED_BY_FC" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DAMAGED_BY_FC-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-FOUND_BETTER_PRICE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-section" data-additional-comment-id="AC_REQUIRED_STORE_AND_PRICE" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE" data-comment-local-id="AC_REQUIRED_STORE_AND_PRICE" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="List the name of the store and the lower price offered:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-FOUND_BETTER_PRICE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="List the name of the store and the lower price offered:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-FOUND_BETTER_PRICE-AC_REQUIRED_STORE_AND_PRICE-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DEFECTIVE" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-DEFECTIVE" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-DEFECTIVE-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-MISSING_PARTS" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Describe what's wrong with the item:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-MISSING_PARTS" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Describe what's wrong with the item:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSING_PARTS-AC_REQUIRED_WHAT_IS_WRONG-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-EXTRA_ITEM" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-section" data-additional-comment-id="AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-comment-local-id="AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Provide the name of the item received in error:" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-EXTRA_ITEM" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Provide the name of the item received in error:" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-EXTRA_ITEM-AC_REQUIRED_ITEM_RECEIVED_IN_ERROR-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_AMZ-PG-BAD-DESC" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-section" data-additional-comment-id="AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" data-comment-local-id="AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="Explain what's wrong with the website description" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_AMZ-PG-BAD-DESC" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" placeholder="Explain what's wrong with the website description" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_AMZ-PG-BAD-DESC-AC_REQUIRED_WHAT_IS_WRONG_WITH_WEBSITE-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-comment-section" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-MISSED_ESTIMATED_DELIVERY" class="a-section a-spacing-top-micro aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-comment-section">
                    <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-section" data-additional-comment-id="AC_REQUIRED" data-is-comment-required="true" class="a-section">
                      <span> Comments (required): </span>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-comment-text-box-section" class="a-section jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-comment-section-comment-text-box-section">
                        <div data-association-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable" data-comment-id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED" data-comment-local-id="AC_REQUIRED" data-is-comment-description-overridden="false" data-is-comment-required="true" data-llm-conversation-id="" data-max-length="200" data-original-aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" data-placeholder-string="" data-question-id="Q_AmazonDefault" data-question-set-id="AmazonDefault" data-response-option-id="RO_CR-MISSED_ESTIMATED_DELIVERY" aria-describedby="" aria-label="" aria-required="" class="a-input-text-wrapper jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-comments-widget-text-box comments-widget-text-box">
                          <textarea maxlength="200" id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED" name="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED" aria-describedby="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" aria-label="Comments (required):" aria-required="true"></textarea>
                        </div>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-remaining-characters-message" class="a-size-base a-color-secondary">
                          <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-char-count"> 200 </span> characters remaining. </span>
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-remaining-characters-message-announcement" role="status" class="comment-visually-hidden"></span>
                        <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-return-comment-error-message" class="a-box a-alert-inline a-alert-inline-error aok-hidden" role="alert">
                          <div class="a-box-inner a-alert-container">
                            <i class="a-icon a-icon-alert"></i>
                            <div class="a-alert-content"> Please describe the issue in the text box </div>
                          </div>
                        </div>
                      </div>
                      <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-read-only-section" class="a-section aok-hidden jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-comment-section-read-only-section">
                        <span id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-AmazonDefault-Q_AmazonDefault-RO_CR-MISSED_ESTIMATED_DELIVERY-AC_REQUIRED-read-only-section-text" class="a-size-base a-color-secondary"></span>
                      </div>
                    </div>
                  </div>
                  <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-pii-note" class="a-section aok-hidden">
                    <span class="a-size-base a-color-secondary">
                      <b>NOTE:</b> We aren't able to offer policy exceptions in response to comments. Do not include personal information as these comments may be shared with external service providers to identify product defects. </span>
                  </div>
                </div>
              </div>
              <div id="jhlmlphmrrluuqp-QW9tlDQdY-self_serviceable-llm-question-main-section" class="a-section a-spacing-none llm-question-main-section"></div>
            </div>
          </div>
        </div>
      </div>
      <hr aria-hidden="true" class="a-spacing-top-large a-divider-normal items-section-last-item-divider aok-hidden">
    </div>
  </form>
</div>
"""
