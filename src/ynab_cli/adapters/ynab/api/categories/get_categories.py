from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.categories_response import CategoriesResponse
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.types import UNSET, Response, Unset


def _get_kwargs(
    plan_id: str,
    *,
    last_knowledge_of_server: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["last_knowledge_of_server"] = last_knowledge_of_server

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/plans/{plan_id}/categories".format(
            plan_id=quote(str(plan_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> CategoriesResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CategoriesResponse.from_dict(response.json())

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
) -> Response[CategoriesResponse | ErrorResponse]:
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
    last_knowledge_of_server: int | Unset = UNSET,
) -> Response[CategoriesResponse | ErrorResponse]:
    """Get all categories

     Returns all categories grouped by category group.  Amounts (assigned, activity, available, etc.) are
    specific to the current plan month (UTC).

    Args:
        plan_id (str):
        last_knowledge_of_server (int | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoriesResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
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
    last_knowledge_of_server: int | Unset = UNSET,
) -> CategoriesResponse | ErrorResponse | None:
    """Get all categories

     Returns all categories grouped by category group.  Amounts (assigned, activity, available, etc.) are
    specific to the current plan month (UTC).

    Args:
        plan_id (str):
        last_knowledge_of_server (int | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoriesResponse | ErrorResponse
    """

    return sync_detailed(
        plan_id=plan_id,
        client=client,
        last_knowledge_of_server=last_knowledge_of_server,
    ).parsed


async def asyncio_detailed(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_knowledge_of_server: int | Unset = UNSET,
) -> Response[CategoriesResponse | ErrorResponse]:
    """Get all categories

     Returns all categories grouped by category group.  Amounts (assigned, activity, available, etc.) are
    specific to the current plan month (UTC).

    Args:
        plan_id (str):
        last_knowledge_of_server (int | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoriesResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        last_knowledge_of_server=last_knowledge_of_server,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    last_knowledge_of_server: int | Unset = UNSET,
) -> CategoriesResponse | ErrorResponse | None:
    """Get all categories

     Returns all categories grouped by category group.  Amounts (assigned, activity, available, etc.) are
    specific to the current plan month (UTC).

    Args:
        plan_id (str):
        last_knowledge_of_server (int | Unset):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoriesResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            plan_id=plan_id,
            client=client,
            last_knowledge_of_server=last_knowledge_of_server,
        )
    ).parsed
