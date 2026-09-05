from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx2

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.account_response import AccountResponse
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    plan_id: str,
    account_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/plans/{plan_id}/accounts/{account_id}".format(
            plan_id=quote(str(plan_id), safe=""),
            account_id=quote(str(account_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
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
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[AccountResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    plan_id: str,
    account_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AccountResponse | ErrorResponse]:
    """Get an account

     Returns a single account

    Args:
        plan_id (str):
        account_id (UUID):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        account_id=account_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    plan_id: str,
    account_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> AccountResponse | ErrorResponse | None:
    """Get an account

     Returns a single account

    Args:
        plan_id (str):
        account_id (UUID):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountResponse | ErrorResponse
    """

    return sync_detailed(
        plan_id=plan_id,
        account_id=account_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    plan_id: str,
    account_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AccountResponse | ErrorResponse]:
    """Get an account

     Returns a single account

    Args:
        plan_id (str):
        account_id (UUID):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        account_id=account_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    plan_id: str,
    account_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> AccountResponse | ErrorResponse | None:
    """Get an account

     Returns a single account

    Args:
        plan_id (str):
        account_id (UUID):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            plan_id=plan_id,
            account_id=account_id,
            client=client,
        )
    ).parsed
