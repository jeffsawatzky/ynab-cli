import factory

from ynab_cli.adapters.ynab import models


class TransactionDetailFactory(factory.Factory):  # type: ignore[misc]
    class Meta:
        model = models.TransactionDetail

    id = factory.Faker("uuid4")
    date = factory.Faker("date_this_year")
    amount = factory.Faker("random_int", min=1, max=100000)
    cleared = models.TransactionClearedStatus.CLEARED
    approved = True
    account_id = factory.Faker("uuid4", cast_to=None)
    deleted = factory.Faker("boolean")
    account_name = factory.Faker("word")
    subtransactions = factory.LazyFunction(list)
