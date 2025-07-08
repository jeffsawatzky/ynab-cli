from typing import cast

from lagom import Container, ExplicitContainer, Singleton

from ynab_cli.domain.constants import YNAB_API_URL


def init_container(container: Container) -> Container:
    from ynab_cli.adapters.ynab.client import AuthenticatedClient
    from ynab_cli.domain.ports.io import IO
    from ynab_cli.domain.settings import Settings
    from ynab_cli.domain.use_cases import budgets as budgets_use_cases
    from ynab_cli.domain.use_cases import categories as categories_use_cases
    from ynab_cli.domain.use_cases import payees as payees_use_cases
    from ynab_cli.domain.use_cases import transactions as transactions_use_cases

    #
    # Adapters
    #
    container[AuthenticatedClient] = Singleton(
        lambda c: AuthenticatedClient(
            YNAB_API_URL,
            cast(Settings, c[Settings]).ynab.access_token,
        )
    )

    #
    # Use Cases
    #

    container[budgets_use_cases.ListAll] = lambda c: budgets_use_cases.ListAll(
        c[IO],
        c[AuthenticatedClient],
    )
    container[categories_use_cases.ListUnused] = lambda c: categories_use_cases.ListUnused(
        c[IO],
        c[AuthenticatedClient],
    )
    container[categories_use_cases.ListAll] = lambda c: categories_use_cases.ListAll(
        c[IO],
        c[AuthenticatedClient],
    )
    container[payees_use_cases.NormalizeNames] = lambda c: payees_use_cases.NormalizeNames(
        c[IO],
        c[AuthenticatedClient],
    )
    container[payees_use_cases.ListDuplicates] = lambda c: payees_use_cases.ListDuplicates(
        c[IO],
        c[AuthenticatedClient],
    )
    container[payees_use_cases.ListUnused] = lambda c: payees_use_cases.ListUnused(
        c[IO],
        c[AuthenticatedClient],
    )
    container[payees_use_cases.ListAll] = lambda c: payees_use_cases.ListAll(
        c[IO],
        c[AuthenticatedClient],
    )
    container[transactions_use_cases.ApplyRules] = lambda c: transactions_use_cases.ApplyRules(
        c[IO],
        c[AuthenticatedClient],
    )

    return container


def make_container() -> Container:  # pragma: no cover
    return init_container(ExplicitContainer())
