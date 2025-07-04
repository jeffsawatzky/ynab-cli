from collections.abc import Iterator
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from lagom import Container

from ynab_cli.host.click.container import init_container


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def container(container: Container) -> Iterator[Container]:
    container = init_container(container.clone()).clone()
    with patch("ynab_cli.host.click.container.make_container", return_value=container):
        # Ensure the container is initialized with the mocked init_container
        yield container
