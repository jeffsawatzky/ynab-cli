import json
import logging
from collections.abc import AsyncIterator
from typing import ClassVar

from bs4 import Tag
from httpx import URL
from typing_extensions import override

from ynab_cli.adapters.amazon.models.refund import Refund
from ynab_cli.adapters.amazon.scrapers.base import BaseScraper
from ynab_cli.adapters.amazon.scrapers.refund import RefundScraper

log = logging.getLogger(__name__)


class RefundsScraper(BaseScraper[AsyncIterator[Refund]]):
    """Scrapes refunds from:
    /spr/returns/cart?orderId=<order_id>
    """

    STATE_SCRIPT_SELECTOR: ClassVar[str] = "script[data-a-state*='eventDataForItemsV2']"

    @override
    async def scrape(self, response_url: URL, html: Tag) -> AsyncIterator[Refund]:
        async def async_iter() -> AsyncIterator[Refund]:
            state_script_tag = html.select_one(self.__class__.STATE_SCRIPT_SELECTOR)
            if not state_script_tag:
                log.warning("Could not find state script tag")
                return

            state_script = self.normalized_text(state_script_tag.string)
            if not state_script:
                log.warning("Could not find state script content")
                return

            try:
                state_json = json.loads(state_script)
                if not isinstance(state_json, dict):
                    log.warning("State script content is not a dictionary")
                    return
            except json.JSONDecodeError as e:
                log.warning(f"Could not parse state script content: {e}")
                return

            for key, value in state_json.items():
                if not isinstance(value, dict):
                    log.warning("State script values are not dictionaries")
                    return

                returnability = value.get("returnability")
                if not returnability:
                    log.warning("Could not find returnability")
                    return

                if returnability == "CONSUMED":
                    order_id = value.get("orderId")
                    if not order_id:
                        log.warning("Could not find order ID")
                        return

                    unit_id_to_unit_data_map_json = value.get("unitIdToUnitDataMap")
                    if not unit_id_to_unit_data_map_json:
                        log.warning("Could not find unit ID to unit data map")
                        return

                    try:
                        unit_id_to_unit_data_map = json.loads(unit_id_to_unit_data_map_json)
                        if not isinstance(unit_id_to_unit_data_map, dict):
                            log.warning("Unit ID to unit data map is not a dictionary")
                            return
                    except json.JSONDecodeError as e:
                        log.warning(f"Could not parse unit ID to unit data map: {e}")
                        return

                    for unit_data in unit_id_to_unit_data_map.values():
                        if not isinstance(unit_data, dict):
                            log.warning("Unit data is not a dictionary")
                            return

                        product_id = unit_data.get("asin")
                        if product_id:
                            break

                    if not product_id:
                        log.warning("Could not find product ID")
                        return

                    refund_selector = f"#{key}-orc-item"
                    refund_tag = html.select_one(refund_selector)
                    if not refund_tag:
                        log.warning("Could not find refund tag")
                        return

                    refund = await RefundScraper(order_id, product_id).scrape(response_url, refund_tag)

                    if refund:
                        yield refund

        return async_iter()
