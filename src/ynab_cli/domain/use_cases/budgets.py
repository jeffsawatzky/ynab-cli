from collections.abc import AsyncIterator
from typing import TypedDict

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.budgets import get_budgets
from ynab_cli.domain import ports
from ynab_cli.domain.settings import Settings


class ListAllParams(TypedDict):
    pass


class ListAll:
    """Use case for listing all budgets."""

    def __init__(self, io: ports.IO, client: ynab.AuthenticatedClient):
        self._io = io
        self._client = client

    async def __call__(self, settings: Settings, params: ListAllParams) -> AsyncIterator[models.BudgetSummary]:
        try:
            progress_total = 0

            budgets = (
                await util.get_asyncio_detailed(
                    self._io, get_budgets.asyncio_detailed, include_accounts=False, client=self._client
                )
            ).data.budgets
            budgets.sort(key=lambda b: b.name)

            progress_total = len(budgets)
            await self._io.progress.update(total=progress_total)
            for budget in budgets:
                await self._io.progress.update(advance=1)
                yield budget

        except Exception as e:
            if isinstance(e, util.ApiError) and e.status_code == 401:
                await self._io.print("Invalid or expired access token. Please update your settings.")
            elif isinstance(e, util.ApiError) and e.status_code == 429:
                await self._io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await self._io.print(f"Exception when calling YNAB: {e}")
        finally:
            await self._io.progress.update(total=progress_total, completed=progress_total)
