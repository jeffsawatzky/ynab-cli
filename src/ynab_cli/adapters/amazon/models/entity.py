from typing import TYPE_CHECKING

from pydantic import BaseModel, computed_field

if TYPE_CHECKING:
    from ynab_cli.adapters.amazon.client import Client


class Entity(BaseModel, frozen=True):
    _is_hydrated: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_hydrated(self) -> bool:
        return self._is_hydrated

    async def hydrate(self, client: "Client") -> None:
        self._is_hydrated = True
