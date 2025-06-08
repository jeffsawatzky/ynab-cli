import re

from ynab_cli.adapters.amazon.constants import DEFAULT_AMAZON_HOST
from ynab_cli.adapters.browser.locale import HostLocaleInfo

HOST_LOCAL_INFO: HostLocaleInfo = {
    DEFAULT_AMAZON_HOST: {"accept_language": "en-US,en;q=0.9", "locale": "en_US", "currency": "USD"},
    "www.amazon.ca": {"accept_language": "en-CA,en;q=0.9", "locale": "en_CA", "currency": "CAD"},
}

LOCALE_REFUND_DATE_REGEX = "LOCALE_REFUND_DATE_REGEX"
LOCALE_AMAZON_GIFT_CARD_PAYMENT_METHOD = "LOCALE_AMAZON_GIFT_CARD_PAYMENT_METHOD"

LOCALE = {
    "en_US": {
        LOCALE_REFUND_DATE_REGEX: re.compile(r".*refund issued on (?P<refund_date>.+)\."),
        LOCALE_AMAZON_GIFT_CARD_PAYMENT_METHOD: "Amazon gift card used",
    },
    "en_CA": {
        LOCALE_REFUND_DATE_REGEX: re.compile(r".*refund issued on (?P<refund_date>.+)\."),
        LOCALE_AMAZON_GIFT_CARD_PAYMENT_METHOD: "Amazon gift card used",
    },
}
