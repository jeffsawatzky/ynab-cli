from getpass import getpass

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import api, models
from ynab_cli.host.cli.constants import YNAB_API_URL


def should_skip_category_or_group(category_or_group: models.Category | models.CategoryGroupWithCategories) -> bool:
    if category_or_group.deleted:
        return True
    return False


async def list_unused(access_token: str, budget_id: str) -> None:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            categories_response: models.CategoriesResponse = await api.CategoriesApi(api_client).get_categories(
                budget_id
            )
            category_groups = categories_response.data.category_groups

            for category_group in category_groups:
                if should_skip_category_or_group(category_or_group=category_group):
                    continue

                for category in category_group.categories:
                    if should_skip_category_or_group(category_or_group=category):
                        continue
                    try:
                        category_transactions_response = await api.TransactionsApi(
                            api_client
                        ).get_transactions_by_category(budget_id, category.id)
                    except ynab.ApiError as e:
                        if e.status == 429:
                            new_access_token = getpass(prompt="API rate limit exceeded. Enter a new access token: ")
                            api_client.configuration.access_token = new_access_token
                            category_transactions_response = await api.TransactionsApi(
                                api_client
                            ).get_transactions_by_category(budget_id, category.id)
                        else:
                            raise e
                    num_transactions = len(category_transactions_response.data.transactions)

                    # List unused category if no transactions
                    if not num_transactions:
                        print(f"{category_group.id}, {category.id}: {category_group.name}, {category.name}")

        except ynab.ApiError as e:
            if e.status == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")
