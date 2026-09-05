from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.transactions_import_response import TransactionsImportResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    plan_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/plans/{plan_id}/transactions/import".format(
            plan_id=quote(str(plan_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
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
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[ErrorResponse | TransactionsImportResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | TransactionsImportResponse]:
    """Import transactions

     Imports available transactions on all linked accounts for the given plan.  Linked accounts allow
    transactions to be imported directly from a specified financial institution and this endpoint
    initiates that import.  Sending a request to this endpoint is the equivalent of clicking "Import" on
    each account in the web application or tapping the "New Transactions" banner in the mobile
    applications.  The response for this endpoint contains the transaction ids that have been imported.

    Args:
        plan_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TransactionsImportResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | TransactionsImportResponse | None:
    """Import transactions

     Imports available transactions on all linked accounts for the given plan.  Linked accounts allow
    transactions to be imported directly from a specified financial institution and this endpoint
    initiates that import.  Sending a request to this endpoint is the equivalent of clicking "Import" on
    each account in the web application or tapping the "New Transactions" banner in the mobile
    applications.  The response for this endpoint contains the transaction ids that have been imported.

    Args:
        plan_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TransactionsImportResponse
    """

    return sync_detailed(
        plan_id=plan_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | TransactionsImportResponse]:
    """Import transactions

     Imports available transactions on all linked accounts for the given plan.  Linked accounts allow
    transactions to be imported directly from a specified financial institution and this endpoint
    initiates that import.  Sending a request to this endpoint is the equivalent of clicking "Import" on
    each account in the web application or tapping the "New Transactions" banner in the mobile
    applications.  The response for this endpoint contains the transaction ids that have been imported.

    Args:
        plan_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TransactionsImportResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | TransactionsImportResponse | None:
    """Import transactions

     Imports available transactions on all linked accounts for the given plan.  Linked accounts allow
    transactions to be imported directly from a specified financial institution and this endpoint
    initiates that import.  Sending a request to this endpoint is the equivalent of clicking "Import" on
    each account in the web application or tapping the "New Transactions" banner in the mobile
    applications.  The response for this endpoint contains the transaction ids that have been imported.

    Args:
        plan_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TransactionsImportResponse
    """

    return (
        await asyncio_detailed(
            plan_id=plan_id,
            client=client,
        )
    ).parsed
