from datetime import date
from decimal import Decimal
from functools import cached_property
from typing import Union

from pydantic import BaseModel, computed_field

from ynab_cli.adapters.amazon.models.transaction import Transaction


class TransactionGroup(BaseModel, frozen=True):
    completed_date: date
    payment_method: str
    order_id: str
    order_link: str
    seller: str
    is_refund: bool
    is_gift_card: bool
    transactions: tuple[Transaction, ...]

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def grand_total(self) -> Decimal:
        grand_total = Decimal(0)
        for transaction in self.transactions:
            grand_total += transaction.grand_total
        return grand_total

    def append(self, transaction: Transaction) -> "TransactionGroup":
        if TransactionGroup.key(self) != TransactionGroup.key(transaction):
            raise ValueError("Transaction does not match group")

        return TransactionGroup(
            completed_date=self.completed_date,
            payment_method=self.payment_method,
            order_id=self.order_id,
            order_link=self.order_link,
            seller=self.seller,
            is_refund=self.is_refund,
            is_gift_card=self.is_gift_card,
            transactions=(*self.transactions, transaction),
        )

    @classmethod
    def key(
        cls, transaction_like: Union[Transaction, "TransactionGroup"]
    ) -> tuple[date, str, str, str, str, bool, bool]:
        return (
            transaction_like.completed_date,
            transaction_like.payment_method,
            transaction_like.order_id,
            transaction_like.order_link,
            transaction_like.seller,
            transaction_like.is_refund,
            transaction_like.is_gift_card,
        )
