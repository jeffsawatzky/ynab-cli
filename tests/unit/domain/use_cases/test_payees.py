from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from ynab_cli.adapters.ynab import models, util
from ynab_cli.adapters.ynab.types import Response
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import payees as use_cases


def test_should_skip_payee(empty_uuid: UUID) -> None:
    assert (
        use_cases._should_skip_payee(
            payee=models.Payee(
                id=empty_uuid,
                name="Payee",
                deleted=False,
            )
        )
        is False
    )
    assert (
        use_cases._should_skip_payee(
            payee=models.Payee(
                id=empty_uuid,
                name="Payee",
                deleted=True,
            )
        )
        is True
    )

    assert (
        use_cases._should_skip_payee(
            payee=models.Payee(
                id=empty_uuid,
                name="Transfer : Savings",
                deleted=False,
            )
        )
        is True
    )
    assert (
        use_cases._should_skip_payee(
            payee=models.Payee(
                id=empty_uuid,
                name="Transfer : Savings",
                deleted=True,
            )
        )
        is True
    )

    assert (
        use_cases._should_skip_payee(
            payee=models.Payee(
                id=empty_uuid,
                name="Starting Balance",
                deleted=False,
            )
        )
        is True
    )
    assert (
        use_cases._should_skip_payee(
            payee=models.Payee(
                id=empty_uuid,
                name="Starting Balance",
                deleted=True,
            )
        )
        is True
    )

    assert (
        use_cases._should_skip_payee(
            payee=models.Payee(
                id=empty_uuid,
                name="My Starting Balance",
                deleted=False,
            )
        )
        is False
    )
    assert (
        use_cases._should_skip_payee(
            payee=models.Payee(
                id=empty_uuid,
                name="My Starting Balance",
                deleted=True,
            )
        )
        is True
    )


def test_normalize_name() -> None:
    assert use_cases._normalize_name("payee") == "Payee"
    assert use_cases._normalize_name("payee ") == "Payee"
    assert use_cases._normalize_name(" payee") == "Payee"
    assert use_cases._normalize_name(" payee ") == "Payee"
    assert use_cases._normalize_name("PAYEE.COM") == "Payee.com"
    assert use_cases._normalize_name("PAYEE.CA") == "Payee.ca"
    assert use_cases._normalize_name("PAyee's RestAurAnt") == "Payee's Restaurant"
    assert use_cases._normalize_name("Payee's \t Restaurant\t\t\n\rand Grill") == "Payee's Restaurant And Grill"


@pytest.mark.anyio
async def test_normalize_names(mocker: MockerFixture, mock_io: MagicMock, empty_uuid: UUID) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.PayeesResponse(
            data=models.PayeesResponseData(
                payees=[
                    models.Payee(id=empty_uuid, name="PAYEE.COM", deleted=False),
                    models.Payee(id=empty_uuid, name="Payee 2", deleted=False),
                    models.Payee(id=empty_uuid, name="Deleted Payee", deleted=True),
                ],
                server_knowledge=0,
            )
        ),
    )
    mock_update_payee = mocker.patch("ynab_cli.domain.use_cases.payees.update_payee")
    mock_update_payee.asyncio_detailed = AsyncMock()

    settings = Settings()
    params: use_cases.NormalizeNamesParams = {}

    results: list[tuple[models.Payee, str]] = []
    async for result in use_cases.NormalizeNames(mock_io, MagicMock())(settings, params):
        payee, name = result
        assert isinstance(payee, models.Payee)
        assert isinstance(name, str)
        assert payee.name in ["PAYEE.COM"]
        assert name in ["Payee.com"]
        results.append(result)

    assert len(results) == 1
    assert mock_update_payee.asyncio_detailed.call_count == 1


@pytest.mark.parametrize(
    ("exception", "expected_print"),
    [
        (util.ApiError(401), "Invalid or expired access token. Please update your settings."),
        (util.ApiError(429), "API rate limit exceeded. Try again later, or get a new access token."),
        (Exception("Unexpected error"), "Exception when calling YNAB: Unexpected error"),
    ],
)
@pytest.mark.anyio
async def test_normalize_names_exception(
    exception: Exception, expected_print: str, mocker: MockerFixture, mock_io: MagicMock
) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.side_effect = exception

    settings = Settings()
    params: use_cases.NormalizeNamesParams = {}

    async for _ in use_cases.NormalizeNames(mock_io, MagicMock())(settings, params):
        pass

    mock_io.print.assert_called_with(expected_print)


