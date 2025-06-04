from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.put_transaction_wrapper import PutTransactionWrapper
from ynab_cli.adapters.ynab.models.transaction_response import TransactionResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    transaction_id: str,
    *,
    body: PutTransactionWrapper,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/budgets/{budget_id}/transactions/{transaction_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TransactionResponse | None:
    if response.status_code == 200:
        response_200 = TransactionResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
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
    body: PutTransactionWrapper,
) -> Response[ErrorResponse | TransactionResponse]:
    """Updates an existing transaction

     Updates a single transaction

    Args:
        budget_id (str):
        transaction_id (str):
        body (PutTransactionWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        transaction_id=transaction_id,
        body=body,
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
    body: PutTransactionWrapper,
) -> ErrorResponse | TransactionResponse | None:
    """Updates an existing transaction

     Updates a single transaction

    Args:
        budget_id (str):
        transaction_id (str):
        body (PutTransactionWrapper):

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
        body=body,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PutTransactionWrapper,
) -> Response[ErrorResponse | TransactionResponse]:
    """Updates an existing transaction

     Updates a single transaction

    Args:
        budget_id (str):
        transaction_id (str):
        body (PutTransactionWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        transaction_id=transaction_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PutTransactionWrapper,
) -> ErrorResponse | TransactionResponse | None:
    """Updates an existing transaction

     Updates a single transaction

    Args:
        budget_id (str):
        transaction_id (str):
        body (PutTransactionWrapper):

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
            body=body,
        )
    ).parsed
