from typing import ClassVar

from bs4 import Tag
from typing_extensions import override
from yarl import URL

from ynab_cli.adapters.amazon.browser import Browser
from ynab_cli.adapters.amazon.scrapers.base import BaseCaptchaFormScraper, BaseFormScraper
from ynab_cli.domain.ports.io import IO


class SignInFormScraper(BaseFormScraper):
    FORM_SELECTOR: ClassVar[str] = "form[name='signIn']"
    SUBMIT_SELECTOR: ClassVar[str] = ""

    def __init__(self, username: str, password: str, browser: Browser, io: IO) -> None:
        super().__init__(browser, io)

        self._username = username
        self._password = password

    @override
    async def _parse_form_tag(
        self, response_url: URL, form_tag: Tag, data: dict[str, str]
    ) -> tuple[str, str, dict[str, str]]:
        action, method, data = await super()._parse_form_tag(response_url, form_tag, data)
        data["email"] = self._username
        data["password"] = self._password

        return (action, method, data)


class SignInCaptchaFormScraper(BaseCaptchaFormScraper):
    FORM_SELECTOR: ClassVar[str] = "form:has(input[id^='captchacharacters'])"
    SUBMIT_SELECTOR: ClassVar[str] = ""
    CAPTCHA_SELECTOR: ClassVar[str] = "form:has(input[id^='captchacharacters']) img"
    CAPTCHA_FIELD: ClassVar[str] = "field-keywords"


class CfvRequestCaptchaFormScraper(BaseCaptchaFormScraper):
    FORM_SELECTOR: ClassVar[str] = "form.cvf-widget-form.cvf-widget-form-captcha"
    SUBMIT_SELECTOR: ClassVar[str] = "input[type='submit'][name='cvf_captcha_captcha_action'][value='verifyCaptcha']"
    CAPTCHA_SELECTOR: ClassVar[str] = "div.cvf-captcha-img > img[alt='captcha']"
    CAPTCHA_FIELD: ClassVar[str] = "cvf_captcha_input"


class PpwWidgetNextPageFormScraper(BaseFormScraper):
    FORM_SELECTOR: ClassVar[str] = "form:has(input[name='ppw-widgetState'])"
    SUBMIT_SELECTOR: ClassVar[str] = "input[type='submit'][name^='ppw-widgetEvent:DefaultNextPageNavigationEvent']"
