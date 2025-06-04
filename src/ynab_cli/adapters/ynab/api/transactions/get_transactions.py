import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.get_transactions_type import GetTransactionsType
from ynab_cli.adapters.ynab.models.transactions_response import TransactionsResponse
from ynab_cli.adapters.ynab.types import UNSET, Response, Unset


def _get_kwargs(
    budget_id: str,
    *,
    since_date: Unset | datetime.date = UNSET,
    type_: Unset | GetTransactionsType = UNSET,
    last_knowledge_of_server: Unset | int = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_since_date: Unset | str = UNSET
    if not isinstance(since_date, Unset):
        json_since_date = since_date.isoformat()
    params["since_date"] = json_since_date

    json_type_: Unset | str = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params["last_knowledge_of_server"] = last_knowledge_of_server

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/budgets/{budget_id}/transactions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TransactionsResponse | None:
    if response.status_code == 200:
        response_200 = TransactionsResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatusError(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | TransactionsResponse]:
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
    since_date: Unset | datetime.date = UNSET,
    type_: Unset | GetTransactionsType = UNSET,
    last_knowledge_of_server: Unset | int = UNSET,
) -> Response[ErrorResponse | TransactionsResponse]:
    """List transactions

     Returns budget transactions, excluding any pending transactions

    Args:
        budget_id (str):
        since_date (Union[Unset, datetime.date]):
        type_ (Union[Unset, GetTransactionsType]):
        last_knowledge_of_server (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionsResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        since_date=since_date,
        type_=type_,
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
    since_date: Unset | datetime.date = UNSET,
    type_: Unset | GetTransactionsType = UNSET,
    last_knowledge_of_server: Unset | int = UNSET,
) -> ErrorResponse | TransactionsResponse | None:
    """List transactions

     Returns budget transactions, excluding any pending transactions

    Args:
        budget_id (str):
        since_date (Union[Unset, datetime.date]):
        type_ (Union[Unset, GetTransactionsType]):
        last_knowledge_of_server (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionsResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        client=client,
        since_date=since_date,
        type_=type_,
        last_knowledge_of_server=last_knowledge_of_server,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
    since_date: Unset | datetime.date = UNSET,
    type_: Unset | GetTransactionsType = UNSET,
    last_knowledge_of_server: Unset | int = UNSET,
) -> Response[ErrorResponse | TransactionsResponse]:
    """List transactions

     Returns budget transactions, excluding any pending transactions

    Args:
        budget_id (str):
        since_date (Union[Unset, datetime.date]):
        type_ (Union[Unset, GetTransactionsType]):
        last_knowledge_of_server (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionsResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        since_date=since_date,
        type_=type_,
        last_knowledge_of_server=last_knowledge_of_server,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    *,
    client: AuthenticatedClient | Client,
    since_date: Unset | datetime.date = UNSET,
    type_: Unset | GetTransactionsType = UNSET,
    last_knowledge_of_server: Unset | int = UNSET,
) -> ErrorResponse | TransactionsResponse | None:
    """List transactions

     Returns budget transactions, excluding any pending transactions

    Args:
        budget_id (str):
        since_date (Union[Unset, datetime.date]):
        type_ (Union[Unset, GetTransactionsType]):
        last_knowledge_of_server (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionsResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            client=client,
            since_date=since_date,
            type_=type_,
            last_knowledge_of_server=last_knowledge_of_server,
        )
    ).parsed
