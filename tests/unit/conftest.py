from unittest.mock import AsyncMock, MagicMock

import pytest

from ynab_cli.domain.ports.io import IO, Progress


@pytest.fixture
def mock_io() -> IO:
    progress = MagicMock(spec=Progress)
    progress.update = AsyncMock(spec=Progress.update)

    io = MagicMock(spec=IO)
    io.progress = progress
    io.prompt = AsyncMock(spec=IO.prompt)
    io.print = AsyncMock(spec=IO.print)
    return io
