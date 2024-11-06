from factory.base import Factory
from factory.declarations import LazyFunction
from factory.faker import Faker

from ynab_cli.adapters.ynab import models


class TransactionDetailFactory(Factory[models.TransactionDetail]):
    class Meta:
        model = models.TransactionDetail

    id = Faker("uuid4")  # type: ignore[no-untyped-call]
    var_date = Faker("date_this_year")  # type: ignore[no-untyped-call]
    amount = Faker("random_int", min=1, max=100000)  # type: ignore[no-untyped-call]
    memo = None
    cleared = models.TransactionClearedStatus.CLEARED
    approved = True
    flag_color = None
    flag_name = None
    account_id = Faker("uuid4")  # type: ignore[no-untyped-call]
    payee_id = None
    category_id = None
    transfer_account_id = None
    transfer_transaction_id = None
    matched_transaction_id = None
    import_id = None
    import_payee_name = None
    import_payee_name_original = None
    debt_transaction_type = None
    deleted = Faker("boolean")  # type: ignore[no-untyped-call]
    account_name = Faker("word")  # type: ignore[no-untyped-call]
    payee_name = None
    category_name = None
    subtransactions = LazyFunction(list)  # type: ignore[no-untyped-call]
