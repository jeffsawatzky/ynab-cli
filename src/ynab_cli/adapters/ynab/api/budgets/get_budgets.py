from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.budget_summary_response import BudgetSummaryResponse
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_accounts: Unset | bool = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_accounts"] = include_accounts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/budgets",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BudgetSummaryResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = BudgetSummaryResponse.from_dict(response.json())

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
) -> Response[BudgetSummaryResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    include_accounts: Unset | bool = UNSET,
) -> Response[BudgetSummaryResponse | ErrorResponse]:
    """List budgets

     Returns budgets list with summary information

    Args:
        include_accounts (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BudgetSummaryResponse, ErrorResponse]]
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
    include_accounts: Unset | bool = UNSET,
) -> BudgetSummaryResponse | ErrorResponse | None:
    """List budgets

     Returns budgets list with summary information

    Args:
        include_accounts (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BudgetSummaryResponse, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        include_accounts=include_accounts,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    include_accounts: Unset | bool = UNSET,
) -> Response[BudgetSummaryResponse | ErrorResponse]:
    """List budgets

     Returns budgets list with summary information

    Args:
        include_accounts (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BudgetSummaryResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        include_accounts=include_accounts,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    include_accounts: Unset | bool = UNSET,
) -> BudgetSummaryResponse | ErrorResponse | None:
    """List budgets

     Returns budgets list with summary information

    Args:
        include_accounts (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BudgetSummaryResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            include_accounts=include_accounts,
        )
    ).parsed
