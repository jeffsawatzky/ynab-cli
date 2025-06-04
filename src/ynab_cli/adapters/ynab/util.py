from typing import Any, TypeVar

from .models import ErrorDetail, ErrorResponse
from .types import Response

M = TypeVar("M")


class ApiError(Exception):
    """Raised by API functions when the response status is not 200 OK and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, error_detail: ErrorDetail | None = None):
        self.status_code = status_code
        self.error_detail = error_detail

        super().__init__(f"Unexpected status code: {status_code}")


def ensure_success(response: Response[Any]) -> None:
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

    return


def get_ynab_model(response: Response[Any], type_: type[M]) -> M:
    parsed = response.parsed

    ensure_success(response)

    if not isinstance(parsed, type_):
        raise TypeError(f"Expected response to be of type {type_.__name__}, but got {type(parsed).__name__}")

    return parsed
