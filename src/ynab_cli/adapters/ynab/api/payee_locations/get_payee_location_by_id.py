from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.payee_location_response import PayeeLocationResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    plan_id: str,
    payee_location_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/plans/{plan_id}/payee_locations/{payee_location_id}".format(
            plan_id=quote(str(plan_id), safe=""),
            payee_location_id=quote(str(payee_location_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> ErrorResponse | PayeeLocationResponse | None:
    if response.status_code == 200:
        response_200 = PayeeLocationResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | PayeeLocationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    plan_id: str,
    payee_location_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | PayeeLocationResponse]:
    """Get a payee location

     Returns a single payee location

    Args:
        plan_id (str):
        payee_location_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PayeeLocationResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        payee_location_id=payee_location_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    plan_id: str,
    payee_location_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | PayeeLocationResponse | None:
    """Get a payee location

     Returns a single payee location

    Args:
        plan_id (str):
        payee_location_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PayeeLocationResponse
    """

    return sync_detailed(
        plan_id=plan_id,
        payee_location_id=payee_location_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    plan_id: str,
    payee_location_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | PayeeLocationResponse]:
    """Get a payee location

     Returns a single payee location

    Args:
        plan_id (str):
        payee_location_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PayeeLocationResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        payee_location_id=payee_location_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    plan_id: str,
    payee_location_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | PayeeLocationResponse | None:
    """Get a payee location

     Returns a single payee location

    Args:
        plan_id (str):
        payee_location_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PayeeLocationResponse
    """

    return (
        await asyncio_detailed(
            plan_id=plan_id,
            payee_location_id=payee_location_id,
            client=client,
        )
    ).parsed
