import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.category_response import CategoryResponse
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    month: datetime.date,
    category_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/budgets/{budget_id}/months/{month}/categories/{category_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CategoryResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CategoryResponse.from_dict(response.json())

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
) -> Response[CategoryResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    month: datetime.date,
    category_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CategoryResponse | ErrorResponse]:
    """Single category for a specific budget month

     Returns a single category for a specific budget month.  Amounts (budgeted, activity, balance, etc.)
    are specific to the current budget month (UTC).

    Args:
        budget_id (str):
        month (datetime.date):
        category_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CategoryResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        month=month,
        category_id=category_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    month: datetime.date,
    category_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> CategoryResponse | ErrorResponse | None:
    """Single category for a specific budget month

     Returns a single category for a specific budget month.  Amounts (budgeted, activity, balance, etc.)
    are specific to the current budget month (UTC).

    Args:
        budget_id (str):
        month (datetime.date):
        category_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CategoryResponse, ErrorResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        month=month,
        category_id=category_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    month: datetime.date,
    category_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CategoryResponse | ErrorResponse]:
    """Single category for a specific budget month

     Returns a single category for a specific budget month.  Amounts (budgeted, activity, balance, etc.)
    are specific to the current budget month (UTC).

    Args:
        budget_id (str):
        month (datetime.date):
        category_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CategoryResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        month=month,
        category_id=category_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    month: datetime.date,
    category_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> CategoryResponse | ErrorResponse | None:
    """Single category for a specific budget month

     Returns a single category for a specific budget month.  Amounts (budgeted, activity, balance, etc.)
    are specific to the current budget month (UTC).

    Args:
        budget_id (str):
        month (datetime.date):
        category_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CategoryResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            month=month,
            category_id=category_id,
            client=client,
        )
    ).parsed
