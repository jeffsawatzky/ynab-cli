from textual.reactive import var
from textual.widget import Widget

from ynab_cli.domain.settings import Settings


class RunnableWidget(Widget):
    settings: var[Settings] = var(Settings())

    async def run_command(self) -> None:
        raise NotImplementedError
