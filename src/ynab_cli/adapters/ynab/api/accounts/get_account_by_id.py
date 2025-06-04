from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.account_response import AccountResponse
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    account_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/budgets/{budget_id}/accounts/{account_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AccountResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = AccountResponse.from_dict(response.json())

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
) -> Response[AccountResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    account_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AccountResponse | ErrorResponse]:
    """Single account

     Returns a single account

    Args:
        budget_id (str):
        account_id (UUID):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        account_id=account_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    account_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> AccountResponse | ErrorResponse | None:
    """Single account

     Returns a single account

    Args:
        budget_id (str):
        account_id (UUID):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountResponse, ErrorResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        account_id=account_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    account_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AccountResponse | ErrorResponse]:
    """Single account

     Returns a single account

    Args:
        budget_id (str):
        account_id (UUID):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        account_id=account_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    account_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> AccountResponse | ErrorResponse | None:
    """Single account

     Returns a single account

    Args:
        budget_id (str):
        account_id (UUID):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            account_id=account_id,
            client=client,
        )
    ).parsed
