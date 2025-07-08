from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.types import Response
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import categories as use_cases


def test_should_skip_category_or_group__with_category(empty_uuid: UUID) -> None:
    assert (
        use_cases._should_skip_category_or_group(
            category_or_group=models.Category(
                id=empty_uuid,
                category_group_id=empty_uuid,
                name="Category",
                activity=0,
                balance=0,
                budgeted=0,
                hidden=False,
                deleted=False,
            )
        )
        is False
    )

    assert (
        use_cases._should_skip_category_or_group(
            category_or_group=models.Category(
                id=empty_uuid,
                category_group_id=empty_uuid,
                name="Category",
                activity=0,
                balance=0,
                budgeted=0,
                hidden=False,
                deleted=True,
            )
        )
        is True
    )


def test_should_skip_category_or_group__with_category_group(empty_uuid: UUID) -> None:
    assert (
        use_cases._should_skip_category_or_group(
            category_or_group=models.CategoryGroupWithCategories(
                id=empty_uuid,
                name="Category",
                hidden=False,
                categories=[],
                deleted=False,
            )
        )
        is False
    )

    assert (
        use_cases._should_skip_category_or_group(
            category_or_group=models.CategoryGroupWithCategories(
                id=empty_uuid,
                name="Category",
                hidden=False,
                categories=[],
                deleted=True,
            )
        )
        is True
    )


@pytest.mark.anyio
async def test_list_unused(mocker: MockerFixture, mock_io: MagicMock, empty_uuid: UUID) -> None:
    mock_get_categories = mocker.patch("ynab_cli.domain.use_cases.categories.get_categories")
    mock_get_categories.asyncio_detailed = AsyncMock()
    mock_get_categories.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.CategoriesResponse(
            data=models.CategoriesResponseData(
                category_groups=[
                    models.CategoryGroupWithCategories(
                        id=empty_uuid,
                        name="Category Group 1",
                        hidden=False,
                        deleted=False,
                        categories=[
                            models.Category(
                                id=empty_uuid,
                                category_group_id=empty_uuid,
                                name="Category 1",
                                activity=0,
                                balance=0,
                                budgeted=0,
                                hidden=False,
                                deleted=False,
                            ),
                            models.Category(
                                id=empty_uuid,
                                category_group_id=empty_uuid,
                                name="Deleted Category",
                                activity=0,
                                balance=0,
                                budgeted=0,
                                hidden=False,
                                deleted=True,
                            ),
                        ],
                    ),
                    models.CategoryGroupWithCategories(
                        id=empty_uuid, name="Deleted Category Group", hidden=False, deleted=True, categories=[]
                    ),
                ],
                server_knowledge=0,
            )
        ),
    )
    mock_get_transactions_by_category = mocker.patch(
        "ynab_cli.domain.use_cases.categories.get_transactions_by_category"
    )
    mock_get_transactions_by_category.asyncio_detailed = AsyncMock()
    mock_get_transactions_by_category.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.TransactionsResponse(
            data=models.TransactionsResponseData(
                transactions=[],
                server_knowledge=0,
            )
        ),
    )

    settings = Settings()
    params: use_cases.ListUnusedParams = {}

    results: list[models.Category] = []
    async for result in use_cases.ListUnused(mock_io, MagicMock())(settings, params):
        assert isinstance(result, models.Category)
        assert result.name in ["Category 1"]
        results.append(result)

    assert len(results) == 1


@pytest.mark.parametrize(
    ("exception", "expected_print"),
    [
        (util.ApiError(401), "Invalid or expired access token. Please update your settings."),
        (util.ApiError(429), "API rate limit exceeded. Try again later, or get a new access token."),
        (Exception("Unexpected error"), "Exception when calling YNAB: Unexpected error"),
    ],
)
@pytest.mark.anyio
async def test_list_unused_exception(
    exception: Exception, expected_print: str, mocker: MockerFixture, mock_io: MagicMock
) -> None:
    mock_get_categories = mocker.patch("ynab_cli.domain.use_cases.categories.get_categories")
    mock_get_categories.asyncio_detailed = AsyncMock()
    mock_get_categories.asyncio_detailed.side_effect = exception

    settings = Settings()
    params: use_cases.ListUnusedParams = {}

    async for _ in use_cases.ListUnused(mock_io, MagicMock())(settings, params):
        pass

    mock_io.print.assert_called_with(expected_print)


@pytest.mark.anyio
async def test_list_all(mocker: MockerFixture, mock_io: MagicMock, empty_uuid: UUID) -> None:
    mock_get_categories = mocker.patch("ynab_cli.domain.use_cases.categories.get_categories")
    mock_get_categories.asyncio_detailed = AsyncMock()
    mock_get_categories.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.CategoriesResponse(
            data=models.CategoriesResponseData(
                category_groups=[
                    models.CategoryGroupWithCategories(
                        id=empty_uuid,
                        name="Category Group 1",
                        hidden=False,
                        deleted=False,
                        categories=[
                            models.Category(
                                id=empty_uuid,
                                category_group_id=empty_uuid,
                                name="Category 1",
                                activity=0,
                                balance=0,
                                budgeted=0,
                                hidden=False,
                                deleted=False,
                            ),
                            models.Category(
                                id=empty_uuid,
                                category_group_id=empty_uuid,
                                name="Deleted Category",
                                activity=0,
                                balance=0,
                                budgeted=0,
                                hidden=False,
                                deleted=True,
                            ),
                        ],
                    ),
                    models.CategoryGroupWithCategories(
                        id=empty_uuid, name="Deleted Category Group", hidden=False, deleted=True, categories=[]
                    ),
                ],
                server_knowledge=0,
            )
        ),
    )

    settings = Settings()
    params: use_cases.ListAllParams = {}

    results = []
    async for result in use_cases.ListAll(mock_io, MagicMock())(settings, params):
        assert isinstance(result, models.Category)
        assert result.name in ["Category 1"]
        results.append(result)

    assert len(results) == 1


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
    mock_get_categories = mocker.patch("ynab_cli.domain.use_cases.categories.get_categories")
    mock_get_categories.asyncio_detailed = AsyncMock()
    mock_get_categories.asyncio_detailed.side_effect = exception

    settings = Settings()
    params: use_cases.ListAllParams = {}

    async for _ in use_cases.ListAll(mock_io, MagicMock())(settings, params):
        pass

    mock_io.print.assert_called_with(expected_print)
