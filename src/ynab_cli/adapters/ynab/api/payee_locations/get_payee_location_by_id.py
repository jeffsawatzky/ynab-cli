from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.payee_location_response import PayeeLocationResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    payee_location_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/budgets/{budget_id}/payee_locations/{payee_location_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
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
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | PayeeLocationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    payee_location_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | PayeeLocationResponse]:
    """Single payee location

     Returns a single payee location

    Args:
        budget_id (str):
        payee_location_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PayeeLocationResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        payee_location_id=payee_location_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    payee_location_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | PayeeLocationResponse | None:
    """Single payee location

     Returns a single payee location

    Args:
        budget_id (str):
        payee_location_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PayeeLocationResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        payee_location_id=payee_location_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    payee_location_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | PayeeLocationResponse]:
    """Single payee location

     Returns a single payee location

    Args:
        budget_id (str):
        payee_location_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PayeeLocationResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        payee_location_id=payee_location_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    payee_location_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | PayeeLocationResponse | None:
    """Single payee location

     Returns a single payee location

    Args:
        budget_id (str):
        payee_location_id (str):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PayeeLocationResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            payee_location_id=payee_location_id,
            client=client,
        )
    ).parsed
