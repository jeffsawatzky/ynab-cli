from http import HTTPStatus
from typing import Any

import httpx2

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.plan_summary_response import PlanSummaryResponse
from ynab_cli.adapters.ynab.types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_accounts: bool | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["include_accounts"] = include_accounts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/plans",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> ErrorResponse | PlanSummaryResponse | None:
    if response.status_code == 200:
        response_200 = PlanSummaryResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | PlanSummaryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    include_accounts: bool | Unset = UNSET,
) -> Response[ErrorResponse | PlanSummaryResponse]:
    """Get all plans

     Returns plans list with summary information

    Args:
        include_accounts (bool | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PlanSummaryResponse]
    """

    kwargs = _get_kwargs(
        include_accounts=include_accounts,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    include_accounts: bool | Unset = UNSET,
) -> ErrorResponse | PlanSummaryResponse | None:
    """Get all plans

     Returns plans list with summary information

    Args:
        include_accounts (bool | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PlanSummaryResponse
    """

    return sync_detailed(
        client=client,
        include_accounts=include_accounts,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    include_accounts: bool | Unset = UNSET,
) -> Response[ErrorResponse | PlanSummaryResponse]:
    """Get all plans

     Returns plans list with summary information

    Args:
        include_accounts (bool | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PlanSummaryResponse]
    """

    kwargs = _get_kwargs(
        include_accounts=include_accounts,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    include_accounts: bool | Unset = UNSET,
) -> ErrorResponse | PlanSummaryResponse | None:
    """Get all plans

     Returns plans list with summary information

    Args:
        include_accounts (bool | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PlanSummaryResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            include_accounts=include_accounts,
        )
    ).parsed
