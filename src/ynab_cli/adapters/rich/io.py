from rich import progress as rich_progress
from rich import prompt as rich_prompt
from typing_extensions import override

from ynab_cli.domain.ports.io import IO, Progress


class RichProgress(Progress):
    def __init__(self, progress_info: tuple[rich_progress.Progress, rich_progress.TaskID]) -> None:
        self._progress, self._task_id = progress_info

    @override
    async def update(
        self, *, total: float | None = None, completed: float | None = None, advance: float | None = None
    ) -> None:
        task = self._progress.tasks[self._task_id]
        if not task.started:
            self._progress.start_task(self._task_id)
        self._progress.update(self._task_id, total=total, completed=completed, advance=advance)


class RichIO(IO):
    def __init__(self, progress_info: tuple[rich_progress.Progress, rich_progress.TaskID]) -> None:
        progress, _ = progress_info
        self._progress = progress
        self.progress = RichProgress(progress_info)

    @override
    async def prompt(self, prompt: str, password: bool = False) -> str:
        try:
            self._progress.stop()
            return rich_prompt.Prompt.ask(prompt, console=self._progress.console, password=password)
        finally:
            self._progress.start()

    @override
    async def print(self, message: str) -> None:
        return self._progress.console.print(message)
