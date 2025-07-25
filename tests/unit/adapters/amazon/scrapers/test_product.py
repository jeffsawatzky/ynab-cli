import pytest
from bs4 import BeautifulSoup
from httpx import URL

from ynab_cli.adapters.amazon.scrapers.product import ProductScraper


@pytest.mark.anyio
async def test_scrape__success_dp() -> None:
    # GIVEN
    fixture = TEST_PARSE_PRODUCT_HTML
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = ProductScraper()
    product = await sut.scrape(URL("https://www.amazon.ca/dp/B07QJ3ZJ3R"), html)

    # THEN
    assert product is not None
    assert product.product_id == "B07QJ3ZJ3R"
    assert product.categories == (
        "Tools & Home Improvement",
        "Lighting & Ceiling Fans",
        "String Lights",
        "Outdoor Light Strings",
    )


@pytest.mark.anyio
async def test_scrape__success_gp() -> None:
    # GIVEN
    fixture = TEST_PARSE_PRODUCT_HTML
    html = BeautifulSoup(fixture, "html.parser")

    # WHEN
    sut = ProductScraper()
    product = await sut.scrape(URL("https://www.amazon.ca/gp/product/B07QJ3ZJ3R"), html)

    # THEN
    assert product is not None
    assert product.product_id == "B07QJ3ZJ3R"
    assert product.categories == (
        "Tools & Home Improvement",
        "Lighting & Ceiling Fans",
        "String Lights",
        "Outdoor Light Strings",
    )


TEST_PARSE_PRODUCT_HTML = """
<div id="showing-breadcrumbs_feature_div" class="celwidget" data-feature-name="showing-breadcrumbs"
    data-csa-c-type="widget" data-csa-c-content-id="showing-breadcrumbs"
    data-csa-c-slot-id="showing-breadcrumbs_feature_div" data-csa-c-asin="" data-csa-c-is-in-initial-active-row="false"
    data-csa-c-id="bjgur7-t2tg7p-fmnxco-qcwdcu" data-cel-widget="showing-breadcrumbs_feature_div">
    <div id="showing-breadcrumbs_div">
        <div cel_widget_id="showing-breadcrumbs_csm_instrumentation_wrapper" class="celwidget"
            data-csa-c-id="b47wmg-s4udjc-6twggi-m1q0i5"
            data-cel-widget="showing-breadcrumbs_csm_instrumentation_wrapper">
            <div id="wayfinding-breadcrumbs_container" class="a-section a-spacing-none a-padding-medium">
                <div id="wayfinding-breadcrumbs_feature_div" class="a-subheader a-breadcrumb feature"
                    data-feature-name="wayfinding-breadcrumbs" data-cel-widget="wayfinding-breadcrumbs_feature_div">
                    <ul class="a-unordered-list a-horizontal a-size-small">
                        <li><span class="a-list-item">
                                <a class="a-link-normal a-color-tertiary"
                                    href="/Home-Improvement/b/ref=dp_bc_aui_C_1?ie=UTF8&amp;node=3006902011">
                                    Tools &amp; Home Improvement
                                </a>
                            </span>
                        </li>
                        <li class="a-breadcrumb-divider"><span class="a-list-item a-color-tertiary">
                                |
                            </span>
                        </li>
                        <li><span class="a-list-item">
                                <a class="a-link-normal a-color-tertiary"
                                    href="/b/ref=dp_bc_aui_C_2?ie=UTF8&amp;node=3130298011">
                                    Lighting &amp; Ceiling Fans
                                </a>
                            </span>
                        </li>
                        <li class="a-breadcrumb-divider"><span class="a-list-item a-color-tertiary">
                                |
                            </span>
                        </li>
                        <li><span class="a-list-item">
                                <a class="a-link-normal a-color-tertiary"
                                    href="/b/ref=dp_bc_aui_C_3?ie=UTF8&amp;node=20753174011">
                                    String Lights
                                </a>
                            </span>
                        </li>
                        <li class="a-breadcrumb-divider"><span class="a-list-item a-color-tertiary">
                                |
                            </span>
                        </li>
                        <li><span class="a-list-item">
                                <a class="a-link-normal a-color-tertiary"
                                    href="/b/ref=dp_bc_aui_C_4?ie=UTF8&amp;node=3130336011">
                                    Outdoor Light Strings
                                </a>
                            </span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
"""
