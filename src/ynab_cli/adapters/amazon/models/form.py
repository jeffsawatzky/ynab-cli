from attrs import define


@define
class Form:
    action: str
    method: str
    data: dict[str, str]
