from unittest.mock import AsyncMock, MagicMock

import pytest

from ynab_cli.domain.ports.io import IO, Progress


@pytest.fixture
def mock_io() -> MagicMock:
    progress = MagicMock(spec=Progress)
    progress.update = AsyncMock()

    io = MagicMock(spec=IO)
    io.progress = progress
    io.prompt = AsyncMock()
    io.print = AsyncMock()
    return io
