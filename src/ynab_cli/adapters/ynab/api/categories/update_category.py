from http import HTTPStatus
from typing import Any

import httpx

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.patch_category_wrapper import PatchCategoryWrapper
from ynab_cli.adapters.ynab.models.save_category_response import SaveCategoryResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    budget_id: str,
    category_id: str,
    *,
    body: PatchCategoryWrapper,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/budgets/{budget_id}/categories/{category_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SaveCategoryResponse | None:
    if response.status_code == 200:
        response_200 = SaveCategoryResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | SaveCategoryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    budget_id: str,
    category_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchCategoryWrapper,
) -> Response[ErrorResponse | SaveCategoryResponse]:
    """Update a category

     Update a category

    Args:
        budget_id (str):
        category_id (str):
        body (PatchCategoryWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SaveCategoryResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        category_id=category_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    budget_id: str,
    category_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchCategoryWrapper,
) -> ErrorResponse | SaveCategoryResponse | None:
    """Update a category

     Update a category

    Args:
        budget_id (str):
        category_id (str):
        body (PatchCategoryWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SaveCategoryResponse]
    """

    return sync_detailed(
        budget_id=budget_id,
        category_id=category_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    budget_id: str,
    category_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchCategoryWrapper,
) -> Response[ErrorResponse | SaveCategoryResponse]:
    """Update a category

     Update a category

    Args:
        budget_id (str):
        category_id (str):
        body (PatchCategoryWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SaveCategoryResponse]]
    """

    kwargs = _get_kwargs(
        budget_id=budget_id,
        category_id=category_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    budget_id: str,
    category_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchCategoryWrapper,
) -> ErrorResponse | SaveCategoryResponse | None:
    """Update a category

     Update a category

    Args:
        budget_id (str):
        category_id (str):
        body (PatchCategoryWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SaveCategoryResponse]
    """

    return (
        await asyncio_detailed(
            budget_id=budget_id,
            category_id=category_id,
            client=client,
            body=body,
        )
    ).parsed
