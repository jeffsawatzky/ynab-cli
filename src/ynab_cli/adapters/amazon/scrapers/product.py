import logging
import re
from typing import ClassVar

from bs4 import Tag
from httpx import URL
from typing_extensions import override

from ynab_cli.adapters.amazon.models.product import Product
from ynab_cli.adapters.amazon.scrapers.base import BaseScraper

log = logging.getLogger(__name__)


class ProductScraper(BaseScraper[Product | None]):
    """Scrapes a single product from:
    /dp/<product_id>
    """

    BREADCRUMBS_FEATURE_SELECTOR: ClassVar[str] = "#wayfinding-breadcrumbs_feature_div"
    BREADCRUMB_ITEMS_SELECTOR: ClassVar[str] = "li > span > a"

    PRODUCT_ID_REGEX: ClassVar[re.Pattern[str]] = re.compile(
        r"(/dp/(?P<product_id1>[a-zA-Z0-9]+)|/gp/product/(?P<product_id2>[a-zA-Z0-9]+))"
    )

    @override
    async def scrape(self, response_url: URL, html: Tag) -> Product | None:
        product_id_match = self.__class__.PRODUCT_ID_REGEX.search(response_url.path)
        if not product_id_match:
            log.error("Could not find product ID in response url")
            return None
        product_id = product_id_match.group("product_id1") or product_id_match.group("product_id2")

        categories: tuple[str, ...] = tuple([])
        breadcrumbs_feature_tag = html.select_one(self.__class__.BREADCRUMBS_FEATURE_SELECTOR)
        if not breadcrumbs_feature_tag:
            log.warning("Could not find breadcrumbs feature tag")
        else:
            breadcrumb_item_tags = breadcrumbs_feature_tag.select(self.__class__.BREADCRUMB_ITEMS_SELECTOR)
            if not breadcrumb_item_tags:
                log.warning("Could not find breadcrumb item tags")
                return None

            categories = tuple(self.normalized_text(tag.text, whitespace=True) for tag in breadcrumb_item_tags)

        return Product(
            product_id=product_id,
            categories=categories,
        )
