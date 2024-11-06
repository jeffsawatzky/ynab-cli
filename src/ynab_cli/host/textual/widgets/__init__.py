import logging
from typing import ClassVar, Generic, TypeVar

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import var
from textual.widgets import DataTable, Log, Static
from textual.worker import Worker, WorkerState
from typing_extensions import override

from ynab_cli.domain.settings import Settings
from ynab_cli.host.textual.types import ActiveTabId, CommandParams

log = logging.getLogger(__name__)


class CommandRunnableWidget(Static):
    def run_command(self, params: CommandParams) -> None:
        raise NotImplementedError


PARAMS = TypeVar("PARAMS")


class BaseCommand(CommandRunnableWidget, Generic[PARAMS]):
    class CommandCompleted(Message):
        def __init__(self, worker_state: WorkerState) -> None:
            super().__init__()
            self.worker_state = worker_state

        pass

    ACTIVE_TAB_ID: ClassVar[ActiveTabId]

    settings: var[Settings] = var(Settings())

    @override
    def compose(self) -> ComposeResult:
        with Vertical():
            yield DataTable()
            yield Log()

    @override
    def run_command(self, params: CommandParams) -> None:
        active_tab_id, use_case_params = params
        if active_tab_id == self.__class__.ACTIVE_TAB_ID:
            self._run_command_worker(use_case_params)

    @work(exclusive=True)
    async def _run_command_worker(self, use_case_params: PARAMS) -> None:
        await self._run_command(use_case_params)

    async def _run_command(self, use_case_params: PARAMS) -> None:
        raise NotImplementedError

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        log = self.query_one(Log)
        log.write_line(f"Worker state changed: {event.state}")

        if event.state not in (WorkerState.PENDING, WorkerState.RUNNING):
            self.post_message(self.CommandCompleted(event.state))
