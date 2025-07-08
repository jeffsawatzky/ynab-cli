from factory import Factory, Faker, LazyFunction

from ynab_cli.adapters.ynab import models


class TransactionDetailFactory(Factory[models.TransactionDetail]):
    class Meta:
        model = models.TransactionDetail

    id = Faker("uuid4")
    date = Faker("date_this_year")
    amount = Faker("random_int", min=1, max=100000)
    cleared = models.TransactionClearedStatus.CLEARED
    approved = True
    account_id = Faker("uuid4", cast_to=None)
    deleted = Faker("boolean")
    account_name = Faker("word")
    subtransactions = LazyFunction(list)
