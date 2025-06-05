import logging
from typing import Generic, TypeVar

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import var
from textual.widgets import DataTable, Log, ProgressBar, Static
from textual.worker import Worker, WorkerState
from typing_extensions import override

from ynab_cli.domain.settings import Settings

log = logging.getLogger(__name__)


PARAMS = TypeVar("PARAMS")


class RunnableWidget(Static):
    settings: var[Settings] = var(Settings())

    async def run_command(self) -> None:
        raise NotImplementedError


class BaseCommand(RunnableWidget, Generic[PARAMS]):
    class CommandCompleted(Message):
        def __init__(self, worker_state: WorkerState) -> None:
            super().__init__()
            self.worker_state = worker_state

        pass

    @override
    def compose(self) -> ComposeResult:
        with Vertical():
            yield ProgressBar(total=0)
            yield DataTable()
            yield Log()

    @work(exclusive=True)
    async def _run_command_worker(self, use_case_params: PARAMS) -> None:
        self.query_one(ProgressBar).update(total=None, progress=0)
        self.query_one(DataTable).clear()
        self.query_one(Log).write_line("Running command...")
        await self._run_command(use_case_params)

    async def _run_command(self, use_case_params: PARAMS) -> None:
        raise NotImplementedError

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        log = self.query_one(Log)
        log.write_line(f"Worker state changed: {event.state}")

        if event.state not in (WorkerState.PENDING, WorkerState.RUNNING):
            self.post_message(self.CommandCompleted(event.state))
