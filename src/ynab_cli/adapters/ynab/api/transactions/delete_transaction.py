from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.transaction_response import TransactionResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    transaction_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/budgets/{budget_id}/transactions/{transaction_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TransactionResponse | None:
    if response.status_code == 200:
        response_200 = TransactionResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatusError(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | TransactionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | TransactionResponse]:
    """Deletes an existing transaction

     Deletes a transaction

    Args:
        budget_id (str):
        transaction_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        transaction_id=transaction_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | TransactionResponse | None:
    """Deletes an existing transaction

     Deletes a transaction

    Args:
        budget_id (str):
        transaction_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        transaction_id=transaction_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | TransactionResponse]:
    """Deletes an existing transaction

     Deletes a transaction

    Args:
        budget_id (str):
        transaction_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        transaction_id=transaction_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | TransactionResponse | None:
    """Deletes an existing transaction

     Deletes a transaction

    Args:
        budget_id (str):
        transaction_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            transaction_id=transaction_id,
            client=client,
        )
    ).parsed
