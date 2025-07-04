from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, Concatenate, ParamSpec, TypeVar

from lagom import Container

from ynab_cli.domain.settings import Settings
from ynab_cli.host.container import make_container as host_make_container

R = TypeVar("R")
P = ParamSpec("P")


def init_container(container: Container) -> Container:
    from ynab_cli.adapters.ynab.client import AuthenticatedClient
    from ynab_cli.host.textual.app import YnabCliApp

    container[YnabCliApp] = lambda c: YnabCliApp(
        c[Settings],
        c[AuthenticatedClient],
    )

    return container


def make_container() -> Container:  # pragma: no cover
    return init_container(host_make_container())


def containerize(
    func: Callable[Concatenate[Container, P], Coroutine[Any, Any, R]],
) -> Callable[Concatenate[Settings, P], Coroutine[Any, Any, R]]:
    @wraps(func)
    async def wrapper(settings: Settings, *args: P.args, **kwargs: P.kwargs) -> R:
        container = make_container()
        container[Settings] = settings

        return await func(container, *args, **kwargs)

    return wrapper  # type: ignore[return-value]
