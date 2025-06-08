from typing import TYPE_CHECKING

from attrs import define, field

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import Client


@define
class Entity:
    _is_hydrated: bool = field(default=False, init=False)

    @property
    def is_hydrated(self) -> bool:
        return self._is_hydrated

    async def hydrate(self, client: "Client") -> None:
        self._is_hydrated = True
