from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.types import Response
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import budgets as use_cases


@pytest.mark.anyio
async def test_list_all(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_budgets = mocker.patch("ynab_cli.domain.use_cases.budgets.get_budgets")
    mock_get_budgets.asyncio_detailed = AsyncMock()
    mock_get_budgets.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.BudgetSummaryResponse(
            data=models.BudgetSummaryResponseData(
                budgets=[
                    models.BudgetSummary(id=UUID("00000000-0000-0000-0000-000000000001"), name="Budget 1"),
                ],
            )
        ),
    )

    use_case = use_cases.ListAll(mock_io, MagicMock())
    settings = Settings()
    params: use_cases.ListAllParams = {}

    budgets = [budget async for budget in use_case(settings, params)]

    assert len(budgets) == 1
    assert budgets[0].name == "Budget 1"


@pytest.mark.parametrize(
    ("exception", "expected_print"),
    [
        (util.ApiError(401), "Invalid or expired access token. Please update your settings."),
        (util.ApiError(429), "API rate limit exceeded. Try again later, or get a new access token."),
        (Exception("Unexpected error"), "Exception when calling YNAB: Unexpected error"),
    ],
)
@pytest.mark.anyio
async def test_list_all_exception(
    exception: Exception, expected_print: str, mocker: MockerFixture, mock_io: MagicMock
) -> None:
    mock_get_budgets = mocker.patch("ynab_cli.domain.use_cases.budgets.get_budgets")
    mock_get_budgets.asyncio_detailed = AsyncMock()
    mock_get_budgets.asyncio_detailed.side_effect = exception

    use_case = use_cases.ListAll(mock_io, MagicMock())
    settings = Settings()
    params: use_cases.ListAllParams = {}

    async for _ in use_case(settings, params):
        pass

    mock_io.print.assert_called_with(expected_print)
