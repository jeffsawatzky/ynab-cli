from uuid import UUID

import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def empty_uuid() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000000")
