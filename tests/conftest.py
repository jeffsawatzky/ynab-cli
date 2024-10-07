from pytest_factoryboy import register

from tests.factories import ynab

register(ynab.TransactionDetailFactory)
