from attrs import define

from ynab_cli.adapters.amazon.models.entity import Entity


@define
class Product(Entity):
    product_id: str
    categories: tuple[str, ...]
