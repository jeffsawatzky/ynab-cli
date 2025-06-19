from unittest.mock import MagicMock, patch

import pytest
from rich import progress as rich_progress
from rich import prompt as rich_prompt

from ynab_cli.adapters.rich.io import RichIO, RichProgress


class TestRichProgress:
    @pytest.fixture
    def mock_progress(self) -> tuple[MagicMock, rich_progress.TaskID]:
        progress = MagicMock(spec=rich_progress.Progress)
        task_id = rich_progress.TaskID(1)
        return progress, task_id

    @pytest.fixture
    def rich_progress_instance(self, mock_progress: tuple[MagicMock, rich_progress.TaskID]) -> RichProgress:
        return RichProgress(mock_progress)

    @pytest.mark.anyio
    async def test_update_starts_task_if_not_started(
        self, rich_progress_instance: RichProgress, mock_progress: tuple[MagicMock, rich_progress.TaskID]
    ) -> None:
        progress, task_id = mock_progress
        mock_task = MagicMock()
        mock_task.started = False
        progress.tasks = {task_id: mock_task}

        await rich_progress_instance.update(total=100.0)

        progress.start_task.assert_called_once_with(task_id)
        progress.update.assert_called_once_with(task_id, total=100.0, completed=None, advance=None)

    @pytest.mark.anyio
    async def test_update_does_not_start_task_if_already_started(
        self, rich_progress_instance: RichProgress, mock_progress: tuple[MagicMock, rich_progress.TaskID]
    ) -> None:
        progress, task_id = mock_progress
        mock_task = MagicMock()
        mock_task.started = True
        progress.tasks = {task_id: mock_task}

        await rich_progress_instance.update(completed=50.0)

        progress.start_task.assert_not_called()
        progress.update.assert_called_once_with(task_id, total=None, completed=50.0, advance=None)

    @pytest.mark.anyio
    async def test_update_with_all_parameters(
        self, rich_progress_instance: RichProgress, mock_progress: tuple[MagicMock, rich_progress.TaskID]
    ) -> None:
        progress, task_id = mock_progress
        mock_task = MagicMock()
        mock_task.started = True
        progress.tasks = {task_id: mock_task}

        await rich_progress_instance.update(total=100.0, completed=75.0, advance=25.0)

        progress.update.assert_called_once_with(task_id, total=100.0, completed=75.0, advance=25.0)


class TestRichIO:
    @pytest.fixture
    def mock_progress_info(self) -> tuple[MagicMock, rich_progress.TaskID]:
        progress = MagicMock(spec=rich_progress.Progress)
        task_id = rich_progress.TaskID(1)
        progress.console = MagicMock()
        return progress, task_id

    @pytest.fixture
    def rich_io_instance(self, mock_progress_info: tuple[MagicMock, rich_progress.TaskID]) -> RichIO:
        return RichIO(mock_progress_info)

    def test_init_creates_rich_progress(self, mock_progress_info: tuple[MagicMock, rich_progress.TaskID]) -> None:
        rich_io = RichIO(mock_progress_info)

        assert isinstance(rich_io.progress, RichProgress)
        assert rich_io._progress == mock_progress_info[0]

    @pytest.mark.anyio
    async def test_prompt_stops_and_starts_progress(
        self, rich_io_instance: RichIO, mock_progress_info: tuple[MagicMock, rich_progress.TaskID]
    ) -> None:
        progress, _ = mock_progress_info

        with patch.object(rich_prompt.Prompt, "ask", return_value="user_input") as mock_ask:
            result = await rich_io_instance.prompt("Enter value:")

            progress.stop.assert_called_once()
            progress.start.assert_called_once()
            mock_ask.assert_called_once_with("Enter value:", console=progress.console, password=False)
            assert result == "user_input"

    @pytest.mark.anyio
    async def test_prompt_with_password(
        self, rich_io_instance: RichIO, mock_progress_info: tuple[MagicMock, rich_progress.TaskID]
    ) -> None:
        progress, _ = mock_progress_info

        with patch.object(rich_prompt.Prompt, "ask", return_value="secret") as mock_ask:
            result = await rich_io_instance.prompt("Enter password:", password=True)

            mock_ask.assert_called_once_with("Enter password:", console=progress.console, password=True)
            assert result == "secret"

    @pytest.mark.anyio
    async def test_prompt_starts_progress_even_on_exception(
        self, rich_io_instance: RichIO, mock_progress_info: tuple[MagicMock, rich_progress.TaskID]
    ) -> None:
        progress, _ = mock_progress_info

        with patch.object(rich_prompt.Prompt, "ask", side_effect=Exception("Test error")):
            with pytest.raises(Exception, match="Test error"):
                await rich_io_instance.prompt("Enter value:")

            progress.stop.assert_called_once()
            progress.start.assert_called_once()

    @pytest.mark.anyio
    async def test_print(
        self, rich_io_instance: RichIO, mock_progress_info: tuple[MagicMock, rich_progress.TaskID]
    ) -> None:
        progress, _ = mock_progress_info

        await rich_io_instance.print("Hello, World!")

        progress.console.print.assert_called_once_with("Hello, World!")
