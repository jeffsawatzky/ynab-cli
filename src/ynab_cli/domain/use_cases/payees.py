import logging
import re
from collections.abc import AsyncIterator
from typing import TypedDict

from rapidfuzz import fuzz

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import api as ynab_api
from ynab_cli.adapters.ynab import models as ynab_models
from ynab_cli.domain import ports
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases.constants import YNAB_API_URL

log = logging.getLogger(__name__)


def _should_skip_payee(payee: ynab_models.Payee) -> bool:
    if payee.deleted or payee.name.startswith("Transfer : ") or payee.name in ["Starting Balance"]:
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


async def normalize_names(
    settings: Settings, io: ports.IO, params: NormalizeNamesParams
) -> AsyncIterator[tuple[ynab_models.Payee, str]]:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=settings.ynab.access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            payees_response = await ynab_api.PayeesApi(api_client).get_payees(settings.ynab.budget_id)
            payees = payees_response.data.payees

            for payee in payees:
                if _should_skip_payee(payee=payee):
                    continue

                normalized_name = _normalize_name(payee.name)
                if normalized_name != payee.name:
                    yield (payee, normalized_name)

                    if not settings.dry_run:
                        try:
                            await ynab_api.PayeesApi(api_client).update_payee(
                                settings.ynab.budget_id,
                                payee.id,
                                ynab_models.PatchPayeeWrapper(payee=ynab_models.SavePayee(name=normalized_name)),
                            )
                        except ynab.ApiError as e:
                            if e.status == 429:
                                new_access_token = await io.prompt(
                                    prompt="API rate limit exceeded. Enter a new access token", password=True
                                )
                                api_client.configuration.access_token = new_access_token
                                await ynab_api.PayeesApi(api_client).update_payee(
                                    settings.ynab.budget_id,
                                    payee.id,
                                    ynab_models.PatchPayeeWrapper(payee=ynab_models.SavePayee(name=normalized_name)),
                                )
                            else:
                                raise e

        except ynab.ApiError as e:
            if e.status == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")


class ListDuplicatesParams(TypedDict):
    pass


async def list_duplicates(
    settings: Settings, io: ports.IO, params: ListDuplicatesParams
) -> AsyncIterator[tuple[ynab_models.Payee, ynab_models.Payee]]:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=settings.ynab.access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            possible_duplicates: dict[tuple[str, str], list[tuple[str, str]]] = {}

            payees_response: ynab_models.PayeesResponse = await ynab_api.PayeesApi(api_client).get_payees(
                settings.ynab.budget_id
            )
            payees = payees_response.data.payees

            for idx, payee in enumerate(payees):
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

        except ynab.ApiError as e:
            if e.status == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")


class ListUnusedParams(TypedDict):
    pass


async def list_unused(settings: Settings, io: ports.IO, params: ListUnusedParams) -> AsyncIterator[ynab_models.Payee]:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=settings.ynab.access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            payees_response: ynab_models.PayeesResponse = await ynab_api.PayeesApi(api_client).get_payees(
                settings.ynab.budget_id
            )
            payees = payees_response.data.payees

            for payee in payees:
                if _should_skip_payee(payee=payee):
                    continue

                try:
                    payee_transactions_response = await ynab_api.TransactionsApi(api_client).get_transactions_by_payee(
                        settings.ynab.budget_id, payee.id
                    )
                except ynab.ApiError as e:
                    if e.status == 429:
                        new_access_token = await io.prompt(
                            prompt="API rate limit exceeded. Enter a new access token", password=True
                        )
                        api_client.configuration.access_token = new_access_token
                        payee_transactions_response = await ynab_api.TransactionsApi(
                            api_client
                        ).get_transactions_by_payee(settings.ynab.budget_id, payee.id)
                    else:
                        raise e
                num_transactions = len(payee_transactions_response.data.transactions)

                # List unused payee if no transactions
                if not num_transactions:
                    yield payee

        except ynab.ApiError as e:
            if e.status == 429:
                await io.print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                await io.print(f"Exception when calling YNAB: {e}\n")
