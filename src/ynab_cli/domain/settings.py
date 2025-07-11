from attrs import define as _attrs_define
from attrs import field


@_attrs_define
class YnabSettings:
    access_token: str = ""
    budget_id: str = ""


@_attrs_define
class Settings:
    ynab: YnabSettings = field(factory=YnabSettings)
