import pytest
from lagom import Container, ExplicitContainer

from ynab_cli.domain.ports.io import IO, StdIO
from ynab_cli.host.container import init_container


@pytest.fixture
def container() -> Container:
    container = init_container(ExplicitContainer())
    container = container.clone()
    container[IO] = StdIO()  # type: ignore[type-abstract]
    return container
