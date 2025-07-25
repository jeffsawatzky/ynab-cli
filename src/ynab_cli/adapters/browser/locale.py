from typing import TypeAlias, TypedDict


class LocaleInfo(TypedDict):
    accept_language: str
    locale: str
    currency: str


Host: TypeAlias = str
HostLocaleInfo: TypeAlias = dict[Host, LocaleInfo]
