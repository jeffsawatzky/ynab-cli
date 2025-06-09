from collections.abc import AsyncIterator
from typing import TypedDict

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.categories import get_categories
from ynab_cli.adapters.ynab.api.transactions import get_transactions_by_category
from ynab_cli.domain import ports
from ynab_cli.domain.constants import YNAB_API_URL
from ynab_cli.domain.settings import Settings


def _should_skip_category_or_group(category_or_group: models.Category | models.CategoryGroupWithCategories) -> bool:
    if category_or_group.deleted:
        return True
    return False


class ListUnusedParams(TypedDict):
    pass


async def list_unused(settings: Settings, io: ports.IO, params: ListUnusedParams) -> AsyncIterator[models.Category]:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=settings.ynab.access_token) as client:
        progress_total = 0
        try:
            category_groups = (
                await util.get_asyncio_detailed(
                    io, get_categories.asyncio_detailed, settings.ynab.budget_id, client=client
                )
            ).data.category_groups
            category_groups.sort(key=lambda cg: cg.name)

            progress_total = len(category_groups)
            await io.progress.update(total=progress_total)
            for category_group in category_groups:
                await io.progress.update(advance=1)

                if _should_skip_category_or_group(category_or_group=category_group):
                    continue

                progress_total += len(category_group.categories)
                await io.progress.update(total=progress_total)
                category_group.categories.sort(key=lambda c: c.name)
                for category in category_group.categories:
                    await io.progress.update(advance=1)

                    if _should_skip_category_or_group(category_or_group=category):
                        continue

                    transactions = (
                        await util.get_asyncio_detailed(
                            io,
                            get_transactions_by_category.asyncio_detailed,
                            settings.ynab.budget_id,
                            str(category.id),
                            client=client,
                        )
                    ).data.transactions
                    num_transactions = len(transactions)

                    # List unused category if no transactions
                    if not num_transactions:
                        yield category

        except util.ApiError as e:
            if e.status_code == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")
        finally:
            await io.progress.update(total=progress_total, completed=progress_total)


class ListAllParams(TypedDict):
    pass


async def list_all(settings: Settings, io: ports.IO, params: ListAllParams) -> AsyncIterator[models.Category]:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=settings.ynab.access_token) as client:
        progress_total = 0
        try:
            category_groups = (
                await util.get_asyncio_detailed(
                    io, get_categories.asyncio_detailed, settings.ynab.budget_id, client=client
                )
            ).data.category_groups
            category_groups.sort(key=lambda cg: cg.name)

            progress_total = len(category_groups)
            await io.progress.update(total=progress_total)
            for category_group in category_groups:
                await io.progress.update(advance=1)

                if _should_skip_category_or_group(category_or_group=category_group):
                    continue

                progress_total += len(category_group.categories)
                await io.progress.update(total=progress_total)
                category_group.categories.sort(key=lambda c: c.name)
                for category in category_group.categories:
                    await io.progress.update(advance=1)

                    if _should_skip_category_or_group(category_or_group=category):
                        continue

                    yield category

        except util.ApiError as e:
            if e.status_code == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")
        finally:
            await io.progress.update(total=progress_total, completed=progress_total)
