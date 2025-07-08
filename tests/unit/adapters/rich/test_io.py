from unittest.mock import Mock, patch

import pytest
from rich import progress as rich_progress
from rich import prompt as rich_prompt
from rich.console import Console

from ynab_cli.adapters.rich.io import RichIO, RichProgress


class TestRichProgress:
    def test_init_creates_task(self) -> None:
        """Test that RichProgress initializes with a task."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1

        rich_progress_instance = RichProgress(mock_progress)

        assert rich_progress_instance._progress == mock_progress
        assert rich_progress_instance._task_id == 1
        mock_progress.add_task.assert_called_once_with("Loading...")

    @pytest.mark.anyio
    async def test_update_starts_task_if_not_started(self) -> None:
        """Test that update starts task if not already started."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_task = Mock()
        mock_task.started = False
        mock_progress.tasks = {1: mock_task}

        rich_progress_instance = RichProgress(mock_progress)

        await rich_progress_instance.update(total=100.0)

        mock_progress.start_task.assert_called_once_with(1)
        mock_progress.update.assert_called_once_with(1, total=100.0, completed=None, advance=None)

    @pytest.mark.anyio
    async def test_update_does_not_start_task_if_already_started(self) -> None:
        """Test that update doesn't start task if already started."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_task = Mock()
        mock_task.started = True
        mock_progress.tasks = {1: mock_task}

        rich_progress_instance = RichProgress(mock_progress)

        await rich_progress_instance.update(completed=50.0)

        mock_progress.start_task.assert_not_called()
        mock_progress.update.assert_called_once_with(1, total=None, completed=50.0, advance=None)

    @pytest.mark.anyio
    async def test_update_with_all_parameters(self) -> None:
        """Test update with all parameters provided."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_task = Mock()
        mock_task.started = True
        mock_progress.tasks = {1: mock_task}

        rich_progress_instance = RichProgress(mock_progress)

        await rich_progress_instance.update(total=100.0, completed=25.0, advance=5.0)

        mock_progress.update.assert_called_once_with(1, total=100.0, completed=25.0, advance=5.0)


class TestRichIO:
    def test_init_creates_progress(self) -> None:
        """Test that RichIO initializes with RichProgress instance."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1

        rich_io = RichIO(mock_progress)

        assert rich_io._progress == mock_progress
        assert isinstance(rich_io.progress, RichProgress)
        assert rich_io.progress._progress == mock_progress

    @pytest.mark.anyio
    async def test_prompt_stops_and_starts_progress(self) -> None:
        """Test that prompt stops progress before asking and starts after."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_console = Mock(spec=Console)
        mock_progress.console = mock_console

        rich_io = RichIO(mock_progress)

        with patch.object(rich_prompt.Prompt, "ask", return_value="user_input") as mock_ask:
            result = await rich_io.prompt("Enter value:")

            assert result == "user_input"
            mock_progress.stop.assert_called_once()
            mock_progress.start.assert_called_once()
            mock_ask.assert_called_once_with("Enter value:", console=mock_console, password=False)

    @pytest.mark.anyio
    async def test_prompt_with_password_true(self) -> None:
        """Test prompt with password=True."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_console = Mock(spec=Console)
        mock_progress.console = mock_console

        rich_io = RichIO(mock_progress)

        with patch.object(rich_prompt.Prompt, "ask", return_value="secret") as mock_ask:
            result = await rich_io.prompt("Enter password:", password=True)

            assert result == "secret"
            mock_ask.assert_called_once_with("Enter password:", console=mock_console, password=True)

    @pytest.mark.anyio
    async def test_prompt_restarts_progress_on_exception(self) -> None:
        """Test that progress is restarted even if prompt raises exception."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_console = Mock(spec=Console)
        mock_progress.console = mock_console

        rich_io = RichIO(mock_progress)

        with patch.object(rich_prompt.Prompt, "ask", side_effect=KeyboardInterrupt()):
            with pytest.raises(KeyboardInterrupt):
                await rich_io.prompt("Enter value:")

            mock_progress.stop.assert_called_once()
            mock_progress.start.assert_called_once()

    @pytest.mark.anyio
    async def test_print_uses_console_print(self) -> None:
        """Test that print uses the progress console."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_console = Mock(spec=Console)
        mock_progress.console = mock_console

        rich_io = RichIO(mock_progress)

        await rich_io.print("Hello, world!")

        mock_console.print.assert_called_once_with("Hello, world!")

    @pytest.mark.anyio
    async def test_print_with_rich_markup(self) -> None:
        """Test print with rich markup."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_console = Mock(spec=Console)
        mock_progress.console = mock_console

        rich_io = RichIO(mock_progress)

        await rich_io.print("[bold red]Error:[/bold red] Something went wrong")

        mock_console.print.assert_called_once_with("[bold red]Error:[/bold red] Something went wrong")

    @pytest.mark.anyio
    async def test_progress_integration(self) -> None:
        """Test that the progress instance works correctly with the IO."""
        mock_progress = Mock(spec=rich_progress.Progress)
        mock_progress.add_task.return_value = 1
        mock_task = Mock()
        mock_task.started = False
        mock_progress.tasks = {1: mock_task}

        rich_io = RichIO(mock_progress)

        # Test that we can use the progress instance
        await rich_io.progress.update(total=100.0, completed=25.0)

        mock_progress.start_task.assert_called_once_with(1)
        mock_progress.update.assert_called_once_with(1, total=100.0, completed=25.0, advance=None)
