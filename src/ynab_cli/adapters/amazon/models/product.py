from ynab_cli.adapters.amazon.models.entity import Entity


class Product(Entity, frozen=True):
    product_id: str
    categories: tuple[str, ...]
