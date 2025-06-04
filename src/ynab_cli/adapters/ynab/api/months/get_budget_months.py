from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.month_summaries_response import MonthSummariesResponse
from ynab_cli.adapters.ynab.types import UNSET, Response, Unset


def _get_kwargs(
    budget_id: str,
    *,
    last_knowledge_of_server: Unset | int = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["last_knowledge_of_server"] = last_knowledge_of_server

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/budgets/{budget_id}/months",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | MonthSummariesResponse | None:
    if response.status_code == 200:
        response_200 = MonthSummariesResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | MonthSummariesResponse]:
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
    last_knowledge_of_server: Unset | int = UNSET,
) -> Response[ErrorResponse | MonthSummariesResponse]:
    """List budget months

     Returns all budget months

    Args:
        budget_id (str):
        last_knowledge_of_server (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MonthSummariesResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        last_knowledge_of_server=last_knowledge_of_server,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_knowledge_of_server: Unset | int = UNSET,
) -> ErrorResponse | MonthSummariesResponse | None:
    """List budget months

     Returns all budget months

    Args:
        budget_id (str):
        last_knowledge_of_server (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MonthSummariesResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        client=client,
        last_knowledge_of_server=last_knowledge_of_server,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_knowledge_of_server: Unset | int = UNSET,
) -> Response[ErrorResponse | MonthSummariesResponse]:
    """List budget months

     Returns all budget months

    Args:
        budget_id (str):
        last_knowledge_of_server (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MonthSummariesResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        last_knowledge_of_server=last_knowledge_of_server,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_knowledge_of_server: Unset | int = UNSET,
) -> ErrorResponse | MonthSummariesResponse | None:
    """List budget months

     Returns all budget months

    Args:
        budget_id (str):
        last_knowledge_of_server (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MonthSummariesResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            client=client,
            last_knowledge_of_server=last_knowledge_of_server,
        )
    ).parsed
