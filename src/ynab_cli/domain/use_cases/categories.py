from getpass import getpass

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.categories import get_categories
from ynab_cli.adapters.ynab.api.transactions import get_transactions_by_category
from ynab_cli.host.cli.constants import YNAB_API_URL


def should_skip_category_or_group(category_or_group: models.Category | models.CategoryGroupWithCategories) -> bool:
    if category_or_group.deleted:
        return True
    return False


async def list_unused(access_token: str, budget_id: str) -> None:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=access_token) as client:
        try:
            get_categories_response = await get_categories.asyncio_detailed(budget_id, client=client)
            category_groups = util.get_ynab_model(
                get_categories_response, models.CategoriesResponse
            ).data.category_groups

            for category_group in category_groups:
                if should_skip_category_or_group(category_or_group=category_group):
                    continue

                for category in category_group.categories:
                    if should_skip_category_or_group(category_or_group=category):
                        continue
                    try:
                        get_transactions_by_category_response = await get_transactions_by_category.asyncio_detailed(
                            budget_id, str(category.id), client=client
                        )
                        transactions = util.get_ynab_model(
                            get_transactions_by_category_response, models.HybridTransactionsResponse
                        ).data.transactions
                    except util.ApiError as e:
                        if e.status_code == 429:
                            new_access_token = getpass(prompt="API rate limit exceeded. Enter a new access token: ")
                            client.token = new_access_token
                            get_transactions_by_category_response = await get_transactions_by_category.asyncio_detailed(
                                budget_id, str(category.id), client=client
                            )
                            transactions = util.get_ynab_model(
                                get_transactions_by_category_response, models.HybridTransactionsResponse
                            ).data.transactions
                        else:
                            raise e
                    num_transactions = len(transactions)

                    # List unused category if no transactions
                    if not num_transactions:
                        print(f"{category_group.id}, {category.id}: {category_group.name}, {category.name}")

        except util.ApiError as e:
            if e.status_code == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")


async def list_all(access_token: str, budget_id: str) -> None:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=access_token) as client:
        try:
            get_categories_response = await get_categories.asyncio_detailed(budget_id, client=client)
            category_groups = util.get_ynab_model(
                get_categories_response, models.CategoriesResponse
            ).data.category_groups

            for category_group in category_groups:
                if should_skip_category_or_group(category_or_group=category_group):
                    continue

                for category in category_group.categories:
                    if should_skip_category_or_group(category_or_group=category):
                        continue

                    print(f"{category_group.id}, {category.id}: {category_group.name}, {category.name}")

        except util.ApiError as e:
            if e.status_code == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")
