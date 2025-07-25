from datetime import date
from decimal import Decimal

from attrs import define

from ynab_cli.adapters.amazon.models.entity import Entity


@define
class Refund(Entity):
    order_id: str
    product_id: str
    refund_total: Decimal
    refund_date: date
