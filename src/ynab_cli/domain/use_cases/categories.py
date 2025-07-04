from collections.abc import AsyncIterator
from typing import TypedDict

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.categories import get_categories
from ynab_cli.adapters.ynab.api.transactions import get_transactions_by_category
from ynab_cli.domain import ports
from ynab_cli.domain.settings import Settings


def _should_skip_category_or_group(category_or_group: models.Category | models.CategoryGroupWithCategories) -> bool:
    if category_or_group.deleted:
        return True
    return False


class ListUnusedParams(TypedDict):
    pass


class ListUnused:
    """Use case for listing unused categories."""

    def __init__(self, io: ports.IO, client: ynab.AuthenticatedClient):
        self._io = io
        self._client = client

    async def __call__(self, settings: Settings, params: ListUnusedParams) -> AsyncIterator[models.Category]:
        try:
            progress_total = 0

            category_groups = (
                await util.get_asyncio_detailed(
                    self._io, get_categories.asyncio_detailed, settings.ynab.budget_id, client=self._client
                )
            ).data.category_groups
            category_groups.sort(key=lambda cg: cg.name)

            progress_total = len(category_groups)
            await self._io.progress.update(total=progress_total)
            for category_group in category_groups:
                await self._io.progress.update(advance=1)

                if _should_skip_category_or_group(category_or_group=category_group):
                    continue

                progress_total += len(category_group.categories)
                await self._io.progress.update(total=progress_total)
                category_group.categories.sort(key=lambda c: c.name)
                for category in category_group.categories:
                    await self._io.progress.update(advance=1)

                    if _should_skip_category_or_group(category_or_group=category):
                        continue

                    transactions = (
                        await util.get_asyncio_detailed(
                            self._io,
                            get_transactions_by_category.asyncio_detailed,
                            settings.ynab.budget_id,
                            str(category.id),
                            client=self._client,
                        )
                    ).data.transactions
                    num_transactions = len(transactions)

                    # List unused category if no transactions
                    if not num_transactions:
                        yield category

        except Exception as e:
            if isinstance(e, util.ApiError) and e.status_code == 401:
                await self._io.print("Invalid or expired access token. Please update your settings.")
            elif isinstance(e, util.ApiError) and e.status_code == 429:
                await self._io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await self._io.print(f"Exception when calling YNAB: {e}")
        finally:
            await self._io.progress.update(total=progress_total, completed=progress_total)


class ListAllParams(TypedDict):
    pass


class ListAll:
    """Use case for listing all categories."""

    def __init__(self, io: ports.IO, client: ynab.AuthenticatedClient):
        self._io = io
        self._client = client

    async def __call__(self, settings: Settings, params: ListAllParams) -> AsyncIterator[models.Category]:
        try:
            progress_total = 0

            category_groups = (
                await util.get_asyncio_detailed(
                    self._io, get_categories.asyncio_detailed, settings.ynab.budget_id, client=self._client
                )
            ).data.category_groups
            category_groups.sort(key=lambda cg: cg.name)

            progress_total = len(category_groups)
            await self._io.progress.update(total=progress_total)
            for category_group in category_groups:
                await self._io.progress.update(advance=1)

                if _should_skip_category_or_group(category_or_group=category_group):
                    continue

                progress_total += len(category_group.categories)
                await self._io.progress.update(total=progress_total)
                category_group.categories.sort(key=lambda c: c.name)
                for category in category_group.categories:
                    await self._io.progress.update(advance=1)

                    if _should_skip_category_or_group(category_or_group=category):
                        continue

                    yield category

        except Exception as e:
            if isinstance(e, util.ApiError) and e.status_code == 401:
                await self._io.print("Invalid or expired access token. Please update your settings.")
            elif isinstance(e, util.ApiError) and e.status_code == 429:
                await self._io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await self._io.print(f"Exception when calling YNAB: {e}")
        finally:
            await self._io.progress.update(total=progress_total, completed=progress_total)
