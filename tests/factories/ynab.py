from datetime import date

import factory

from ynab_cli.adapters.ynab import models


class TransactionDetailFactory(factory.Factory):  # type: ignore[misc]
    class Meta:
        model = models.TransactionDetail

    id: str = factory.Faker("uuid4")
    var_date: date = factory.Faker("date_this_year")
    amount: int = factory.Faker("random_int", min=1, max=100000)
    memo: str | None = None
    cleared: models.TransactionClearedStatus = models.TransactionClearedStatus.CLEARED
    approved: bool = True
    flag_color: models.TransactionFlagColor | None = None
    flag_name: str | None = None
    account_id: str = factory.Faker("uuid4")
    payee_id: str | None = None
    category_id: str | None = None
    transfer_account_id: str | None = None
    transfer_transaction_id: str | None = None
    matched_transaction_id: str | None = None
    import_id: str | None = None
    import_payee_name: str | None = None
    import_payee_name_original: str | None = None
    debt_transaction_type: str | None = None
    deleted: bool = factory.Faker("boolean")
    account_name: str = factory.Faker("word")
    payee_name: str | None = None
    category_name: str | None = None
    subtransactions: list[models.SubTransaction] = factory.LazyFunction(list)
