from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.patch_payee_wrapper import PatchPayeeWrapper
from ynab_cli.adapters.ynab.models.save_payee_response import SavePayeeResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    payee_id: str,
    *,
    body: PatchPayeeWrapper,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/budgets/{budget_id}/payees/{payee_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SavePayeeResponse | None:
    if response.status_code == 200:
        response_200 = SavePayeeResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatusError(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | SavePayeeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    payee_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchPayeeWrapper,
) -> Response[ErrorResponse | SavePayeeResponse]:
    """Update a payee

     Update a payee

    Args:
        budget_id (str):
        payee_id (str):
        body (PatchPayeeWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SavePayeeResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        payee_id=payee_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    payee_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchPayeeWrapper,
) -> ErrorResponse | SavePayeeResponse | None:
    """Update a payee

     Update a payee

    Args:
        budget_id (str):
        payee_id (str):
        body (PatchPayeeWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SavePayeeResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        payee_id=payee_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    payee_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchPayeeWrapper,
) -> Response[ErrorResponse | SavePayeeResponse]:
    """Update a payee

     Update a payee

    Args:
        budget_id (str):
        payee_id (str):
        body (PatchPayeeWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SavePayeeResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        payee_id=payee_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    payee_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchPayeeWrapper,
) -> ErrorResponse | SavePayeeResponse | None:
    """Update a payee

     Update a payee

    Args:
        budget_id (str):
        payee_id (str):
        body (PatchPayeeWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SavePayeeResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            payee_id=payee_id,
            client=client,
            body=body,
        )
    ).parsed
