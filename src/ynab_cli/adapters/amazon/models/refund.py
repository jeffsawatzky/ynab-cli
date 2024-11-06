from datetime import date
from decimal import Decimal

from ynab_cli.adapters.amazon.models.entity import Entity


class Refund(Entity, frozen=True):
    order_id: str
    product_id: str
    refund_total: Decimal
    refund_date: date
