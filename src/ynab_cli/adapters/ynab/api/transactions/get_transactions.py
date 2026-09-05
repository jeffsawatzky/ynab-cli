import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.get_transactions_type import GetTransactionsType
from ynab_cli.adapters.ynab.models.transactions_response import TransactionsResponse
from ynab_cli.adapters.ynab.types import UNSET, Response, Unset


def _get_kwargs(
    plan_id: str,
    *,
    since_date: datetime.date | Unset = UNSET,
    until_date: datetime.date | Unset = UNSET,
    type_: GetTransactionsType | Unset = UNSET,
    last_knowledge_of_server: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_since_date: str | Unset = UNSET
    if not isinstance(since_date, Unset):
        json_since_date = since_date.isoformat()
    params["since_date"] = json_since_date

    json_until_date: str | Unset = UNSET
    if not isinstance(until_date, Unset):
        json_until_date = until_date.isoformat()
    params["until_date"] = json_until_date

    json_type_: str | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params["last_knowledge_of_server"] = last_knowledge_of_server

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/plans/{plan_id}/transactions".format(
            plan_id=quote(str(plan_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
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
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[ErrorResponse | TransactionsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    since_date: datetime.date | Unset = UNSET,
    until_date: datetime.date | Unset = UNSET,
    type_: GetTransactionsType | Unset = UNSET,
    last_knowledge_of_server: int | Unset = UNSET,
) -> Response[ErrorResponse | TransactionsResponse]:
    """Get transactions

     Returns plan transactions, excluding any pending transactions

    Args:
        plan_id (str):
        since_date (datetime.date | Unset):
        until_date (datetime.date | Unset):
        type_ (GetTransactionsType | Unset):
        last_knowledge_of_server (int | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TransactionsResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        since_date=since_date,
        until_date=until_date,
        type_=type_,
        last_knowledge_of_server=last_knowledge_of_server,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    since_date: datetime.date | Unset = UNSET,
    until_date: datetime.date | Unset = UNSET,
    type_: GetTransactionsType | Unset = UNSET,
    last_knowledge_of_server: int | Unset = UNSET,
) -> ErrorResponse | TransactionsResponse | None:
    """Get transactions

     Returns plan transactions, excluding any pending transactions

    Args:
        plan_id (str):
        since_date (datetime.date | Unset):
        until_date (datetime.date | Unset):
        type_ (GetTransactionsType | Unset):
        last_knowledge_of_server (int | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TransactionsResponse
    """

    return sync_detailed(
        plan_id=plan_id,
        client=client,
        since_date=since_date,
        until_date=until_date,
        type_=type_,
        last_knowledge_of_server=last_knowledge_of_server,
    ).parsed


async def asyncio_detailed(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    since_date: datetime.date | Unset = UNSET,
    until_date: datetime.date | Unset = UNSET,
    type_: GetTransactionsType | Unset = UNSET,
    last_knowledge_of_server: int | Unset = UNSET,
) -> Response[ErrorResponse | TransactionsResponse]:
    """Get transactions

     Returns plan transactions, excluding any pending transactions

    Args:
        plan_id (str):
        since_date (datetime.date | Unset):
        until_date (datetime.date | Unset):
        type_ (GetTransactionsType | Unset):
        last_knowledge_of_server (int | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TransactionsResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        since_date=since_date,
        until_date=until_date,
        type_=type_,
        last_knowledge_of_server=last_knowledge_of_server,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    since_date: datetime.date | Unset = UNSET,
    until_date: datetime.date | Unset = UNSET,
    type_: GetTransactionsType | Unset = UNSET,
    last_knowledge_of_server: int | Unset = UNSET,
) -> ErrorResponse | TransactionsResponse | None:
    """Get transactions

     Returns plan transactions, excluding any pending transactions

    Args:
        plan_id (str):
        since_date (datetime.date | Unset):
        until_date (datetime.date | Unset):
        type_ (GetTransactionsType | Unset):
        last_knowledge_of_server (int | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TransactionsResponse
    """

    return (
        await asyncio_detailed(
            plan_id=plan_id,
            client=client,
            since_date=since_date,
            until_date=until_date,
            type_=type_,
            last_knowledge_of_server=last_knowledge_of_server,
        )
    ).parsed
