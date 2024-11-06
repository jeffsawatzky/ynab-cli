import logging
from collections.abc import AsyncIterator
from typing import TypedDict

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import api as ynab_api
from ynab_cli.adapters.ynab import models as ynab_models
from ynab_cli.domain import ports
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases.constants import YNAB_API_URL

log = logging.getLogger(__name__)


def _should_skip_category_or_group(
    category_or_group: ynab_models.Category | ynab_models.CategoryGroupWithCategories,
) -> bool:
    if category_or_group.deleted:
        return True
    return False


class ListUnusedParams(TypedDict):
    pass


async def list_unused(
    settings: Settings, io: ports.IO, params: ListUnusedParams
) -> AsyncIterator[ynab_models.Category]:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=settings.ynab.access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            categories_response = await ynab_api.CategoriesApi(api_client).get_categories(settings.ynab.budget_id)
            category_groups = categories_response.data.category_groups

            for category_group in category_groups:
                if _should_skip_category_or_group(category_or_group=category_group):
                    continue

                for category in category_group.categories:
                    if _should_skip_category_or_group(category_or_group=category):
                        continue
                    try:
                        category_transactions_response = await ynab_api.TransactionsApi(
                            api_client
                        ).get_transactions_by_category(settings.ynab.budget_id, category.id)
                    except ynab.ApiError as e:
                        if e.status == 429:
                            new_access_token = await io.prompt(
                                prompt="API rate limit exceeded. Enter a new access token", password=True
                            )
                            api_client.configuration.access_token = new_access_token
                            category_transactions_response = await ynab_api.TransactionsApi(
                                api_client
                            ).get_transactions_by_category(settings.ynab.budget_id, category.id)
                        else:
                            raise e
                    num_transactions = len(category_transactions_response.data.transactions)

                    # List unused category if no transactions
                    if not num_transactions:
                        yield category

        except ynab.ApiError as e:
            if e.status == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")


class ListAllParams(TypedDict):
    pass


async def list_all(settings: Settings, io: ports.IO, params: ListAllParams) -> AsyncIterator[ynab_models.Category]:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=settings.ynab.access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            categories_response = await ynab_api.CategoriesApi(api_client).get_categories(settings.ynab.budget_id)
            category_groups = categories_response.data.category_groups

            for category_group in category_groups:
                if _should_skip_category_or_group(category_or_group=category_group):
                    continue

                for category in category_group.categories:
                    if _should_skip_category_or_group(category_or_group=category):
                        continue

                    yield category

        except ynab.ApiError as e:
            if e.status == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")
