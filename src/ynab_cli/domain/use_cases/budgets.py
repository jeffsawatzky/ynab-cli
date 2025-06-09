from collections.abc import AsyncIterator
from typing import TypedDict

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.budgets import get_budgets
from ynab_cli.domain import ports
from ynab_cli.domain.constants import YNAB_API_URL
from ynab_cli.domain.settings import Settings


class ListAllParams(TypedDict):
    pass


async def list_all(settings: Settings, io: ports.IO, params: ListAllParams) -> AsyncIterator[models.BudgetSummary]:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=settings.ynab.access_token) as client:
        progress_total = 0
        try:
            budgets = (
                await util.get_asyncio_detailed(io, get_budgets.asyncio_detailed, include_accounts=True, client=client)
            ).data.budgets
            budgets.sort(key=lambda b: b.name)

            progress_total = len(budgets)
            await io.progress.update(total=progress_total)
            for budget in budgets:
                await io.progress.update(advance=1)
                yield budget

        except util.ApiError as e:
            if e.status_code == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")
        finally:
            await io.progress.update(total=progress_total, completed=progress_total)
