import re
from collections.abc import AsyncIterator
from typing import TypedDict
from uuid import UUID

from rapidfuzz import fuzz

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.payees import get_payees, update_payee
from ynab_cli.adapters.ynab.api.transactions import get_transactions_by_payee
from ynab_cli.domain import ports
from ynab_cli.domain.constants import UNUSED_PREFIX
from ynab_cli.domain.settings import Settings


def _should_skip_payee(payee: models.Payee) -> bool:
    if (
        payee.deleted
        or (payee.transfer_account_id and isinstance(payee.transfer_account_id, str))
        or payee.name.startswith("Transfer : ")
        or payee.name.startswith(UNUSED_PREFIX)
        or payee.name in ["Starting Balance"]
    ):
        return True
    return False


def _normalize_name(name: str) -> str:
    normalized_name = name.title().strip()
    # Normalize possessive names
    normalized_name = normalized_name.replace("'S", "'s")
    # Normalize multiple whitespaces
    normalized_name = re.sub(r"\s+", " ", normalized_name)
    # Normalize domain names
    m = re.search(r".+\.([a-zA-Z]{2,3})$", normalized_name)
    if m:
        normalized_name = normalized_name.replace(m.group(1), m.group(1).lower())

    return normalized_name


class NormalizeNamesParams(TypedDict):
    pass


class NormalizeNames:
    """Use case for normalizing payee names."""

    def __init__(self, io: ports.IO, client: ynab.AuthenticatedClient):
        self._io = io
        self._client = client

    async def __call__(
        self, settings: Settings, params: NormalizeNamesParams
    ) -> AsyncIterator[tuple[models.Payee, str]]:
        try:
            progress_total = 0

            payees = (
                await util.get_asyncio_detailed(
                    self._io, get_payees.asyncio_detailed, settings.ynab.budget_id, client=self._client
                )
            ).data.payees
            payees.sort(key=lambda p: p.name)

            progress_total = len(payees)
            await self._io.progress.update(total=progress_total)
            for payee in payees:
                await self._io.progress.update(advance=1)

                if _should_skip_payee(payee=payee):
                    continue

                normalized_name = _normalize_name(payee.name)
                if normalized_name != payee.name:
                    yield (payee, normalized_name)

                    if not settings.dry_run:
                        await util.run_asyncio_detailed(
                            self._io,
                            update_payee.asyncio_detailed,
                            settings.ynab.budget_id,
                            str(payee.id),
                            client=self._client,
                            body=models.PatchPayeeWrapper(payee=models.SavePayee(name=normalized_name)),
                        )

        except Exception as e:
            if isinstance(e, util.ApiError) and e.status_code == 401:
                await self._io.print("Invalid or expired access token. Please update your settings.")
            elif isinstance(e, util.ApiError) and e.status_code == 429:
                await self._io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await self._io.print(f"Exception when calling YNAB: {e}")
        finally:
            await self._io.progress.update(total=progress_total, completed=progress_total)


class ListDuplicatesParams(TypedDict):
    pass


