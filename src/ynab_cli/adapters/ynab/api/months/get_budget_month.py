import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.month_detail_response import MonthDetailResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    month: datetime.date,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/budgets/{budget_id}/months/{month}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | MonthDetailResponse | None:
    if response.status_code == 200:
        response_200 = MonthDetailResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | MonthDetailResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    month: datetime.date,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | MonthDetailResponse]:
    """Single budget month

     Returns a single budget month

    Args:
        budget_id (str):
        month (datetime.date):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MonthDetailResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        month=month,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    month: datetime.date,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | MonthDetailResponse | None:
    """Single budget month

     Returns a single budget month

    Args:
        budget_id (str):
        month (datetime.date):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MonthDetailResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        month=month,
        client=client,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    month: datetime.date,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | MonthDetailResponse]:
    """Single budget month

     Returns a single budget month

    Args:
        budget_id (str):
        month (datetime.date):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MonthDetailResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        month=month,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    month: datetime.date,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | MonthDetailResponse | None:
    """Single budget month

     Returns a single budget month

    Args:
        budget_id (str):
        month (datetime.date):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MonthDetailResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            month=month,
            client=client,
        )
    ).parsed
