from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.transactions_import_response import TransactionsImportResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/budgets/{budget_id}/transactions/import",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TransactionsImportResponse | None:
    if response.status_code == 200:
        response_200 = TransactionsImportResponse.from_dict(response.json())

        return response_200
    if response.status_code == 201:
        response_201 = TransactionsImportResponse.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatusError(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | TransactionsImportResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | TransactionsImportResponse]:
    r"""Import transactions

     Imports available transactions on all linked accounts for the given budget.  Linked accounts allow
    transactions to be imported directly from a specified financial institution and this endpoint
    initiates that import.  Sending a request to this endpoint is the equivalent of clicking \"Import\"
    on each account in the web application or tapping the \"New Transactions\" banner in the mobile
    applications.  The response for this endpoint contains the transaction ids that have been imported.

    Args:
        budget_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionsImportResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | TransactionsImportResponse | None:
    r"""Import transactions

     Imports available transactions on all linked accounts for the given budget.  Linked accounts allow
    transactions to be imported directly from a specified financial institution and this endpoint
    initiates that import.  Sending a request to this endpoint is the equivalent of clicking \"Import\"
    on each account in the web application or tapping the \"New Transactions\" banner in the mobile
    applications.  The response for this endpoint contains the transaction ids that have been imported.

    Args:
        budget_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionsImportResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | TransactionsImportResponse]:
    r"""Import transactions

     Imports available transactions on all linked accounts for the given budget.  Linked accounts allow
    transactions to be imported directly from a specified financial institution and this endpoint
    initiates that import.  Sending a request to this endpoint is the equivalent of clicking \"Import\"
    on each account in the web application or tapping the \"New Transactions\" banner in the mobile
    applications.  The response for this endpoint contains the transaction ids that have been imported.

    Args:
        budget_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionsImportResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | TransactionsImportResponse | None:
    r"""Import transactions

     Imports available transactions on all linked accounts for the given budget.  Linked accounts allow
    transactions to be imported directly from a specified financial institution and this endpoint
    initiates that import.  Sending a request to this endpoint is the equivalent of clicking \"Import\"
    on each account in the web application or tapping the \"New Transactions\" banner in the mobile
    applications.  The response for this endpoint contains the transaction ids that have been imported.

    Args:
        budget_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionsImportResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            client=client,
        )
    ).parsed