class ListDuplicates:
    """Use case for listing duplicate payees."""

    def __init__(self, io: ports.IO, client: ynab.AuthenticatedClient):
        self._io = io
        self._client = client

    async def __call__(
        self, settings: Settings, params: ListDuplicatesParams
    ) -> AsyncIterator[tuple[models.Payee, models.Payee]]:
        try:
            progress_total = 0

            possible_duplicates: dict[tuple[UUID, str], list[tuple[UUID, str]]] = {}

            payees = (
                await util.get_asyncio_detailed(
                    self._io, get_payees.asyncio_detailed, settings.ynab.budget_id, client=self._client
                )
            ).data.payees
            payees.sort(key=lambda p: p.name)

            progress_total = len(payees)
            await self._io.progress.update(total=progress_total)
            for idx, payee in enumerate(payees):
                await self._io.progress.update(advance=1)

                if _should_skip_payee(payee=payee):
                    continue

                filtered_payees = list(payees)
                del filtered_payees[idx]

                for filtered_payee in filtered_payees:
                    if _should_skip_payee(payee=filtered_payee):
                        continue

                    normalized_payee_name = _normalize_name(payee.name).lower()
                    normalized_filtered_payee_name = _normalize_name(filtered_payee.name).lower()
                    if fuzz.ratio(normalized_payee_name, normalized_filtered_payee_name) > 70:
                        # Check to see if we already tracked this possible duplicate in the other direction
                        existing_possible_duplicates = possible_duplicates.get((filtered_payee.id, filtered_payee.name))
                        if existing_possible_duplicates:
                            if (payee.id, payee.name) in existing_possible_duplicates:
                                continue

                        possible_duplicates[(payee.id, payee.name)] = possible_duplicates.get(
                            (payee.id, payee.name), []
                        )
                        possible_duplicates[(payee.id, payee.name)].append((filtered_payee.id, filtered_payee.name))

                        yield (payee, filtered_payee)

        except Exception as e:
            if isinstance(e, util.ApiError) and e.status_code == 401:
                await self._io.print("Invalid or expired access token. Please update your settings.")
            elif isinstance(e, util.ApiError) and e.status_code == 429:
                await self._io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await self._io.print(f"Exception when calling YNAB: {e}")
        finally:
            await self._io.progress.update(total=progress_total, completed=progress_total)


class ListUnusedParams(TypedDict):
    prefix_unused: bool


class ListUnused:
    """Use case for listing unused payees."""

    def __init__(self, io: ports.IO, client: ynab.AuthenticatedClient):
        self._io = io
        self._client = client

    async def __call__(self, settings: Settings, params: ListUnusedParams) -> AsyncIterator[models.Payee]:
        try:
            progress_total = 0

            payees = (
                await util.get_asyncio_detailed(
                    self._io, get_payees.asyncio_detailed, settings.ynab.budget_id, client=self._client
                )
            ).data.payees
            payees.sort(key=lambda p: p.name)

            progress_total = len(payees)
            await self._io.progress.update(total=progress_total)
            for payee in payees:
                await self._io.progress.update(advance=1)

                if _should_skip_payee(payee=payee):
                    continue

                transactions = (
                    await util.get_asyncio_detailed(
                        self._io,
                        get_transactions_by_payee.asyncio_detailed,
                        settings.ynab.budget_id,
                        str(payee.id),
                        client=self._client,
                    )
                ).data.transactions
                num_transactions = len(transactions)

                # List unused payee if no transactions
                if not num_transactions:
                    yield payee

                    # If prefix_unused is True, rename the payee
                    if not settings.dry_run and params.get("prefix_unused", False):
                        new_name = f"{UNUSED_PREFIX} {payee.name}"
                        await util.run_asyncio_detailed(
                            self._io,
                            update_payee.asyncio_detailed,
                            settings.ynab.budget_id,
                            str(payee.id),
                            client=self._client,
                            body=models.PatchPayeeWrapper(payee=models.SavePayee(name=new_name)),
                        )

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
    """Use case for listing all payees."""

    def __init__(self, io: ports.IO, client: ynab.AuthenticatedClient):
        self._io = io
        self._client = client

    async def __call__(self, settings: Settings, params: ListAllParams) -> AsyncIterator[models.Payee]:
        try:
            progress_total = 0

            payees = (
                await util.get_asyncio_detailed(
                    self._io, get_payees.asyncio_detailed, settings.ynab.budget_id, client=self._client
                )
            ).data.payees
            payees.sort(key=lambda p: p.name)

            progress_total = len(payees)
            await self._io.progress.update(total=progress_total)
            for payee in payees:
                await self._io.progress.update(advance=1)

                if _should_skip_payee(payee=payee):
                    continue

                yield payee

        except Exception as e:
            if isinstance(e, util.ApiError) and e.status_code == 401:
                await self._io.print("Invalid or expired access token. Please update your settings.")
            elif isinstance(e, util.ApiError) and e.status_code == 429:
                await self._io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await self._io.print(f"Exception when calling YNAB: {e}")
        finally:
            await self._io.progress.update(total=progress_total, completed=progress_total)
