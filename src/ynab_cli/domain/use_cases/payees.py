import re
from getpass import getpass

from rapidfuzz import fuzz

from ynab_cli.adapters import ynab
from ynab_cli.adapters.ynab import api, models
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
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            payees_response = await api.PayeesApi(api_client).get_payees(budget_id)
            payees = payees_response.data.payees

            for payee in payees:
                if should_skip_payee(payee=payee):
                    continue

                normalized_name = normalize_name(payee.name)
                if normalized_name != payee.name:
                    print(f"{payee.id}: {payee.name} -> {normalized_name}")

                    if not dry_run:
                        try:
                            await api.PayeesApi(api_client).update_payee(
                                budget_id,
                                payee.id,
                                models.PatchPayeeWrapper(payee=models.SavePayee(name=normalized_name)),
                            )
                        except ynab.ApiError as e:
                            if e.status == 429:
                                new_access_token = getpass(prompt="API rate limit exceeded. Enter a new access token: ")
                                api_client.configuration.access_token = new_access_token
                                await api.PayeesApi(api_client).update_payee(
                                    budget_id,
                                    payee.id,
                                    models.PatchPayeeWrapper(payee=models.SavePayee(name=normalized_name)),
                                )
                            else:
                                raise e

        except ynab.ApiError as e:
            if e.status == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")


async def list_duplicates(access_token: str, budget_id: str) -> None:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            possible_duplicates: dict[tuple[str, str], list[tuple[str, str]]] = {}

            payees_response: models.PayeesResponse = await api.PayeesApi(api_client).get_payees(budget_id)
            payees = payees_response.data.payees

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

        except ynab.ApiError as e:
            if e.status == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")


async def list_unused(access_token: str, budget_id: str) -> None:
    configuration = ynab.Configuration(
        host=YNAB_API_URL,
        access_token=access_token,
    )

    async with ynab.ApiClient(configuration) as api_client:
        try:
            payees_response: models.PayeesResponse = await api.PayeesApi(api_client).get_payees(budget_id)
            payees = payees_response.data.payees

            for payee in payees:
                if should_skip_payee(payee=payee):
                    continue

                try:
                    payee_transactions_response = await api.TransactionsApi(api_client).get_transactions_by_payee(
                        budget_id, payee.id
                    )
                except ynab.ApiError as e:
                    if e.status == 429:
                        new_access_token = getpass(prompt="API rate limit exceeded. Enter a new access token: ")
                        api_client.configuration.access_token = new_access_token
                        payee_transactions_response = await api.TransactionsApi(api_client).get_transactions_by_payee(
                            budget_id, payee.id
                        )
                    else:
                        raise e
                num_transactions = len(payee_transactions_response.data.transactions)

                # List unused payee if no transactions
                if not num_transactions:
                    print(f"{payee.id}: {payee.name}")

        except ynab.ApiError as e:
            if e.status == 429:
                print("API rate limit exceeded. Try again later, or get a new access token.")
            else:
                print(f"Exception when calling YNAB: {e}\n")
