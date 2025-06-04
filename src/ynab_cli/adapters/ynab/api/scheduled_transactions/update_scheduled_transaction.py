from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.put_scheduled_transaction_wrapper import PutScheduledTransactionWrapper
from ynab_cli.adapters.ynab.models.scheduled_transaction_response import ScheduledTransactionResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    scheduled_transaction_id: str,
    *,
    body: PutScheduledTransactionWrapper,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/budgets/{budget_id}/scheduled_transactions/{scheduled_transaction_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ScheduledTransactionResponse | None:
    if response.status_code == 200:
        response_200 = ScheduledTransactionResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | ScheduledTransactionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    scheduled_transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PutScheduledTransactionWrapper,
) -> Response[ErrorResponse | ScheduledTransactionResponse]:
    """Updates an existing scheduled transaction

     Updates a single scheduled transaction

    Args:
        budget_id (str):
        scheduled_transaction_id (str):
        body (PutScheduledTransactionWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ScheduledTransactionResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        scheduled_transaction_id=scheduled_transaction_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    scheduled_transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PutScheduledTransactionWrapper,
) -> ErrorResponse | ScheduledTransactionResponse | None:
    """Updates an existing scheduled transaction

     Updates a single scheduled transaction

    Args:
        budget_id (str):
        scheduled_transaction_id (str):
        body (PutScheduledTransactionWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ScheduledTransactionResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        scheduled_transaction_id=scheduled_transaction_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    scheduled_transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PutScheduledTransactionWrapper,
) -> Response[ErrorResponse | ScheduledTransactionResponse]:
    """Updates an existing scheduled transaction

     Updates a single scheduled transaction

    Args:
        budget_id (str):
        scheduled_transaction_id (str):
        body (PutScheduledTransactionWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ScheduledTransactionResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        scheduled_transaction_id=scheduled_transaction_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    scheduled_transaction_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PutScheduledTransactionWrapper,
) -> ErrorResponse | ScheduledTransactionResponse | None:
    """Updates an existing scheduled transaction

     Updates a single scheduled transaction

    Args:
        budget_id (str):
        scheduled_transaction_id (str):
        body (PutScheduledTransactionWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ScheduledTransactionResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            scheduled_transaction_id=scheduled_transaction_id,
            client=client,
            body=body,
        )
    ).parsed
