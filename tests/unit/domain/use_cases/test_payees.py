from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from ynab_cli.adapters.ynab import AuthenticatedClient, models
from ynab_cli.adapters.ynab.types import Response
from ynab_cli.domain.settings import Settings
from ynab_cli.domain.use_cases import payees as use_cases

uuid = UUID("00000000-0000-0000-0000-000000000000")


def test_should_skip_payee() -> None:
    assert use_cases._should_skip_payee(payee=models.Payee(id=uuid, name="Payee", deleted=False)) is False
    assert use_cases._should_skip_payee(payee=models.Payee(id=uuid, name="Payee", deleted=True)) is True

    assert use_cases._should_skip_payee(payee=models.Payee(id=uuid, name="Transfer : Savings", deleted=False)) is True
    assert use_cases._should_skip_payee(payee=models.Payee(id=uuid, name="Transfer : Savings", deleted=True)) is True

    assert use_cases._should_skip_payee(payee=models.Payee(id=uuid, name="Starting Balance", deleted=False)) is True
    assert use_cases._should_skip_payee(payee=models.Payee(id=uuid, name="Starting Balance", deleted=True)) is True

    assert use_cases._should_skip_payee(payee=models.Payee(id=uuid, name="My Starting Balance", deleted=False)) is False
    assert use_cases._should_skip_payee(payee=models.Payee(id=uuid, name="My Starting Balance", deleted=True)) is True


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
async def test_normalize_names(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.PayeesResponse(
            data=models.PayeesResponseData(
                payees=[
                    models.Payee(id=uuid, name="PAYEE.COM", deleted=False),
                    models.Payee(id=uuid, name="Payee 2", deleted=False),
                ],
                server_knowledge=0,
            )
        ),
    )
    mock_update_payee = mocker.patch("ynab_cli.domain.use_cases.payees.update_payee")
    mock_update_payee.asyncio_detailed = AsyncMock()

    settings = Settings()
    params: use_cases.NormalizeNamesParams = {}
    client = MagicMock(spec=AuthenticatedClient)

    results: list[tuple[models.Payee, str]] = []
    async for result in use_cases.normalize_names(settings, mock_io, params, client=client):
        payee, name = result
        assert isinstance(payee, models.Payee)
        assert isinstance(name, str)
        assert payee.name in ["PAYEE.COM"]
        assert name in ["Payee.com"]
        results.append(result)

    assert len(results) == 1
    assert mock_update_payee.asyncio_detailed.call_count == 1


@pytest.mark.anyio
async def test_list_duplicates(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.PayeesResponse(
            data=models.PayeesResponseData(
                payees=[
                    models.Payee(id=uuid, name="Payee 1", deleted=False),
                    models.Payee(id=uuid, name="Payee 2", deleted=False),
                    models.Payee(id=uuid, name="Payee 1", deleted=False),
                ],
                server_knowledge=0,
            )
        ),
    )

    settings = Settings()
    params: use_cases.ListDuplicatesParams = {}
    client = MagicMock(spec=AuthenticatedClient)

    results: list[tuple[models.Payee, models.Payee]] = []
    async for result in use_cases.list_duplicates(settings, mock_io, params, client=client):
        payee_1, payee_other_1 = result
        assert isinstance(payee_1, models.Payee)
        assert isinstance(payee_other_1, models.Payee)
        assert payee_1.name in ["Payee 1"]
        assert payee_other_1.name in ["Payee 1", "Payee 2"]
        results.append(result)

    assert len(results) == 3


@pytest.mark.anyio
async def test_list_unused(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.PayeesResponse(
            data=models.PayeesResponseData(
                payees=[
                    models.Payee(id=uuid, name="Payee 1", deleted=False),
                ],
                server_knowledge=0,
            )
        ),
    )
    mocke_get_transactions_by_payee = mocker.patch("ynab_cli.domain.use_cases.payees.get_transactions_by_payee")
    mocke_get_transactions_by_payee.asyncio_detailed = AsyncMock()
    mocke_get_transactions_by_payee.asyncio_detailed.return_value = Response(
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
    client = MagicMock(spec=AuthenticatedClient)

    results: list[models.Payee] = []
    async for result in use_cases.list_unused(settings, mock_io, params, client=client):
        assert isinstance(result, models.Payee)
        assert result.name in ["Payee 1"]
        results.append(result)

    assert len(results) == 1
    assert mock_update_payee.asyncio_detailed.call_count == 1


@pytest.mark.anyio
async def test_list_all(mocker: MockerFixture, mock_io: MagicMock) -> None:
    mock_get_payees = mocker.patch("ynab_cli.domain.use_cases.payees.get_payees")
    mock_get_payees.asyncio_detailed = AsyncMock()
    mock_get_payees.asyncio_detailed.return_value = Response(
        status_code=HTTPStatus.OK,
        content=b"",
        headers={},
        parsed=models.PayeesResponse(
            data=models.PayeesResponseData(
                payees=[
                    models.Payee(id=uuid, name="Payee 1", deleted=False),
                    models.Payee(id=uuid, name="Payee 2", deleted=False),
                    models.Payee(id=uuid, name="Payee 3", deleted=True),
                ],
                server_knowledge=0,
            )
        ),
    )

    settings = Settings()
    params: use_cases.ListAllParams = {}
    client = MagicMock(spec=AuthenticatedClient)

    results = []
    async for result in use_cases.list_all(settings, mock_io, params, client=client):
        assert isinstance(result, models.Payee)
        assert result.name in ["Payee 1", "Payee 2"]
        results.append(result)

    assert len(results) == 2
