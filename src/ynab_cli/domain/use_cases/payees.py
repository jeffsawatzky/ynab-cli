import re
from getpass import getpass
from uuid import UUID

from rapidfuzz import fuzz

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.api.payees import get_payees, update_payee
from ynab_cli.adapters.ynab.api.transactions import get_transactions_by_payee
from ynab_cli.host.cli.constants import YNAB_API_URL


def should_skip_payee(payee: models.Payee) -> bool:
    if payee.deleted or payee.name.startswith("Transfer : ") or payee.name in ["Starting Balance"]:
        return True
    return False


def normalize_name(name: str) -> str:
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


async def normalize_names(access_token: str, budget_id: str, dry_run: bool) -> None:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=access_token) as client:
        try:
            get_payees_response = await get_payees.asyncio_detailed(
                budget_id,
                client=client,
            )
            payees = util.get_ynab_model(get_payees_response, models.PayeesResponse).data.payees

            for payee in payees:
                if should_skip_payee(payee=payee):
                    continue

                normalized_name = normalize_name(payee.name)
                if normalized_name != payee.name:
                    print(f"{payee.id}: {payee.name} -> {normalized_name}")

                    if not dry_run:
                        try:
                            util.ensure_success(
                                await update_payee.asyncio_detailed(
                                    budget_id,
                                    str(payee.id),
                                    client=client,
                                    body=models.PatchPayeeWrapper(payee=models.SavePayee(name=normalized_name)),
                                )
                            )
                        except util.ApiError as e:
                            if e.status_code == 429:
                                new_access_token = getpass(prompt="API rate limit exceeded. Enter a new access token: ")
                                client.token = new_access_token
                                util.ensure_success(
                                    await update_payee.asyncio_detailed(
                                        budget_id,
                                        str(payee.id),
                                        client=client,
                                        body=models.PatchPayeeWrapper(payee=models.SavePayee(name=normalized_name)),
                                    )
                                )
                            else:
                                raise e

        except util.ApiError as e:
            if e.status_code == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")


async def list_duplicates(access_token: str, budget_id: str) -> None:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=access_token) as client:
        try:
            possible_duplicates: dict[tuple[UUID, str], list[tuple[UUID, str]]] = {}

            get_payees_response = await get_payees.asyncio_detailed(
                budget_id,
                client=client,
            )
            payees = util.get_ynab_model(get_payees_response, models.PayeesResponse).data.payees

            for idx, payee in enumerate(payees):
                if should_skip_payee(payee=payee):
                    continue

                filtered_payees = list(payees)
                del filtered_payees[idx]

                for filtered_payee in filtered_payees:
                    if should_skip_payee(payee=filtered_payee):
                        continue

                    normalized_payee_name = normalize_name(payee.name).lower()
                    normalized_filtered_payee_name = normalize_name(filtered_payee.name).lower()
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

            if possible_duplicates:
                for original, duplicates in possible_duplicates.items():
                    print()
                    print(original)
                    for duplicate in duplicates:
                        print(f"\t\t{duplicate}")
                    print()

            else:
                print("No duplicates found.")

        except util.ApiError as e:
            if e.status_code == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")


async def list_unused(access_token: str, budget_id: str) -> None:
    async with ynab.AuthenticatedClient(base_url=YNAB_API_URL, token=access_token) as client:
        try:
            get_payees_response = await get_payees.asyncio_detailed(
                budget_id,
                client=client,
            )
            payees = util.get_ynab_model(get_payees_response, models.PayeesResponse).data.payees

            for payee in payees:
                if should_skip_payee(payee=payee):
                    continue

                try:
                    get_transactions_by_payee_response = await get_transactions_by_payee.asyncio_detailed(
                        budget_id,
                        str(payee.id),
                        client=client,
                    )
                    transactions = util.get_ynab_model(
                        get_transactions_by_payee_response, models.HybridTransactionsResponse
                    ).data.transactions
                except util.ApiError as e:
                    if e.status_code == 429:
                        new_access_token = getpass(prompt="API rate limit exceeded. Enter a new access token: ")
                        client.token = new_access_token
                        get_transactions_by_payee_response = await get_transactions_by_payee.asyncio_detailed(
                            budget_id,
                            str(payee.id),
                            client=client,
                        )
                        transactions = util.get_ynab_model(
                            get_transactions_by_payee_response, models.HybridTransactionsResponse
                        ).data.transactions
                    else:
                        raise e
                num_transactions = len(transactions)

                # List unused payee if no transactions
                if not num_transactions:
                    print(f"{payee.id}: {payee.name}")

        except util.ApiError as e:
            if e.status_code == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")