@pytest.mark.anyio
async def test_list_duplicates(mocker: MockerFixture, mock_io: MagicMock, empty_uuid: UUID) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.PayeesResponse(
            data=models.PayeesResponseData(
                payees=[
                    models.Payee(id=empty_uuid, name="Payee 1", deleted=False),
                    models.Payee(id=empty_uuid, name="Payee 2", deleted=False),
                    models.Payee(id=empty_uuid, name="Payee 1", deleted=False),
                    models.Payee(id=empty_uuid, name="Deleted Payee", deleted=True),
                ],
                server_knowledge=0,
            )
        ),
    )

    settings = Settings()
    params: use_cases.ListDuplicatesParams = {}

    results: list[tuple[models.Payee, models.Payee]] = []
    async for result in use_cases.ListDuplicates(mock_io, MagicMock())(settings, params):
        payee_1, payee_other_1 = result
        assert isinstance(payee_1, models.Payee)
        assert isinstance(payee_other_1, models.Payee)
        assert payee_1.name in ["Payee 1"]
        assert payee_other_1.name in ["Payee 1", "Payee 2"]
        results.append(result)

    assert len(results) == 3


@pytest.mark.parametrize(
    ("exception", "expected_print"),
    [
        (util.ApiError(401), "Invalid or expired access token. Please update your settings."),
        (util.ApiError(429), "API rate limit exceeded. Try again later, or get a new access token."),
        (Exception("Unexpected error"), "Exception when calling YNAB: Unexpected error"),
    ],
)
@pytest.mark.anyio
async def test_list_duplicates_exception(
    exception: Exception, expected_print: str, mocker: MockerFixture, mock_io: MagicMock
) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.side_effect = exception

    settings = Settings()
    params: use_cases.ListDuplicatesParams = {}

    async for _ in use_cases.ListDuplicates(mock_io, MagicMock())(settings, params):
        pass

    mock_io.print.assert_called_with(expected_print)


@pytest.mark.anyio
async def test_list_unused(mocker: MockerFixture, mock_io: MagicMock, empty_uuid: UUID) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.PayeesResponse(
            data=models.PayeesResponseData(
                payees=[
                    models.Payee(id=empty_uuid, name="Payee 1", deleted=False),
                    models.Payee(id=empty_uuid, name="Deleted Payee", deleted=True),
                ],
                server_knowledge=0,
            )
        ),
    )
    mock_get_transactions_by_payee = mocker.patch("ynab_cli.domain.use_cases.payees.get_transactions_by_payee")
    mock_get_transactions_by_payee.asyncio_detailed = AsyncMock()
    mock_get_transactions_by_payee.asyncio_detailed.return_value = Response(
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
    mock_update_payee = mocker.patch("ynab_cli.domain.use_cases.payees.update_payee")
    mock_update_payee.asyncio_detailed = AsyncMock()

    settings = Settings()
    params: use_cases.ListUnusedParams = {
        "prefix_unused": True,
    }

    results: list[models.Payee] = []
    async for result in use_cases.ListUnused(mock_io, MagicMock())(settings, params):
        assert isinstance(result, models.Payee)
        assert result.name in ["Payee 1"]
        results.append(result)

    assert len(results) == 1
    assert mock_update_payee.asyncio_detailed.call_count == 1


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
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.side_effect = exception

    settings = Settings()
    params: use_cases.ListUnusedParams = {
        "prefix_unused": True,
    }

    async for _ in use_cases.ListUnused(mock_io, MagicMock())(settings, params):
        pass

    mock_io.print.assert_called_with(expected_print)


@pytest.mark.anyio
async def test_list_all(mocker: MockerFixture, mock_io: MagicMock, empty_uuid: UUID) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.PayeesResponse(
            data=models.PayeesResponseData(
                payees=[
                    models.Payee(id=empty_uuid, name="Payee 1", deleted=False),
                    models.Payee(id=empty_uuid, name="Payee 2", deleted=False),
                    models.Payee(id=empty_uuid, name="Payee 3", deleted=True),
                    models.Payee(id=empty_uuid, name="Deleted Payee", deleted=True),
                ],
                server_knowledge=0,
            )
        ),
    )

    settings = Settings()
    params: use_cases.ListAllParams = {}

    results = []
    async for result in use_cases.ListAll(mock_io, MagicMock())(settings, params):
        assert isinstance(result, models.Payee)
        assert result.name in ["Payee 1", "Payee 2"]
        results.append(result)

    assert len(results) == 2


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
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.side_effect = exception

    settings = Settings()
    params: use_cases.ListAllParams = {}

    async for _ in use_cases.ListAll(mock_io, MagicMock())(settings, params):
        pass

    mock_io.print.assert_called_with(expected_print)
