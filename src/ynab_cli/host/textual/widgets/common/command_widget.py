from textual import on, work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import DataTable, Log, ProgressBar
from textual.worker import Worker, WorkerState
from typing_extensions import override

from ynab_cli.domain.settings import Settings


class CommandWidget(Widget):
    settings: var[Settings] = var(Settings())

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

    async def get_command_params(self) -> None:
        self._get_command_params_worker()

    @work(exclusive=True)
    async def _get_command_params_worker(self) -> None:
        await self._get_command_params()

    async def _get_command_params(self) -> None:
        self.app.notify("This command does not require parameters.")

    async def run_command(self) -> None:
        self._run_command_worker()

    @work(exclusive=True, name="_run_command_worker")
    async def _run_command_worker(self) -> None:
        self.query_one(ProgressBar).update(total=None, progress=0)
        self.query_one(DataTable).clear()
        self.query_one(Log).write_line("Running command...")
        await self._run_command()

    async def _run_command(self) -> None:
        raise NotImplementedError

    @on(Worker.StateChanged)
    def _worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.name == "_run_command_worker":
            log = self.query_one(Log)
            log.write_line(f"Worker state changed: {event.state}")

            if event.state not in (WorkerState.PENDING, WorkerState.RUNNING):
                self.post_message(self.CommandCompleted(event.state))
