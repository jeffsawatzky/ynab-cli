from typing import ClassVar

from ynab_cli.adapters.amazon.scrapers.base import BaseFormScraper


class PpwWidgetNextPageFormScraper(BaseFormScraper):
    FORM_SELECTOR: ClassVar[str] = "form:has(input[name='ppw-widgetState'])"
    SUBMIT_SELECTOR: ClassVar[str] = "input[type='submit'][name^='ppw-widgetEvent:DefaultNextPageNavigationEvent']"
