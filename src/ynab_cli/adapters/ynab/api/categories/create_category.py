from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ynab_cli.adapters.ynab import errors
from ynab_cli.adapters.ynab.client import AuthenticatedClient, Client
from ynab_cli.adapters.ynab.models.error_response import ErrorResponse
from ynab_cli.adapters.ynab.models.post_category_wrapper import PostCategoryWrapper
from ynab_cli.adapters.ynab.models.save_category_response import SaveCategoryResponse
from ynab_cli.adapters.ynab.types import Response


def _get_kwargs(
    plan_id: str,
    *,
    body: PostCategoryWrapper,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/plans/{plan_id}/categories".format(
            plan_id=quote(str(plan_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> ErrorResponse | SaveCategoryResponse | None:
    if response.status_code == 201:
        response_201 = SaveCategoryResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatusError(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[ErrorResponse | SaveCategoryResponse]:
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
    body: PostCategoryWrapper,
) -> Response[ErrorResponse | SaveCategoryResponse]:
    """Create a category

     Creates a new category

    Args:
        plan_id (str):
        body (PostCategoryWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SaveCategoryResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostCategoryWrapper,
) -> ErrorResponse | SaveCategoryResponse | None:
    """Create a category

     Creates a new category

    Args:
        plan_id (str):
        body (PostCategoryWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SaveCategoryResponse
    """

    return sync_detailed(
        plan_id=plan_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostCategoryWrapper,
) -> Response[ErrorResponse | SaveCategoryResponse]:
    """Create a category

     Creates a new category

    Args:
        plan_id (str):
        body (PostCategoryWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SaveCategoryResponse]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    plan_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostCategoryWrapper,
) -> ErrorResponse | SaveCategoryResponse | None:
    """Create a category

     Creates a new category

    Args:
        plan_id (str):
        body (PostCategoryWrapper):

    Raises:
        errors.UnexpectedStatusError: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SaveCategoryResponse
    """

    return (
        await asyncio_detailed(
            plan_id=plan_id,
            client=client,
            body=body,
        )
    ).parsed
