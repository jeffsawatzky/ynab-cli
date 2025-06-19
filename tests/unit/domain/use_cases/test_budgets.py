from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from ynab_cli.adapters.ynab import AuthenticatedClient, models, util
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

    settings = Settings(ynab=MagicMock(access_token="test_token"))
    params: use_cases.ListAllParams = {}
    client = MagicMock(spec=AuthenticatedClient)

    budgets = [budget async for budget in use_cases.list_all(settings, mock_io, params, client=client)]

    assert len(budgets) == 1
    assert budgets[0].name == "Budget 1"


@pytest.mark.anyio
async def test_list_all_api_error_401(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_budgets = mocker.patch("ynab_cli.domain.use_cases.budgets.get_budgets")
    mock_get_budgets.asyncio_detailed = AsyncMock()
    mock_get_budgets.asyncio_detailed.side_effect = util.ApiError(401)

    settings = Settings()
    params: use_cases.ListAllParams = {}
    client = MagicMock(spec=AuthenticatedClient)

    async for _ in use_cases.list_all(settings, mock_io, params, client=client):
        pass

    mock_io.print.assert_called_with("Invalid or expired access token. Please update your settings.")


@pytest.mark.anyio
async def test_list_all_api_error_429(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_budgets = mocker.patch("ynab_cli.domain.use_cases.budgets.get_budgets")
    mock_get_budgets.asyncio_detailed = AsyncMock()
    mock_get_budgets.asyncio_detailed.side_effect = util.ApiError(429)

    settings = Settings()
    params: use_cases.ListAllParams = {}
    client = MagicMock(spec=AuthenticatedClient)

    async for _ in use_cases.list_all(settings, mock_io, params, client=client):
        pass

    mock_io.print.assert_called_with("API rate limit exceeded. Try again later, or get a new access token.")


@pytest.mark.anyio
async def test_list_all_exception(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_budgets = mocker.patch("ynab_cli.domain.use_cases.budgets.get_budgets")
    mock_get_budgets.asyncio_detailed = AsyncMock()
    mock_get_budgets.asyncio_detailed.side_effect = Exception("Unexpected error")

    settings = Settings()
    params: use_cases.ListAllParams = {}
    client = MagicMock(spec=AuthenticatedClient)

    async for _ in use_cases.list_all(settings, mock_io, params, client=client):
        pass

    mock_io.print.assert_called_with("Exception when calling YNAB: Unexpected error")
