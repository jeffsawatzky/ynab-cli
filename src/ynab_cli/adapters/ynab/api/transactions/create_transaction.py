from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.post_transactions_wrapper import PostTransactionsWrapper
from ynab_cli.adapters.ynab.models.save_transactions_response import SaveTransactionsResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    *,
    body: PostTransactionsWrapper,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/budgets/{budget_id}/transactions",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SaveTransactionsResponse | None:
    if response.status_code == 201:
        response_201 = SaveTransactionsResponse.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatusError(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | SaveTransactionsResponse]:
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
    body: PostTransactionsWrapper,
) -> Response[ErrorResponse | SaveTransactionsResponse]:
    """Create a single transaction or multiple transactions

     Creates a single transaction or multiple transactions.  If you provide a body containing a
    `transaction` object, a single transaction will be created and if you provide a body containing a
    `transactions` array, multiple transactions will be created.  Scheduled transactions (transactions
    with a future date) cannot be created on this endpoint.

    Args:
        budget_id (str):
        body (PostTransactionsWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SaveTransactionsResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostTransactionsWrapper,
) -> ErrorResponse | SaveTransactionsResponse | None:
    """Create a single transaction or multiple transactions

     Creates a single transaction or multiple transactions.  If you provide a body containing a
    `transaction` object, a single transaction will be created and if you provide a body containing a
    `transactions` array, multiple transactions will be created.  Scheduled transactions (transactions
    with a future date) cannot be created on this endpoint.

    Args:
        budget_id (str):
        body (PostTransactionsWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SaveTransactionsResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostTransactionsWrapper,
) -> Response[ErrorResponse | SaveTransactionsResponse]:
    """Create a single transaction or multiple transactions

     Creates a single transaction or multiple transactions.  If you provide a body containing a
    `transaction` object, a single transaction will be created and if you provide a body containing a
    `transactions` array, multiple transactions will be created.  Scheduled transactions (transactions
    with a future date) cannot be created on this endpoint.

    Args:
        budget_id (str):
        body (PostTransactionsWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SaveTransactionsResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostTransactionsWrapper,
) -> ErrorResponse | SaveTransactionsResponse | None:
    """Create a single transaction or multiple transactions

     Creates a single transaction or multiple transactions.  If you provide a body containing a
    `transaction` object, a single transaction will be created and if you provide a body containing a
    `transactions` array, multiple transactions will be created.  Scheduled transactions (transactions
    with a future date) cannot be created on this endpoint.

    Args:
        budget_id (str):
        body (PostTransactionsWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SaveTransactionsResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            client=client,
            body=body,
        )
    ).parsed
