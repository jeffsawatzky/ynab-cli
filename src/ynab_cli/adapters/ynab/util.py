from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, TypeVar

from ynab_cli.adapters.ynab import AuthenticatedClient
from ynab_cli.domain.ports.io import IO

from .models import ErrorDetail, ErrorResponse
from .types import Response

P = ParamSpec("P")
R = TypeVar("R")


class ApiError(Exception):
    """Raised by API functions when the response status is not 200 OK and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, error_detail: ErrorDetail | None = None):
        self.status_code = status_code
        self.error_detail = error_detail

        super().__init__(f"Unexpected status code: {status_code}")


def get_parsed_response_data(response: Response[ErrorResponse | R]) -> R | None:
    parsed = response.parsed

    if isinstance(parsed, ErrorResponse):
        error_detail = parsed.error
        raise ApiError(status_code=response.status_code, error_detail=error_detail)

    if response.status_code >= 400:
        error_detail = ErrorDetail(
            id=str(response.status_code.value),
            name="unknown_error",
            detail="An unknown error occurred",
        )
        raise ApiError(status_code=response.status_code, error_detail=error_detail)

    return parsed


async def run_asyncio_detailed(
    io: IO,
    asyncio_detailed: Callable[P, Coroutine[Any, Any, Response[ErrorResponse | R]]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R | None:
    try:
        client = kwargs["client"] if "client" in kwargs and isinstance(kwargs["client"], AuthenticatedClient) else None

        response = await asyncio_detailed(*args, **kwargs)
        parsed_data = get_parsed_response_data(response)
    except ApiError as e:
        if e.status_code == 429 and client is not None:
            new_access_token = await io.prompt(
                prompt="API rate limit exceeded. Enter a new access token", password=True
            )
            if not new_access_token:
                raise e

            client.update_token(new_access_token)

            response = await asyncio_detailed(*args, **kwargs)
            parsed_data = get_parsed_response_data(response)
        else:
            raise e

    return parsed_data


async def get_asyncio_detailed(
    io: IO,
    asyncio_detailed: Callable[P, Coroutine[Any, Any, Response[ErrorResponse | R]]],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    response = await run_asyncio_detailed(io, asyncio_detailed, *args, **kwargs)
    if response is None:
        raise ApiError(
            status_code=500, error_detail=ErrorDetail(id="500", name="internal_error", detail="No response data")
        )
    return response
